# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from functools import singledispatchmethod

from benchexec.tools.template import BaseTool2
from benchexec.util import ProcessExitCode
from fm_tools import FmData
from fm_tools.run import get_tool_info


@dataclass(frozen=True)
class RunResult:
    command: tuple[str, ...]
    exit_code: int
    raw_output: str

    def as_benchexec_run(self):
        return BaseTool2.Run(
            cmdline=self.command,
            exit_code=ProcessExitCode.from_raw(self.exit_code),
            output=BaseTool2.RunOutput(self.raw_output.splitlines(keepends=True)),
            termination_reason=False,  # TODO: We do not know about this
        )

    @singledispatchmethod
    def determine_result(self, tool: BaseTool2) -> str:
        return tool.determine_result(self.as_benchexec_run())

    @determine_result.register
    def _(self, tool: FmData) -> str:
        tool = get_tool_info(tool)
        return self.determine_result(tool)
