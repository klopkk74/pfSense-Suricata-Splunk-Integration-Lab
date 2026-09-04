# Kiến trúc hệ thống

## Sơ đồ tổng quan

Kali Linux (192.168.187.130)
    │ (nmap scan)
    ▼
pfSense (192.168.1.1) + Suricata (IDS/IPS)
    │ (syslog-ng)
    ▼
Splunk Server (192.168.1.138)
    │ (Alert → Telegram)
    ▼
Telegram Bot (@splunk_alert_NVK_bot)

## Giải thích luồng dữ liệu

1. Kali Linux chạy `nmap -sS 192.168.1.131` (tấn công scan)
2. Suricata trên pfSense phát hiện và ghi log vào `/var/log/suricata/suricata_*/eve.json`
3. Syslog-ng đọc file và gửi log đến Splunk qua UDP 1514
4. Splunk parse JSON, lưu vào index `main`
5. Alert "Scan Attack Detected" chạy mỗi 5 phút
6. Khi có kết quả, Trigger Actions gửi email và Telegram
7. Telegram Bot gửi tin nhắn đến Chat ID đã cấu hình

## Các thành phần chính

| Thành phần | Vai trò |
|------------|---------|
| pfSense | Tường lửa, gateway, chạy Suricata |
| Suricata | IDS/IPS phát hiện tấn công scan |
| Syslog-ng | Chuyển tiếp log từ pfSense đến Splunk |
| Splunk | Thu thập, lưu trữ, phân tích log |
| Telegram Bot | Gửi cảnh báo tự động |