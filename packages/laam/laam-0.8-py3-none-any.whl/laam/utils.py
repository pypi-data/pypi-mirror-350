# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import contextlib
import enum
import sys


#############
# Constants #
#############
class Color(enum.Enum):
    green = "\033[1;32m"
    grey = "\033[0;90m"
    red = "\033[1;31m"
    yellow = "\033[1;33m"
    end = "\033[0m"


PRIORITIES = {
    3: Color.red.value,
    4: Color.red.value,
    5: Color.yellow.value,
    7: Color.grey.value,
}


def get_color(priority):
    return PRIORITIES.get(priority, "")


def print_error(ret, expected=200) -> bool:
    if ret.status_code == expected:
        return False

    print("Unable to call the appliance API", file=sys.stderr)
    print(f"Code: {ret.status_code}", file=sys.stderr)
    with contextlib.suppress(Exception):
        print(f"Error: {ret.json()['detail']}", file=sys.stderr)
    return True
