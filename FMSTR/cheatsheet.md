## Bảng tra cứu cờ định dạng 

    Ký tự định dạng      Cấu trúc dự liệu nhận diện       Mô tả chức năng và cơ chế lấy dự liệu 
    
    %d/%i                int(theo giá trị )               hiển thị số nguyên có dấu dưới dạng thập phân

    %u                   unsigned int (theo giá trị)      Hiển thị số nguyên không dấu dưới dạng thập phân.

    %x/%X                unsigned int` (theo giá trị)     Hiển thị giá trị nguyên dưới dạng Hexadecimal.
    
    %p                   void *                           Hiển thị giá trị con trỏ (địa chỉ bộ nhớ) dưới dạng Hexadecimal.

    %s                   char *                           Đọc và in chuỗi ASCIIZ từ địa chỉ con trỏ được trích xuất trên Stack.

    %n                   int * (theo tham chiếu)          Ghi tổng số ký tự đã xuất ra màn hình trước đó vào địa chỉ biến `int`.

    %hn                  short int * (theo tham chiếu)    Ghi số ký tự đã xuất (dạng 2 byte / short) vào địa chỉ mục tiêu.

## Mẫu vuln cơ bản
```c
// Sai (Vulnerable): int func(char \*user) { printf(user); // Người dùng kiểm soát chuỗi định dạng } // Đúng (Secure): int func(char \*user) { printf("%s", user); // Chuỗi định dạng cố định là "%s" }
```
## Mã nguồn lỗi trong thực tế 

Các hàm thuộc gia đình định dạng bao gồm `printf`, `fprintf`, `sprintf`, `snprintf`, `vprintf`, `vfprintf`, `vsprintf`, `vsnprintf`, cùng các hàm liên quan như `syslog` và `setproctitle`. Việc sử dụng sai được chia thành hai dạng chính:

* **Dạng 1 (Direct Vulnerability):** Chuỗi định dạng do người dùng cung cấp trực tiếp vào tham số hàm (như trong lỗi `rpc.statd` trên Linux hoặc `telnetd` trên IRIX).

```c
char tmpbuf[512]; snprintf(tmpbuf, sizeof(tmpbuf), "foo: %s", user); syslog(LOG\_NOTICE, tmpbuf); // Lỗi tại tham số thứ hai của syslog
```

* **Dạng 2 (Indirect Vulnerability):** Chuỗi người dùng được truyền gián tiếp qua một hàm bọc (wrapper function) tùy chỉnh (như trong `wu-ftpd` hoặc `QPOP 2.53`).

```c
int Error(char \*fmt, ...) { ... } int somefunc(char \*user) { Error(user); // Truyền gián tiếp người dùng nhập vào hàm bọc }
```
## Các thao tác khai thác cơ bản 
### 1\. Gây Crash Chương Trình (Denial of Service)

Gửi chuỗi định dạng chứa nhiều ký tự `%s` liên tiếp:

```
%s%s%s%s%s%s%s%s%s%s%s%s

```

Hàm định dạng sẽ cố gắng đọc chuỗi từ các địa chỉ ngẫu nhiên trên Stack. Khi gặp địa chỉ không hợp lệ (unmapped memory), Kernel sẽ gửi tín hiệu `SIGSEGV` làm chương trình bị chấm dứt và dump core.

### 2\. Đọc Bộ Nhớ (Memory Inspection)

* **Rút hầm Stack (Dump Stack):** Sử dụng `%08x.%08x.%08x.%08x` để in các giá trị 4-byte trên Stack từ vị trí con trỏ hiện tại đi ngược lên top của Stack.
* **Đọc địa chỉ bất kỳ (Arbitrary Memory Read):** Chèn địa chỉ mục tiêu vào đầu chuỗi định dạng, sử dụng chuỗi `%08x` để đẩy con trỏ Stack nội bộ của hàm `printf` đến đúng vị trí chuỗi định dạng, sau đó dùng `%s` để đọc nội dung tại địa chỉ đó.

```
Payload: \x10\x01\x48\x08_%08x.%08x.%08x.%08x.%08x|%s|

```

Payload trên sẽ đọc chuỗi ASCIIZ từ địa chỉ `0x08480110` cho đến khi gặp byte NUL (`\x00`).

### 3\. Ghi Bộ Nhớ Bất Kỳ (Arbitrary Memory Write)

Sử dụng đặc tả `%n` để ghi số lượng ký tự đã in vào địa chỉ chỉ định trên Stack.

#### Công thức tính toán Padding cho từng Byte

Để ghi một giá trị địa chỉ 4-byte dạng Little-Endian, kỹ thuật tiêu chuẩn là thực hiện ghi 4 lần liên tiếp (chênh lệch nhau 1 byte địa chỉ).

Công thức tính số lượng ký tự đệm (padding) cho mỗi bước ghi byte `write_byte` khi đã in `already_written` ký tự:

```c
write\_byte += 0x100 already\_written %= 0x100 padding = (write\_byte - already\_written) % 0x100 if (padding &lt; 10) padding += 0x100
```
*Lưu ý:* Việc đảm bảo `padding &gt;= 10` giúp độ rộng chuỗi xuất ra bởi cờ dạng `%nu` luôn chính xác theo tham số chiều dài chỉ định.

#### Cấu trúc chuỗi Payload ghi 4 bước (Four-stage Overwrite Payload)

Payload hoàn chỉnh trên Stack gồm 3 thành phần chính theo thứ tự:

```
[Stackpop Sequence] [Dummy-Addr Pairs * 4] [Write Code (%nu%n)]

```

1. **Stackpop Sequence:** Chuỗi các cờ `%u` hoặc `%08x` để di chuyển con trỏ Stack của hàm định dạng tới vùng địa chỉ chỉ định.
2. **Dummy-Addr Pairs:** 4 cặp địa chỉ ghi tăng dần 1 byte (kèm các byte đệm rác không chứa NUL byte).
3. **Write Code:** Các cặp `%nu%n` tương ứng để điều khiển byte thấp của bộ đếm và thực thi ghi vào địa chỉ.

## \. Kỹ Thuật Ghi Đè &amp; Mục Tiêu Thay Thế (Alternative Targets)

Thay vì chỉ tập trung ghi đè con trỏ trả về (Return Address) trên Stack vốn dễ bị thay đổi theo môi trường, việc khai thác lỗ hổng chuỗi định dạng cho phép ghi vào bất kỳ vùng nhớ có quyền ghi nào trong không gian tiến trình.

Các mục tiêu ghi đè chiến lược được tổng hợp trong bảng sau:

| Mục tiêu ghi đè                      | Vị trí / Cơ chế hoạt động                                                                | Ưu điểm khai thác                                                                                                       | Công cụ &amp; Kỹ thuật xác định           |
| ------------------------------------ | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Global Offset Table (GOT)**        | Bảng chứa địa chỉ thực của các hàm thư viện động liên kết với file nhị phân ELF.         | Địa chỉ GOT cố định theo binary, không phụ thuộc vào Stack hay Heap. Bỏ qua các cơ chế bảo vệ StackGuard / StackShield. | `objdump --dynamic-reloc binary`      |
| **Destructors (** **.dtors** **)**   | Bảng chứa các con trỏ hàm dọn dẹp được thực thi ngay trước khi tiến trình gọi `exit()`.  | Ghi đè con trỏ NULL tại offset `+4` trong bảng `.dtors` bằng địa chỉ Shellcode.                                         | Đọc bảng định dạng ELF binary.        |
| **C Library Hooks**                  | Các con trỏ hook trong GNU C Library (`__malloc_hook`, `__realloc_hook`, `__free_hook`). | Được tự động kích hoạt mỗi khi tiến trình cấp phát hoặc giải phóng bộ nhớ qua `malloc`/`free`.                          | Kiểm tra ký hiệu trong libc.          |
| **Structures** **atexit**            | Cấu trúc quản lý danh sách các hàm dọn dẹp được đăng ký để chạy khi gọi `exit`.          | Hiệu quả với các chương trình liên kết tĩnh (statically linked binaries).                                               | Phân tích cấu trúc `__atexit`.        |
| **Function Pointers &amp;** **jmp\_buf** | Các con trỏ hàm trong bảng xử lý lệnh hoặc cấu trúc nhảy `setjmp`/`longjmp`.             | Kích hoạt shellcode khi tiến trình thực thi luồng chuyển tiếp lệnh tương ứng.                                           | Phân tích mã máy / bộ nhớ tiến trình. |

### Kỹ thuật Return-into-LibC

Khi bộ nhớ Stack bị chặn quyền thi hành (Non-executable Stack / PaX patch), kẻ tấn công ghi đè địa chỉ GOT của một hàm (ví dụ `fopen`) bằng địa chỉ hàm thư viện `system()`. Khi tiến trình gọi `fopen(user_buf)`, chuỗi câu lệnh hệ thống chứa trong `user_buf` (ví dụ: `cd /tmp; cp /bin/sh .; chmod 4777 sh; exit;`) sẽ được chuyển thẳng cho `system()` thực thi.

---
## \. Biến Thể Tối Ưu Payload &amp; Khai Thác Trên Heap

### 1\. Short Write (`%hn`)

Sử dụng cờ `%hn` để ghi dữ liệu kiểu `short int` (2 byte) trong một lần ghi.

* **Cú pháp:** `printf("%.29010u%hn%.32010u%hn", 1, (short *) &amp;foo[0], 1, (short *) &amp;foo[2]);`
* **Ưu điểm:** Chỉ cần 2 lần ghi thay vì 4 lần; không làm hỏng các dữ liệu nằm liền sau địa chỉ ghi.
* **Hạn chế:** Phụ thuộc vào khả năng chịu đựng bộ đếm vượt ngưỡng của thư viện C (không tương thích libc5 cũ).

### 2\. Direct Parameter Access (`%$`)

Cho phép truy cập trực tiếp tham số thứ `n` trên Stack mà không cần chuỗi Stackpop dài.

* **Cú pháp:** `printf("%6$d\n", 6, 5, 4, 3, 2, 1);` \-&gt; In ra `1` (tham số thứ 6).
* **Payload ghi trực tiếp:** `printf("%1$16u%2$n%1$16u%3$n%1$32u%4$n%1$64u%5$n", 1, &amp;foo[0], &amp;foo[1], &amp;foo[2], &amp;foo[3]);`
* **Giới hạn nền tảng:** BSD giới hạn trong 8 tham số đầu; Solaris C Library giới hạn 30 tham số đầu.

### 3\. Khai Thác Chuỗi Định Dạng Trên Heap

Khi chuỗi định dạng nằm trên Heap thay vì Stack, con trỏ Stack của hàm `printf` không thể trỏ trực tiếp vào chính chuỗi định dạng.

* **Giải pháp 1 (Stack Buffer Intermediate):** Nếu trên Stack có một bộ đệm đầu ra (`outbuf`), in các địa chỉ mục tiêu lên `outbuf` trước, sau đó dùng các cờ `%n` truy cập địa chỉ từ `outbuf` trên Stack.
* **Giải pháp 2 (Alternative Stack Data):** Lợi dụng các trường dữ liệu khác lưu trên Stack (như trường Password trong dịch vụ FTP) để chứa dữ liệu hoặc Shellcode.

---
## \. Quy Trình Brute Force &amp; Công Cụ Hỗ Trợ

Trong trường hợp không xác định được offset chính xác của bộ nhớ, kẻ tấn công có thể áp dụng hai phương pháp Dò tìm tự động (Brute Force):

### 1\. Response-Based Brute Force (Dò tìm dựa trên phản hồi)

Áp dụng khi kẻ tấn công nhìn thấy kết quả đầu ra của hàm định dạng (ví dụ dịch vụ FTP):

1. **Đo khoảng cách (Distance):** Gửi chuỗi `AAAABBBB|stackpop|%08x|` và tăng dần số lượng `%u` cho đến khi đầu ra xuất hiện chuỗi Hex `41414141` (`AAAA`).
2. **Căn chỉnh (Alignment):** Nếu không xuất hiện mẫu `41414141`, thêm từ 1 đến 3 byte rác vào đầu chuỗi để căn chỉnh biên 4-byte.
3. **Xác định địa chỉ Buffer (Buffer Address):** Gửi `addr|stackpop|___%%|%s|`. Nếu `addr` trỏ đúng vào chuỗi đệm, kết quả sẽ in ra 2 ký tự `%` liên tiếp thay vì 1 ký tự `%`.

### 2\. Blind Brute Force (Dò tìm mù)

Áp dụng cho các tiến trình chạy ngầm (Daemon) ghi log qua `syslog` không trả phản hồi trực tiếp:

* Đo thời gian xử lý của server khi truyền các tham số tính toán lớn như `%.9999999u`.
* Tạo lỗi Segment Fault chủ động bằng cờ `%n` trỏ tới địa chỉ không hợp lệ để xác định ranh giới bộ nhớ.

### 3\. Các Công Cụ Hỗ Trợ Phân Tích

* `ltrace`: Theo dõi và ghi lại tham số của các hàm thư viện động (`printf`, `strcpy`, `syslog`), giúp tìm địa chỉ chuỗi định dạng nhanh chóng.
* `strace`: Theo dõi các lời gọi hệ thống (System Calls), hỗ trợ tìm địa chỉ các bộ đệm đọc dữ liệu đầu vào.
* `gdb`: Trình gỡ lỗi mức mã máy và mã nguồn GNU Debugger.
* `objdump`: Phân tích cấu trúc file nhị phân ELF, trích xuất địa chỉ các bảng GOT (`objdump --dynamic-reloc binary`) và các section trong bộ nhớ.
