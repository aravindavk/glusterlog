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

import re

# [TS] LOG_LEVEL [MSGID: <ID>] [FILE:LINE:FUNC] DOMAIN: MSG
# MSGID is optional and MSG can be structured log format or can be normal msg
log_pattern = re.compile('\[([^\]]+)\]\s'
                         '([IEWTD])\s'
                         '(\[MSGID:\s([^\]]+)\]\s)?'
                         '\[([^\]]+)\]\s'
                         '([^:]+):\s'
                         '(.+)')


class ParsedData(object):
    def __init__(self):
        self.known_format = False
        self.ts = None
        self.log_level = None
        self.msg_id = None
        self.file_info = None
        self.domain = None
        self.message = None
        self.fields = {}

    def __str__(self):
        data = (
            "Known Format: {0}\n"
            "Timestamp   : {1}\n"
            "Log Level   : {2}\n"
            "MSG ID      : {3}\n"
            "File Info   : {4}\n"
            "Domain      : {5}\n"
            "Message     : {6}\n".format(
                self.known_format,
                self.ts,
                self.log_level,
                self.msg_id,
                self.file_info,
                self.domain,
                self.message
            ))
        if self.fields:
            data += "\nFields      : "
            for k, v in self.fields.items():
                data += "{0}={1}, ".format(k, v)

        data = data.strip(", ")
        return data

    def json(self):
        import json

        return json.dumps(
            {
                "known_format": self.known_format,
                "timestamp": self.ts,
                "log_level": self.log_level,
                "msg_id": self.msg_id,
                "file_info": self.file_info,
                "domain": self.domain,
                "message": self.message,
                "fields": self.fields
            },
            indent=4
        )


def parse(data):
    m = log_pattern.match(data)
    out = ParsedData()
    if m:
        out.known_format = True
        out.ts = m.group(1)
        out.log_level = m.group(2)
        out.msg_id = m.group(4)
        out.file_info = m.group(5)
        out.domain = m.group(6)

        msg_parts = m.group(7).split("\t")
        out.message = msg_parts[0]

        out.fields = {}
        if (len(msg_parts) > 1):
            for i in range(1, len(msg_parts)):
                key_value = msg_parts[i].strip().split("=")
                # If no value, then this will be same as key
                out.fields[key_value[0].strip()] = key_value[-1].strip()
    else:
        # No match, add raw message to message, known_format is False
        out.message = data

    return out
