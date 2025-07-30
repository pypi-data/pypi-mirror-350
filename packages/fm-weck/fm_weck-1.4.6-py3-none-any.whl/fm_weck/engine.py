# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import io
import logging
import shutil
import signal
import subprocess
import sys
from abc import ABC, abstractmethod
from functools import cached_property, singledispatchmethod
from pathlib import Path
from tempfile import mkdtemp
from typing import Callable, List, Optional, Union

from fm_weck.run_result import RunResult

try:
    from fm_tools.fmdata import FmData, FmImageConfig
except ImportError:
    # Mock the FmData and FmImageConfig class for type checking
    class FmData:
        def get_images(self):
            pass

    class FmImageConfig:
        pass


from fm_weck.config import Config, parse_fm_data
from fm_weck.exceptions import NoImageError
from fm_weck.image_mgr import ImageMgr

logger = logging.getLogger(__name__)

CWD_MOUNT_LOCATION = "/home/cwd"
CACHE_MOUNT_LOCATION = "/home/fm-weck_cache"
OUTPUT_MOUNT_LOCATION = "/home/output"

RESERVED_LOCATIONS = frozenset([CACHE_MOUNT_LOCATION, CWD_MOUNT_LOCATION, OUTPUT_MOUNT_LOCATION])


class Engine(ABC):
    interactive: bool = False
    handle_io: bool = True
    print_output_to_stdout: bool = True
    add_benchexec_capabilities: bool = False
    add_mounting_capabilities: bool = True
    image: Optional[str] = None
    dry_run: bool = False

    def __init__(self, image: Union[str, FmImageConfig]):
        self._tmp_output_dir = Path(mkdtemp("fm_weck_output")).resolve()
        self.image = self._initialize_image(image)
        self.extra_args = {}
        self._engine = None

        self.output_dir = Path.cwd() / "output"
        self.log_file = None

        self.env = {}

    def __del__(self):
        if self._tmp_output_dir.exists():
            shutil.rmtree(self._tmp_output_dir)

    def get_workdir(self):
        return Path(CWD_MOUNT_LOCATION)

    def set_output_log(self, output_log: Path):
        self.log_file = output_log

    def set_output_files_dir(self, output_log: Path):
        self.output_dir = output_log

    def mount(self, source: str, target: str):
        self.extra_args["mounts"] = self.extra_args.get("mounts", []) + [
            "-v",
            f"{source}:{target}",
        ]

    def add_container_long_opt(self, arg: list[str]):
        """
        Add a long option to the container command.
        If the first element of the list does not start with "--", it will be prepended.
        Example:
        add_container_long_opt(["--option", "value"]) -> --option value
        add_container_long_opt(["option", "value"]) -> --option value
        """

        if not arg:
            raise ValueError("Argument must not be empty.")

        base = arg[0]
        if not base.startswith("--"):
            base = f"--{base}"

        self.extra_args["container_args"] = self.extra_args.get("container_args", []) + [base] + arg[1:]

    @abstractmethod
    def benchexec_capabilities(self):
        raise NotImplementedError

    def base_command(self):
        return [self._engine, "run"]

    def interactive_command(self):
        return ["-it"]

    def add_environment(self):
        return sum([["-e", f"{key}={value}"] for key, value in self.env.items()], [])

    def setup_command(self):
        return [
            "--security-opt",
            "label=disable",
            "--entrypoint",
            '[""]',
            "-v",
            f"{Path.cwd().absolute()}:{CWD_MOUNT_LOCATION}",
            "-v",
            f"{Config().cache_location}:{CACHE_MOUNT_LOCATION}",
            "-v",
            f"{self._tmp_output_dir}:{OUTPUT_MOUNT_LOCATION}",
            "--workdir",
            str(self.get_workdir()),
            "--rm",
        ]

    def mounting_capabilities(self):
        return [
            "--cap-add",
            "SYS_ADMIN",
        ]

    def _move_output(self):
        if not self.output_dir.exists():
            self.output_dir.mkdir()
        for file in self._tmp_output_dir.iterdir():
            if file.is_file():
                shutil.copy(file, self.output_dir / file.name)
            elif file.is_dir():
                try:
                    # This may fail if there are some permission errors,
                    # but we don't want to stop the whole process in case this happens.
                    # One such example is UAutomizer's output which contains
                    # some config files produced by Java.
                    shutil.copytree(
                        file,
                        self.output_dir,
                        dirs_exist_ok=True,
                    )
                except shutil.Error as e:
                    logger.warning(f"Error while copying the output {file} directory: {e}")

    def assemble_command(self, command: tuple[str, ...]) -> list[str]:
        base = self.base_command()
        if self.add_benchexec_capabilities:
            base += self.benchexec_capabilities()

        if self.add_mounting_capabilities:
            base += self.mounting_capabilities()

        base += self.setup_command()
        base += self.add_environment()

        if self.interactive:
            base += self.interactive_command()

        for value in self.extra_args.values():
            if isinstance(value, list) and not isinstance(value, str):
                base += value
            else:
                base.append(value)

        _command = self._prep_command(command)
        return base + [self.image, *_command]

    def _prep_command(self, command: tuple[str, ...]) -> tuple[str, ...]:
        """We want to map absolute paths of the current working directory to the
        working directory of the container."""

        def _map_path(p: Union[str, Path]) -> Union[str, Path]:
            if isinstance(p, Path):
                if not p.is_absolute():
                    return p
                if p.is_relative_to(Path.cwd()):
                    relative = p.relative_to(Path.cwd())
                    return self.get_workdir() / relative
                elif p.is_relative_to(Config().cache_location):
                    relative = p.relative_to(Config().cache_location)
                    return Path(CACHE_MOUNT_LOCATION) / relative
                else:
                    return p
            mapped = _map_path(Path(p))
            if Path(p) == mapped:
                return p
            else:
                return mapped

        return tuple(map(_map_path, command))

    @singledispatchmethod
    def _initialize_image(self, image: str) -> str:
        logger.debug("Initializing image from string %s", image)
        return image

    @_initialize_image.register
    def _from_fm_config(self, fm_config: FmImageConfig) -> str:
        logger.debug("Initializing image from FmImageConfig: %s", fm_config)
        return ImageMgr().prepare_image(self, fm_config)

    @staticmethod
    def extract_image(fm: Union[str, Path], version: str, config: dict) -> str:
        image = config.get("defaults", {}).get("image", None)

        return parse_fm_data(fm, version).get_images().with_fallback(image)

    @staticmethod
    def _base_engine_class(config: Config):
        engine = config.defaults().get("engine", "podman").lower()

        if engine == "docker":
            return Docker
        if engine == "podman":
            return Podman

        raise ValueError(f"Unknown engine {engine}")

    @singledispatchmethod
    @staticmethod
    def from_config(config: Config) -> "Engine":
        Base = Engine._base_engine_class(config)
        engine = Base(config.from_defaults_or_none("image"))
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: Path, version: str, config: Config):
        image = Engine.extract_image(fm, version, config)
        Base = Engine._base_engine_class(config)
        engine = Base(image)
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: str, version: str, config: Config):
        image = Engine.extract_image(fm, version, config)
        Base = Engine._base_engine_class(config)
        engine = Base(image)
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: FmData, config: Config):
        image = fm.get_images().with_fallback(config.from_defaults_or_none("image"))
        Base = Engine._base_engine_class(config)
        engine = Base(image)
        return Engine._prepare_engine(engine, config)

    @staticmethod
    def _prepare_engine(engine, config: Config) -> "Engine":
        for src, target in config.mounts():
            if not Path(src).exists():
                logger.warning("Mount source %s does not exist. Ignoring it...", src)
                continue
            engine.mount(src, target)

        if config.is_dry_run():
            engine.dry_run = True

        return engine

    @abstractmethod
    def image_from(self, containerfile: Path) -> "BuildCommand":
        pass

    class BuildCommand(ABC):
        build_args: List[str] = []

        @abstractmethod
        def __init__(self, containerfile: Path, **kwargs):
            pass

        def base_image(self, image: str):
            self.build_args += ["--build-arg", f"BASE_IMAGE={image}"]
            return self

        def packages(self, packages: list[str]):
            self.build_args += ["--build-arg", f"REQUIRED_PACKAGES={' '.join(packages)}"]
            return self

        def engine(self):
            return [self._engine]

        def build(self):
            cmd = self.engine() + [
                "build",
                "-f",
                self.containerfile,
                *self.build_args,
                ".",
            ]

            logging.debug("Running command: %s", cmd)

            ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            tag = ret.stdout.decode().splitlines()[-1].strip()
            logger.info("Built image %s", tag)
            logger.debug("Output of build image was:\n%s", ret.stdout.decode())
            logger.debug("Error of build image was:\n%s", ret.stderr.decode())
            if ret.returncode != 0:
                raise subprocess.CalledProcessError(
                    ret.returncode, cmd, output=ret.stdout.decode(), stderr=ret.stderr.decode()
                )

            return tag

    def _run_process_without_attaching_io(
        self, command: tuple[str, ...] | list[str], timeout_sec: Optional[float] = None
    ) -> RunResult:
        def terminate_process_group(signal_received, frame):
            if process:
                logging.info("Received signal %s. Terminating container process.", signal_received)
                process.send_signal(signal.SIGTERM)

        # Register signal handler
        signal.signal(signal.SIGINT, terminate_process_group)
        signal.signal(signal.SIGTERM, terminate_process_group)

        logger.debug("\n\nRunning command:\n%s\n\n", " ".join(map(str, command)))
        process = subprocess.Popen(command)

        try:
            process.wait(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait()

        return RunResult(command, process.returncode, io.StringIO())

    def _run_process(self, command: tuple[str, ...] | list[str], timeout_sec: Optional[float] = None) -> RunResult:
        process = None  # To make sure process is defined if a signal is caught early

        def terminate_process_group(signal_received, frame):
            if process:
                logging.info("Received signal %s. Terminating container process.", signal_received)
                process.send_signal(signal.SIGTERM)

        # Register signal handler
        signal.signal(signal.SIGINT, terminate_process_group)
        signal.signal(signal.SIGTERM, terminate_process_group)

        logger.debug("\n\nRunning command:\n%s\n\n", " ".join(map(str, command)))

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        full_stdout = io.StringIO()

        def run_and_poll(writer: Callable[[str], None]):
            while process.poll() is None:
                line = process.stdout.readline().decode("utf-8")
                writer(line)
                if self.print_output_to_stdout:
                    sys.stdout.write(line)

        if self.log_file is None:
            run_and_poll(full_stdout.write)
        else:
            with self.log_file.open("w") as log:
                run_and_poll(log.write)

        assert process is not None, "Process should be defined at this point."
        try:
            process.wait(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait()

        if self.log_file is not None:
            with self.log_file.open("r") as log:
                return RunResult(command, process.returncode, log.read())

        return RunResult(command, process.returncode, full_stdout.read())

    def run(self, *command: str, timeout_sec: Optional[float] = None) -> RunResult:
        if self.image is None:
            raise NoImageError("No image set for engine.")

        command = self.assemble_command(command)
        logger.debug("Running: %s", command)
        if self.dry_run:
            print("Command to be executed:")
            print(" ".join(map(str, command)))
            return 0, ""

        if self.interactive or not self.handle_io:
            return self._run_process_without_attaching_io(command, timeout_sec=timeout_sec)

        result = self._run_process(command, timeout_sec=timeout_sec)
        self._move_output()
        return result


class Podman(Engine):
    def __init__(self, image: Union[str, FmImageConfig]):
        super().__init__(image)
        self._engine = "podman"

    class PodmanBuildCommand(Engine.BuildCommand):
        def __init__(self, containerfile: Path):
            self.containerfile = containerfile
            self._engine = "podman"

    def image_from(self, containerfile: Path):
        return self.PodmanBuildCommand(containerfile)

    def benchexec_capabilities(self):
        return [
            # "--annotation",
            # "run.oci.keep_original_groups=1",
            # "--cgroups=split",
            "--security-opt",
            "unmask=/sys/fs/cgroup",
            "--security-opt",
            "unmask=/proc/*",
            "--security-opt",
            "seccomp=unconfined",
            # "-v",
            # "/sys/fs/cgroup:/sys/fs/cgroup:rw",
        ]


class Docker(Engine):
    def __init__(self, image: Union[str, FmImageConfig]):
        super().__init__(image)
        logger.debug("Image: %s", self.image)
        self._engine = "docker"

    class DockerBuildCommand(Engine.BuildCommand):
        def __init__(self, containerfile: Path, needs_sudo: bool = False):
            self.containerfile = containerfile
            if needs_sudo:
                self._engine = "sudo docker"
            else:
                self._engine = "docker"

        def engine(self):
            return self._engine.split(" ")

    def image_from(self, containerfile: Path):
        return self.DockerBuildCommand(containerfile, needs_sudo=self._requires_sudo)

    @cached_property
    def _requires_sudo(self):
        """Test if docker works without sudo."""
        try:
            subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.debug("Docker does not require sudo.")
            return False
        except subprocess.CalledProcessError:
            logger.debug("Docker requires sudo.")
            return True

    def base_command(self):
        if self._requires_sudo:
            return ["sudo", "docker", "run"]
        return ["docker", "run"]

    def setup_command(self):
        return [
            "--entrypoint",
            "/bin/sh",
            "-v",
            f"{Path.cwd().absolute()}:{CWD_MOUNT_LOCATION}",
            "-v",
            f"{Config().cache_location}:{CACHE_MOUNT_LOCATION}",
            "-v",
            f"{self._tmp_output_dir}:{OUTPUT_MOUNT_LOCATION}",
            "--workdir",
            str(self.get_workdir()),
            "--rm",
        ]

    def benchexec_capabilities(self):
        return [
            "--security-opt",
            "seccomp=unconfined",
            "--security-opt",
            "apparmor=unconfined",
            "--security-opt",
            "label=disable",
            "-v /sys/fs/cgroup:/sys/fs/cgroup",
        ]
