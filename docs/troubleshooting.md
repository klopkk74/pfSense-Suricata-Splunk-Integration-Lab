# Xử lý sự cố thường gặp

## 1. Splunk không nhận log Suricata
- Kiểm tra Data Input: **Settings > Data inputs > UDP > 1514** (đảm bảo Status = Enabled)
- Kiểm tra syslog-ng: `ps aux | grep syslog-ng`
- Kiểm tra file eve.json: `tail -f /var/log/suricata/suricata_em046693/eve.json`
- Kiểm tra cấu hình syslog-ng: `cat /usr/local/etc/syslog-ng.conf`

## 2. Log Suricata không parse được
- Kiểm tra `props.conf`: `KV_MODE = json`
- Kiểm tra `transforms.conf`: REGEX cắt header syslog
- Kiểm tra `_raw` trong Splunk: `index=main sourcetype=suricata | head 1 | table _raw`

## 3. Telegram không gửi được tin nhắn
- Kiểm tra token và chat_id trong file `.env`
- Kiểm tra script Python: `python3 /opt/splunk/etc/apps/search/bin/telegram_alert.py`
- Kiểm tra `alert_actions.conf`: `cat /opt/splunk/etc/apps/search/local/alert_actions.conf`
- Kiểm tra log Splunk: `sudo tail -f /opt/splunk/var/log/splunk/splunkd.log | grep -i telegram`

## 4. Thời gian hiển thị sai
- Cộng thêm 7 giờ (UTC+7) trong script Python
- Hoặc cấu hình Time Zone trong Splunk Preferences

## 5. Suricata không tạo alert
- Kiểm tra file `eve.json`: `tail -f /var/log/suricata/suricata_em046693/eve.json`
- Kiểm tra Suricata đang chạy: `ps aux | grep suricata`
- Kiểm tra rule Suricata đã bật: **Services > Suricata > Rules**
- Kiểm tra chế độ: IDS (phát hiện) hay IPS (ngăn chặn)

## 6. Lỗi cổng 5140 trên syslog-ng
- Lỗi: `Error binding socket; addr='AF_INET(192.168.1.1:5140)'`
- Giải pháp: Đổi cổng thành 5141 trong cấu hình syslog-ng