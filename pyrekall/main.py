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
parser.add_argument('-M', '--mft', dest='mft', action='store_true', help="list MFT entries")
parser.add_argument('-F', '--files', dest='files', action='store_true', help="list files")
parser.add_argument('-D', '--drivers', dest='drivers', action='store_true', help="list drivers")
parser.add_argument('--service-descriptors', dest='ssdt', action='store_true', help="list service descriptor table contents")
parser.add_argument('-T', '--threads', dest='threads', action='store_true', help="list threads")
parser.add_argument('--tokens', dest='tokens', action='store_true', help="list tokens")
parser.add_argument('--unlinked-dlls', dest='unlinked_dlls', action='store_true', help="list unlinked DLLs")
parser.add_argument('--kernel-modules', dest='kernel_modules', action='store_true', help="list loaded kernel modules")
parser.add_argument('--kernel-timers', dest='kernel_timers', action='store_true', help="list loaded kernel timers")


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
        args.mft,
        args.files,
        args.drivers,
        args.ssdt,
        args.connections,
        args.threads,
        args.tokens,
        args.unlinked_dlls,
        args.kernel_modules,
        args.kernel_timers
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

        if args.mft:
            result['mft'] = [x.summary() for x in sample.get_mft()]
        
        if args.files:
            result['files'] = [x.summary() for x in sample.get_files()]
        
        if args.drivers:
            result['drivers'] = [x.summary() for x in sample.get_drivers()]
        
        if args.ssdt:
            result['ssdt'] = [x.summary() for x in sample.get_ssdt()]
        
        if args.threads:
            result['threads'] = [x.summary() for x in sample.get_threads()]

        if args.tokens:
            result['tokens'] = [x.summary() for x in sample.get_tokens()]
        
        if args.unlinked_dlls:
            result['unlinked_dlls'] = [x.summary() for x in sample.get_unlinked_dlls()]
        
        if args.kernel_modules:
            result['kernel_modules'] = [x.summary() for x in sample.get_kernel_modules()]
        
        if args.kernel_timers:
            result['kernel_timers'] = [x.summary() for x in sample.get_kernel_timers()]

    if args.quiet:
        sys.exit(0)
    elif args.pretty_print:
        pprint.pprint(result)
    else:
        print(result)
