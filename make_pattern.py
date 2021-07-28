#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print("Usage: ./make_pattern.py [pattern_size]")
    print(f"Smallest to make max chunk size is {1090519038//2+1}.")
    exit()
else:
    p = int(sys.argv[1])

file = open("patt", "w")
longstr = "y"*p

file.write(longstr)
file.write("\n")
# file.write(longstr)
file.write("AAAA")
file.write("\n")
file.close()