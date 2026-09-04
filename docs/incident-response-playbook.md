# Quy trình ứng phó sự cố

## Pha 1: Phát hiện và Phân tích
- Nhận alert trên Telegram
- Truy vấn Splunk: `index=main sourcetype=suricata src_ip=<IP> OR dest_ip=<IP>`
- Xác định false positive
- Đánh giá mức độ (Medium/High)

## Pha 2: Ngăn chặn
- Tạo rule block trên pfSense
- Ghi nhận hành động

## Pha 3: Loại bỏ
- Kiểm tra máy chủ mục tiêu
- Xác định không có dấu hiệu xâm nhập

## Pha 4: Phục hồi
- Theo dõi hệ thống sau sự cố
- Dỡ bỏ lệnh chặn sau 24h

## Pha 5: Báo cáo
- Viết báo cáo sự cố
- Đề xuất cải tiến