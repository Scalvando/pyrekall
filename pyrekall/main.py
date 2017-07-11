#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from pyrekall.models.sample import Sample
import argparse
import logging
import pprint
import sys
import json

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
parser.add_argument('--ssdt', dest='ssdt', action='store_true', help="list service descriptor table contents")
parser.add_argument('-T', '--threads', dest='threads', action='store_true', help="list threads")
parser.add_argument('--tokens', dest='tokens', action='store_true', help="list tokens")
parser.add_argument('--unlinked', dest='unlinked_dlls', action='store_true', help="list unlinked DLLs")
parser.add_argument('--kmodules', dest='kernel_modules', action='store_true', help="list loaded kernel modules")
parser.add_argument('--ktimers', dest='kernel_timers', action='store_true', help="list loaded kernel timers")
parser.add_argument('-R', '--registry', dest='registry_keys', action='store_true', help="list registry keys")
parser.add_argument('--shimcache', dest='shimcache', action='store_true', help="list shimcache entries")
parser.add_argument('--dnscache', dest='dns_cache', action='store_true', help='list DNS records')
parser.add_argument('--symlinks', dest='symlinks', action='store_true', help='list symlink objects')
parser.add_argument('-I', '--imports', dest='importfunc', action='store_true', help='list imported functions')
parser.add_argument('-H', '--hidden', dest='hiddenproc', action='store_true', help='list hidden processes')

parser.add_argument('-P', '--processes', dest='processes', action='store_true', help='list running processes')
parser.add_argument('--include-handles', dest='include_handles', action='store_true', help='include handles in process summaries')
parser.add_argument('--include-dlls', dest='include_dlls', action='store_true', help='include DLL dependencies in process summaries')

parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help="don't print a JSON object at the end" )
parser.add_argument('--pretty-print', dest='pretty_print', action='store_true', help='pretty print the CLI output')
parser.add_argument('--human-readable', dest='human_readable', action='store_true',
                    help='use human readable representations of integers where applicable (e.g. 128868 → 126MiB )')
parser.add_argument('-j', '--json', dest='json', action='store_true', help='output as JSON')
parser.add_argument('-o', '--output', type=argparse.FileType('w+'), dest='output', help='output file path')

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
        args.kernel_timers,
        args.registry_keys,
        args.shimcache,
        args.dns_cache,
        args.symlinks,
        args.importfunc,
        args.hiddenproc
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
            result['user'] = list(map(lambda x: x.summary(), sample.get_users()))

        if args.processes:
            result['process'] = list(map(lambda x: x.summary(), sample.get_processes()))

        if args.services:
            result['service'] = list(map(lambda x: x.summary(), sample.get_services()))

        if args.connections:
            result['connection'] = [x.summary() for x in sample.get_connections()]

        if args.mft:
            result['mft_entry'] = [x.summary() for x in sample.get_mft()]
        
        if args.files:
            result['pooled_file'] = [x.summary() for x in sample.get_files()]
        
        if args.drivers:
            result['driver'] = [x.summary() for x in sample.get_drivers()]
        
        if args.ssdt:
            result['ssdt_entry'] = [x.summary() for x in sample.get_ssdt()]
        
        if args.threads:
            result['thread'] = [x.summary() for x in sample.get_threads()]

        if args.tokens:
            result['token'] = [x.summary() for x in sample.get_tokens()]
        
        if args.unlinked_dlls:
            result['unlinked_dll'] = [x.summary() for x in sample.get_unlinked_dlls()]
        
        if args.kernel_modules:
            result['kernel_module'] = [x.summary() for x in sample.get_kernel_modules()]
        
        if args.kernel_timers:
            result['kernel_timer'] = [x.summary() for x in sample.get_kernel_timers()]
        
        if args.registry_keys:
            result['registry_key'] = sample.get_registry_keys().summary()
        
        if args.shimcache:
            result['shimcache_entry'] = [x.summary() for x in sample.get_shimcache()]

        if args.dns_cache:
            result['dns_cache'] = list(map(lambda x: x.summary(), sample.get_dns_cache()))
        
        if args.symlinks:
            result['symlink'] = list(map(lambda x: x.summary(), sample.get_symlinks()))

        if args.importfunc:
            result['imported_function'] = list(map(lambda x: x.summary(), sample.get_importfunc()))

        if args.hiddenproc:
            result['hidden_process'] = list(map(lambda x: x.summary(), sample.get_hiddenproc()))


    if args.quiet:
        sys.exit(0)
    elif args.pretty_print:
        pprint.pprint(result)
    elif args.json:
        with open(args.output.name, 'w+') as f:
            for artifact in result:
                for item in result[artifact]:
                    item['_type'] = artifact

                    if 'creation_time' in item:
                        item['timestamp'] = item['creation_time']
                    elif 'last_modified' in item:
                        item['timestamp'] = item['last_modified']
                    elif 'last_write' in item:
                        item['timestamp'] = item['last_write']
                    else:
                        item['timestamp'] = '1970-01-01T00:00:00Z'
                    f.write('{}\n'.format(json.dumps(item)))
    else:
        print(result)
