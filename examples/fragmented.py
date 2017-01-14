#!/usr/bin/python

from __future__ import print_function
import btrfs
import sys

vaddr = int(sys.argv[1])
fs = btrfs.FileSystem(sys.argv[2])
block_group = fs.block_group(vaddr)

nodesize = fs.fs_info().nodesize
tree = btrfs.ctree.EXTENT_TREE_OBJECTID
min_key = btrfs.ctree.Key(vaddr, 0, 0)
max_key = btrfs.ctree.Key(vaddr + block_group.length, 0, 0) - 1
end_prev = 0
fragments = -1
for header, _ in btrfs.ioctl.search(fs.fd, tree, min_key, max_key):
    if header.type == btrfs.ctree.EXTENT_ITEM_KEY:
        length = header.offset
    elif header.type == btrfs.ctree.METADATA_ITEM_KEY:
        length = nodesize
    else:
        continue
    end = header.objectid + length
    if end != end_prev:
        fragments = fragments + 1
    end_prev = end

print(fragments)
