#
# Copyright (c) 2017 Red Hat, Inc.
#
# This file is part of glusterlog project which is a
# subproject of GlusterFS ( www.gluster.org)
#
# This file is licensed to you under your choice of the GNU Lesser
# General Public License, version 3 or any later version (LGPLv3 or
# later), or the GNU General Public License, version 2 (GPLv2), in all
# cases as published by the Free Software Foundation.

import sys
from argparse import ArgumentParser

from glusterlog import parse


def tojson():
    parser = ArgumentParser()
    parser.add_argument("--single-json", action="store_true")
    args = parser.parse_args()

    prev = "[" if args.single_json else ""
    for line in sys.stdin:
        parsed_data = parse(line)
        data = parsed_data.json()
        if args.single_json:
            data += ","

        print(prev)
        prev = data

    # Print the last row
    print(prev.strip(","))

    if args.single_json:
        print("]")


def main():
    try:
        tojson()
    except KeyboardInterrupt:
        sys.exit(1)
if __name__ == "__main__":
    main()
