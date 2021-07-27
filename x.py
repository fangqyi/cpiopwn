#!/usr/bin/env python3

from pwn import *

PATTERN_FILE = "./patt"
CPIO_BINARY = "./cpio-2.13/src/cpio"
BLOCK_SIZE = 16384 # 1<<20
NUM_PATTERNS = 50000

cpio_cmd = f"{CPIO_BINARY} -iv -E {PATTERN_FILE} -r " + "y "*(NUM_PATTERNS-1)  # --block-size={BLOCK_SIZE}

# open a gdb session
gdb_cmd = f"gdb --args"
p = process(gdb_cmd.split() + cpio_cmd.split())

# config breakpoints
p.sendline(b'break main')
p.sendline(b'break initialize_buffers')
p.sendline(b'break read_pattern_file')
p.sendline(b'break process_copy_in')
p.sendline(b'break ds_fgetstr')
p.sendline(b'break query_rename')
p.sendline(b'break does_noth_but_break')
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
# out = p.recvuntil("New pattern")
# print(out.decode(), end='')
# print(p.recv().decode())
# p.interactive()
# p.close()
# exit()
p.interactive()