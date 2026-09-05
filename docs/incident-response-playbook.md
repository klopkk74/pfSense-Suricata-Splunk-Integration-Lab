# Quy trình ứng phó sự cố

## Pha 1: Phát hiện và Phân tích

- Nhận alert trên Telegram: Khi Splunk phát hiện sự kiện bất thường, hệ thống tự động gửi thông báo qua Telegram đến đội ngũ SOC. Thông báo bao gồm thời gian, IP nguồn, IP đích, loại tấn công và mức độ cảnh báo. Người trực SOC xác nhận đã nhận và bắt đầu xử lý.

- Truy vấn Splunk: Nhà phân tích thực hiện truy vấn để lấy log chi tiết:
  index=main sourcetype=suricata src_ip=<IP> OR dest_ip=<IP>
  Mục đích là xác định bối cảnh sự cố, các kết nối trước và sau thời điểm phát sinh cảnh báo.

- Xác định false positive: Kiểm tra IP nguồn có nằm trong danh sách trắng (IP nội bộ, công cụ quét lỗ hổng, đối tác đã xác thực) không. Đối chiếu với lịch sử hoạt động và ngữ cảnh tổ chức để xác định đây là tấn công thật hay cảnh báo giả.

- Đánh giá mức độ:
  * Medium: Scan từ IP lạ, chưa có dấu hiệu xâm nhập thành công.
  * High: Scan kèm theo đăng nhập thành công, tài khoản bị khóa bất thường, hoặc thay đổi hệ thống không rõ nguyên nhân.

## Pha 2: Ngăn chặn

- Tạo rule block trên pfSense: Truy cập pfSense Web UI, vào Firewall > Rules, chọn WAN, thêm rule Block với Source là IP nguồn. Mục đích ngăn chặn ngay lập tức các kết nối tiếp theo từ IP độc hại.

- Ghi nhận hành động: Lưu ID sự cố, thời gian, IP bị chặn, loại rule, người thực hiện để phục vụ báo cáo và tránh xử lý trùng lặp.

## Pha 3: Loại bỏ

- Kiểm tra máy chủ mục tiêu: Đăng nhập vào máy chủ để kiểm tra log đăng nhập, tiến trình lạ, file thay đổi gần đây, lịch sử lệnh. Mục đích xác định kẻ tấn công đã xâm nhập được hay chưa.

- Xác định không có dấu hiệu xâm nhập: Kết luận khi không phát hiện user lạ, backdoor, mã độc, thay đổi cấu hình bất thường. Nếu có dấu hiệu, thu thập chứng cứ và chuyển lên cấp cao hơn.

## Pha 4: Phục hồi

- Theo dõi hệ thống sau sự cố: Giám sát trong 24-48 giờ để phát hiện hoạt động bất thường tiếp theo.

- Dỡ bỏ lệnh chặn sau 24h: Xóa rule block trên pfSense sau khi xác nhận hệ thống an toàn. Ghi nhận thời gian dỡ bỏ.

## Pha 5: Báo cáo

- Viết báo cáo sự cố: Tóm tắt thời gian, nguyên nhân, hành động đã thực hiện, kết quả. Lưu vào hệ thống quản lý sự cố.

- Đề xuất cải tiến: Điều chỉnh ngưỡng alert, cập nhật rule Suricata, cải thiện Dashboard, bổ sung IP đen.
