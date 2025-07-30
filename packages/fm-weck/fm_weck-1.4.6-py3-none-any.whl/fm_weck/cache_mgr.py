# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import shutil

logger = logging.getLogger(__name__)


def ask_and_clear(cache_location: str):
    response = (
        input(f"The following cache location will be deleted: {cache_location}\nDo you want to proceed? (Y/n): ")
        .strip()
        .lower()
    )

    if response == "y":
        clear_cache(cache_location)
    elif response == "n":
        return
    else:
        logger.error(f"Unknown command '{response}'\n")
        ask_and_clear(cache_location)


def clear_cache(cache_location: str):
    if not cache_location:
        logger.error("Cache location is unknown.")
        return

    if os.path.isdir(cache_location):
        for item in os.listdir(cache_location):
            item_path = os.path.join(cache_location, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            except Exception as e:
                logger.error(f"Error removing {item_path}: {e}")
    else:
        logger.error(f"The path {cache_location} is not a valid directory.")
