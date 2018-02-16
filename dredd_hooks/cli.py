#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2015, 2016 Apiary Czech Republic, s.r.o.
#  License: MIT
#
from __future__ import print_function

import sys

import dredd_hooks as dredd


def run_dredd_hooks():
    import argparse
    parser = argparse.ArgumentParser(
        description='Start the Python Dredd hooks worker.'
    )

    parser.add_argument('files', metavar='file', type=str, nargs='*',
                        default=[], help='the hook files (or globs) to load')
    parser.add_argument('--host', dest='host', type=str, default='127.0.0.1',
                        help='the host to listen on')
    parser.add_argument('--port', dest='port', type=int, default=61321,
                        help='the port to listen to')

    args = parser.parse_args()
    dredd.main(args.files, host=args.host, port=args.port)


def main():
    """Run dredd_hooks as a script."""
    try:
        sys.exit(run_dredd_hooks())
    except KeyboardInterrupt:
        pass
