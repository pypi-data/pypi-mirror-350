# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import yaml
from tabulate import tabulate


class VersionListing:
    tool_and_version: dict[str, list] = {}

    def __init__(self, tool_paths: list):
        for tool_path in tool_paths:
            with open(tool_path) as stream:
                tool_data = yaml.safe_load(stream)

                versions = [version_data["version"] for version_data in tool_data["versions"]]
                self.tool_and_version[tool_data["name"]] = versions

    def print_versions(self):
        data_list = list(self.tool_and_version.items())
        print(tabulate(data_list, headers=["TOOL", "VERSIONS"], tablefmt="fancy_grid"))
