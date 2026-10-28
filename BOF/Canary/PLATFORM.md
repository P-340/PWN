# STACK CANARY

<img width="1164" height="53" alt="image" src="https://github.com/user-attachments/assets/f0b440f4-01ba-4f49-93bf-c40b2ab9d777" />

stack canary là chuỗi giá trị 8-byte ngẫu nhiên , được gọi là stack canary hoặc cookie, nằm ngay trước địa chỉ trả về (return address) đã lưu — nghĩa là, nằm sau các biến cục bộ và trước con trỏ khung cơ sở (base pointer) rbp cùng với địa chỉ trả về.

<img width="814" height="427" alt="image" src="https://github.com/user-attachments/assets/29086708-032c-4662-a154-526ed333072d" />

Trước khi kết thúc và trả về từ một hàm, chương trình sẽ kiểm tra xem giá trị canary có bị thay đổi hay không. Nếu có, điều đó cho thấy nhiều khả năng đã xảy ra một cuộc tấn công phá hủy stack (stack smashing), và chương trình sẽ đột ngột dừng lại (abort) để ngăn chặn việc bị khai thác. Để hỗ trợ đa luồng, trình biên dịch sẽ lưu trữ giá trị canary trong Khối điều khiển luồng (Thread Control Block - TCB), nhờ đó mỗi luồng sẽ có một giá trị ngẫu nhiên riêng biệt. Giá trị canary này được truy cập thông qua thanh ghi segment fs trên các hệ thống Linux kiến trúc x86_64.

<img width="1000" height="269" alt="image" src="https://github.com/user-attachments/assets/83de00b9-40e8-4a39-bd6d-fca5bd40c1b3" />

Trình biên dịch thường tạo ra các đoạn mã để lấy giá trị canary thông qua lệnh mov %fs:0x28, %rax, đẩy nó lên stack bằng lệnh mov %rax, -0x8(%rbp). Sau đó, trước khi trả về (return), chương trình sẽ so sánh giá trị hiện tại với giá trị gốc ban đầu; nếu không khớp, chương trình sẽ gọi hàm __stack_chk_fail@plt, dẫn đến việc tiến trình bị hủy bỏ (abort). Tất nhiên, nếu kẻ tấn công sở hữu sẵn giá trị canary (ví dụ do các lỗi rò rỉ bộ nhớ như lỗi định dạng chuỗi - format string vulnerabilities), cơ chế này hoàn toàn có thể bị vô hiệu hóa.
