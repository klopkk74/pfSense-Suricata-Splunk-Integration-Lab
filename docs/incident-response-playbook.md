# QUY TRÌNH ỨNG PHÓ SỰ CỐ

## PHA 1: PHÁT HIỆN VÀ PHÂN TÍCH

- Nhận cảnh báo từ Telegram (Splunk Alert) với các thông tin: thời gian, IP nguồn, IP đích, loại sự kiện, signature.

- Truy vấn Splunk để lấy log chi tiết:
  index=* sourcetype=suricata src_ip=<IP> OR dest_ip=<IP>

- Xác định false positive:
  - Kiểm tra IP nguồn có nằm trong danh sách trắng (IP nội bộ, công cụ quét hợp pháp, đối tác tin cậy) không.
  - Đối chiếu với lịch sử hoạt động và ngữ cảnh hệ thống.

- Phân loại mức độ nghiêm trọng:
  * Low: Không có dấu hiệu tấn công thành công, có thể là false positive.
  * Medium: Có dấu hiệu tấn công nhưng chưa xâm nhập thành công.
  * High: Tấn công đã xâm nhập hoặc có nguy cơ ảnh hưởng nghiêm trọng.
  * Critical: Hệ thống bị chiếm quyền, dữ liệu bị lộ, hoặc dịch vụ bị gián đoạn.

- Ghi nhận thông tin cơ bản vào ticket: thời gian, IP, loại sự kiện, mức độ, hành động dự kiến.


## PHA 2: NGĂN CHẶN

- Thực hiện ngăn chặn tạm thời:
  - Chặn IP nguồn trên pfSense.
  - Cách ly máy chủ bị ảnh hưởng.
  - Khóa tài khoản bị xâm nhập.
  - Giới hạn tốc độ hoặc áp dụng rate limiting.

- Ghi nhận hành động và thời gian thực hiện.
- Thông báo cho các bên liên quan.


## PHA 3: ĐIỀU TRA VÀ LOẠI BỎ

- Thu thập chứng cứ: log Splunk, log hệ thống, snapshot, dữ liệu mạng.
- Xác định nguyên nhân gốc rễ của sự cố.
- Loại bỏ nguyên nhân sự cố:
  - Xóa mã độc hoặc tệp tin độc hại.
  - Đóng lỗ hổng bảo mật.
  - Thu hồi quyền truy cập trái phép.
  - Khắc phục cấu hình sai.
- Xác nhận đã loại bỏ thành công.


## PHA 4: PHỤC HỒI VÀ GIÁM SÁT

- Phục hồi hệ thống về trạng thái hoạt động bình thường.
- Khởi động lại các dịch vụ bị tạm dừng.
- Dỡ bỏ các biện pháp ngăn chặn tạm thời sau khi xác nhận an toàn.
- Giám sát tăng cường trong 24-48 giờ sau sự cố.


## PHA 5: BÁO CÁO VÀ CẢI TIẾN

- Viết báo cáo sự cố bao gồm:
  - Thời gian phát hiện và kết thúc sự cố.
  - Nguyên nhân gốc rễ.
  - Các hành động đã thực hiện.
  - Kết quả và bài học kinh nghiệm.
- Đề xuất cải tiến cho hệ thống và quy trình.
- Lưu báo cáo vào hệ thống quản lý sự cố.
