<img width="898" height="371" alt="Screenshot from 2026-11-01 15-13-12" src="https://github.com/user-attachments/assets/3cbec51b-5181-4764-93b5-c3d782d82a04" />
<img width="232" height="177" alt="Screenshot from 2026-11-01 15-17-25" src="https://github.com/user-attachments/assets/fb47f96a-3ef5-4202-9402-724f413ef001" />

-->lỗi format string

#### NOTE:Trong file 32 bit lỗi format string sẽ bắt đầu đếm từ esp ngay trước khi call hàm lỗi thật sự (ở đây là hàm warnx)

Let's Exploit 

1 Leak libc base
- gửi payload %71$p vào để lấy giá trị tại esp+0x11c (ngay trước khi call warnx)
- lấy được libc base và system base
2 ghi đè got warn
- dung %hn để ghi đè vào warn

<img width="810" height="308" alt="image" src="https://github.com/user-attachments/assets/541e293d-6e2e-4492-b640-959905277515" />

3 gửi /bin/sh
- gửi /bin/sh vào buffer để đén khi thực hiện warn thì nó sẽ trỏ ngay vào /bin/sh
<img width="810" height="308" alt="image" src="https://github.com/user-attachments/assets/70f5ca27-44fb-4d66-aa6c-0dec1779623c" />

