#
# Copyright (c) 2017 Red Hat, Inc.
#
# This file is part of gluster-health-report project which is a
# subproject of GlusterFS ( www.gluster.org)
#
# This file is licensed to you under your choice of the GNU Lesser
# General Public License, version 3 or any later version (LGPLv3 or
# later), or the GNU General Public License, version 2 (GPLv2), in all
# cases as published by the Free Software Foundation.

import sys

from glusterlog import parse

# To print Text in Color in bash terminal
# ESC[ATTR;FG_COLOR;BG_COLORm<TEXT>ESC[RESET
ESC = "\033"
RESET = "\033[0m"

# Bash Attributes
ATTR_NORMAL = "[0;"
ATTR_BOLD = "[1;"

# Bash Foreground colors
FG_BLACK = "30"
FG_RED = "31"
FG_GREEN = "32"
FG_YELLOW = "33"
FG_BLUE = "34"
FG_PURPLE = "35"
FG_CYAN = "36"
FG_WHITE = "37"

# Bash Background Colors
BG_BLACK = "40"
BG_RED = "41"
BG_GREEN = "42"
BG_YELLOW = "43"
BG_BLUE = "44"
BG_PURPLE = "45"
BG_CYAN = "46"
BG_WHITE = "47"


def normal_color(color, bg=None):
    if bg is not None:
        return ESC + ATTR_NORMAL + color + ";" + bg + "m"

    return ESC + ATTR_NORMAL + color + "m"


def bold_color(color, bg=None):
    if bg is not None:
        return ESC + ATTR_BOLD + color + ";" + bg + "m"

    return ESC + ATTR_BOLD + color + "m"


def level_color(lvl):
    if lvl == "I":
        return bold_color(FG_BLACK, BG_GREEN)
    elif lvl == "E":
        return bold_color(FG_WHITE, BG_RED)
    elif lvl == "W":
        return bold_color(FG_BLACK, BG_YELLOW)
    else:
        return normal_color(FG_BLACK, BG_WHITE)


TS_COLOR = normal_color(FG_YELLOW)
MSGID_COLOR = normal_color(FG_BLACK, BG_YELLOW)
FILEINFO_COLOR = normal_color(FG_CYAN)
DOMAIN_COLOR = normal_color(FG_BLUE)
MSG_COLOR = normal_color(FG_WHITE)
KEY_COLOR = normal_color(FG_BLACK, BG_WHITE)
VALUE_COLOR = normal_color(FG_YELLOW)


def colorize():
    for line in sys.stdin:
        line = line.strip()
        parsed_data = parse(line)
        if parsed_data.known_format:
            msg = "{TS_COLOR}{ts:26}{RESET} ".format(
                TS_COLOR=TS_COLOR,
                RESET=RESET,
                ts=parsed_data.ts,
            )
            msg += "{LEVEL_COLOR} {level} {RESET} ".format(
                RESET=RESET,
                LEVEL_COLOR=level_color(parsed_data.log_level),
                level=parsed_data.log_level
            )
            if parsed_data.msg_id is not None:
                msg += "{MSGID_COLOR}MSGID: {msg_id:>5}{RESET} ".format(
                    MSGID_COLOR=MSGID_COLOR,
                    msg_id=parsed_data.msg_id,
                    RESET=RESET
                )

            msg += "{FILEINFO_COLOR}{fileinfo}{RESET} ".format(
                FILEINFO_COLOR=FILEINFO_COLOR,
                fileinfo=parsed_data.file_info,
                RESET=RESET
            )
            msg += "{DOMAIN_COLOR}{domain}{RESET} ".format(
                DOMAIN_COLOR=DOMAIN_COLOR,
                domain=parsed_data.domain,
                RESET=RESET
            )
            msg += "{MSG_COLOR}{message}{RESET}".format(
                MSG_COLOR=MSG_COLOR,
                message=parsed_data.message,
                RESET=RESET
            )
            for k, v in parsed_data.fields.items():
                msg += " {KEY_COLOR}{k}{RESET}={VALUE_COLOR}{v}{RESET}".format(
                    k=k,
                    v=v,
                    KEY_COLOR=KEY_COLOR,
                    VALUE_COLOR=VALUE_COLOR,
                    RESET=RESET
                )

            print(msg)
        else:
            print(line)


def main():
    try:
        colorize()
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
