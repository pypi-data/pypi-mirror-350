#!/usr/bin/python3 -u

# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import argparse

from . import client
from . import server
from . import util
from . import const

def mainline():

    parser = argparse.ArgumentParser(description="bbperf: end to end performance and bufferbloat measurement tool")

    parser.add_argument("-v", "--verbosity",
        action="count",
        default=0,
        help="increase output verbosity (can be repeated)")

    parser.add_argument("-q", "--quiet",
        action="count",
        default=0,
        help="decrease output verbosity (can be repeated)")

    parser.add_argument("-s", "--server",
        action="store_true",
        default=False,
        help="run in server mode")

    parser.add_argument("-c", "--client",
        metavar="SERVER_IP",
        default=None,
        help="run in client mode")

    parser.add_argument("-p", "--port",
        metavar="SERVER_PORT",
        type=int,
        default=const.SERVER_PORT,
        help="server port (default: 5301)")

    parser.add_argument("-R", "--reverse",
        action="store_true",
        default=False,
        help="data flow in download direction (server to client)")

    parser.add_argument("-t", "--time",
        metavar="SECONDS",
        type=int,
        default=const.DURATION_SEC,
        help="duration of run in seconds")

    parser.add_argument("-u", "--udp",
        action="store_true",
        default=False,
        help="run in UDP mode (default: TCP mode)")

    parser.add_argument("-g", "--graph",
        action="store_true",
        default=False,
        help="generate graph (requires gnuplot)")

    parser.add_argument("-k", "--keep",
        action="store_true",
        default=False,
        help="keep data file")

    parser.add_argument("-J", "--json-file",
        default=None,
        help="JSON output file")

    args = parser.parse_args()

    util.validate_args(args)

    if args.client:
        client.client_mainline(args)
    else:
        server.server_mainline(args)


if __name__ == '__main__':
    mainline()
