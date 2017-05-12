#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from pyrekall.models.sample import Sample
import argparse
import logging
import pprint
import sys

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'), help="the name of the memory sample to use")

parser.add_argument('-A', '--all', dest='all', action='store_true', help='list everything of interest')
parser.add_argument('-X', '--sample', dest='sample', action='store_true', help="list high-level information about the memory sample")
parser.add_argument('-S', '--services', dest='services', action='store_true', help="list running services")
parser.add_argument('-U', '--users', dest='users', action='store_true', help="list users")
parser.add_argument('-C', '--connections', dest='connections', action='store_true', help="list connections")

parser.add_argument('-P', '--processes', dest='processes', action='store_true', help='list running processes')
parser.add_argument('--include-handles', dest='include_handles', action='store_true', help='include handles in process summaries')
parser.add_argument('--include-dlls', dest='include_dlls', action='store_true', help='include DLL dependencies in process summaries')

parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help="don't print a JSON object at the end" )
parser.add_argument('--pretty-print', dest='pretty_print', action='store_true', help='pretty print the CLI output')
parser.add_argument('--human-readable', dest='human_readable', action='store_true',
                    help='use human readable representations of integers where applicable (e.g. 128868 → 126MiB )')

args = parser.parse_args()


if __name__ == "__main__":
    if not any([
        args.all,
        args.sample,
        args.services,
        args.processes,
        args.users,
        args.connections
    ]):
        parser.print_help()
        sys.exit(1)

    result = {}
    sample = Sample(path=args.file.name)
    sample.flags['human_readable'] = args.human_readable
    sample.flags['include_dlls'] = args.include_dlls
    sample.flags['include_handles'] = args.include_handles

    if args.all:
        result = sample.summary(all=args.all)
    else:
        if args.sample:
            result['sample'] = sample.summary(all=args.all)

        if args.users:
            result['users'] = list(map(lambda x: x.summary(), sample.get_users()))

        if args.processes:
            result['processes'] = list(map(lambda x: x.summary(), sample.get_processes()))

        if args.services:
            result['services'] = list(map(lambda x: x.summary(), sample.get_services()))

        if args.connections:
            result['connections'] = [x.summary() for x in sample.get_connections()]

    if args.quiet:
        sys.exit(0)
    elif args.pretty_print:
        pprint.pprint(result)
    else:
        print(result)
