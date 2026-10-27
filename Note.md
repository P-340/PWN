# các lỗi hay gặp khi chơi 
1 Lỗi căn chỉnh 16 bit 

-Trước khi call, bắt buộc rsp phải chia hết cho 16 bytes ,nếu không thì các lệnh tối ưu bên trong thư viện C (như movaps ) sẽ cố gắng nạp vào thanh ghi 16 bytes và bắn ngay ra lỗi SIGSEGV
<img width="813" height="278" alt="image" src="https://github.com/user-attachments/assets/abd3ad67-2f14-4ec5-a84d-c4490fa8cd26" />

- giải pháp : đặt thêm 1 thằng ret ở rip (ví dụ ngay trước get_shell) để căn chỉnh rsp
