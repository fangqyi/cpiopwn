#!/usr/bin/env python3

file = open("patt", "w")
longstr = "y"*(1090519038//2+1)

file.write(longstr)
file.write("\n")
file.write(longstr)
file.close()