#!/usr/bin/python

from __future__ import print_function
import btrfs
import sys

filename = sys.argv[1]
print(btrfs.crc32c.name_hash(filename))
