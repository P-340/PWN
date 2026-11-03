I BUG

<img width="480" height="270" alt="image" src="https://github.com/user-attachments/assets/9e11e624-48cf-46b4-9e2e-f79f6c45cdfa" />

-xuất hiện bug buffer overflow
-ta quyết định sử dụng srop do thiếu các gadget cần thiết khi ta chỉ có pop rax,syscall 
II Idea
read /bin/sh lên stack --> chạy execve(/bin/sh) với rdi đang giữ vị trí stack 
III Exploit
1 read /bin/sh lên stack
<img width="815" height="546" alt="image" src="https://github.com/user-attachments/assets/96a6dc1a-72ed-40d6-9d40-92b5c066a558" />
gửi payload sao cho 0x0f rơi đúng ở dưới phần pop rax để rax lấy được giá trị 0x0f(syscall srop)
<img width="815" height="546" alt="image" src="https://github.com/user-attachments/assets/4a318701-2226-4dda-bf8f-f2399261981b" />
<img width="815" height="546" alt="image" src="https://github.com/user-attachments/assets/c5b3cb80-f626-4756-85cf-41eba91e46dc" />

sử dụng SigreturnFrame để đưa các giá trị vào stack khi syscall(15) được gọi 
đưa stack tiếp theo là bss 
```python
frame = SigreturnFrame(arch='amd64')
frame.rsp = 0x601028 
frame.rip =  syscall 
frame.rax= 0 
frame.rdi = 0
frame.rsi= 0x601028
frame.rdx= 0x1000
```
2 chạy execve(/bin/sh) 
đầu tiên ghi tiếp pop rax lên trước (sau khi syscall thì sẽ là pop rax)
<img width="815" height="546" alt="image" src="https://github.com/user-attachments/assets/39764277-3276-4740-9671-ef53e35a9d52" />

tiếp tục đưa 0x0f vào rax và dùng frame
