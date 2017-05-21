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
parser.add_argument('file', type=argparse.FileType('r'), help="The path to the memory sample")
args = parser.parse_args()


if __name__ == "__main__":
    sample = Sample(path=args.file.name)
    process = sample.get_process_by_name("System")
    for handle in process.get_handles():
        pass