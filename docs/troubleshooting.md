# Xử lý sự cố thường gặp

> **Lưu ý**: Đây là các lỗi phổ biến trong quá trình cài đặt và vận hành hệ thống. Nếu gặp lỗi khác, vui lòng kiểm tra log tương ứng.

---

## 1. Splunk không nhận log Suricata

**Lỗi**: Splunk không hiển thị log Suricata, hoặc index `main` trống.

**Kiểm tra**:
- Data Input: **Settings > Data inputs > UDP > 1514** (đảm bảo Status = Enabled)
- Syslog-ng đang chạy:
  
 ```bash
  ps aux | grep syslog-ng
 ```

- File `eve.json` có dữ liệu:

 ```bash
  tail -f /var/log/suricata/suricata_em046693/eve.json
 ```

- Cấu hình syslog-ng:

 ```bash
  cat /usr/local/etc/syslog-ng.conf
 ```

---

## 2. Log Suricata không parse được

**Lỗi**: Log hiển thị trong Splunk nhưng không tách được trường (`src_ip`, `dest_ip`, `alert.signature`...).

**Kiểm tra**:
- `props.conf`:

 ```bash
  KV_MODE = json
 ```

- `transforms.conf`: REGEX cắt header syslog
- Kiểm tra `_raw` trong Splunk:

 ```bash
  index=main sourcetype=suricata | head 1 | table _raw
 ```

---

## 3. Telegram không gửi được tin nhắn

**Lỗi**: Alert kích hoạt nhưng không có tin nhắn Telegram.

**Kiểm tra**:
- Token và chat_id trong file `.env`
- Chạy thử script Python:

 ```bash
  python3 /opt/splunk/etc/apps/search/bin/telegram_alert.py
 ```
- Kiểm tra `alert_actions.conf`:
 ```bash
  cat /opt/splunk/etc/apps/search/local/alert_actions.conf
 ```

- Kiểm tra log Splunk:
 ```bash
  sudo tail -f /opt/splunk/var/log/splunk/splunkd.log | grep -i telegram
 ```

---

## 4. Thời gian hiển thị sai

**Lỗi**: Thời gian trong alert Telegram lệch so với thực tế.

**Giải pháp**:
- Cộng thêm 7 giờ (UTC+7) trong script Python
- Hoặc cấu hình Time Zone trong Splunk Preferences

---

## 5. Suricata không tạo alert

**Lỗi**: Đã tấn công nhưng không thấy alert trong `eve.json` hoặc Splunk.

**Kiểm tra**:
- File `eve.json`:

 ```bash
  tail -f /var/log/suricata/suricata_em046693/eve.json
 ```

- Suricata đang chạy:

 ```bash
  ps aux | grep suricata
 ```

- Rule Suricata đã bật: **Services > Suricata > Rules**
- Chế độ: IDS (phát hiện) hay IPS (ngăn chặn)

---

## 6. Lỗi cổng 5140 trên syslog-ng

**Lỗi**:
- Error binding socket; addr='AF_INET(<pfsense_IP>:5140)'

- **Giải pháp**: Đổi cổng thành 5141 trong cấu hình syslog-ng

---

## 7. Splunk không khởi động được

**Lỗi**: `splunk start` báo lỗi permission hoặc không chạy.

**Kiểm tra**:
- Quyền sở hữu thư mục Splunk:

 ```bash
  ls -la /opt/splunk
 ```
- Chạy với quyền phù hợp:

 ```bash
  sudo /opt/splunk/bin/splunk start --accept-license
 ```
- Kiểm tra log:

 ```bash
  tail -50 /opt/splunk/var/log/splunk/splunkd.log
 ```

---

## 8. Alert không kích hoạt dù có log

**Lỗi**: Log có trong Splunk nhưng Alert không chạy.

**Kiểm tra**:
- Cron schedule: */5 * * * *
- Time Range: Last 5 minutes
- Trigger condition: Number of Results > 0
- SPL có đúng không (chạy thử trên Search)
- Alert có bị disable không: **Settings > Searches, reports, and alerts**

---

## 9. Rule Suricata không match

**Lỗi**: Đã bật rule nhưng không có alert.

**Kiểm tra**:
- Rule đã được enable chưa (dấu tick xanh)
- Rule có yêu cầu dấu ; hoặc điều kiện đặc biệt không
- Traffic có đi qua interface WAN không
- Kiểm tra eve.json có ghi nhận traffic không

---

## 10. Syslog-ng không gửi log đi

**Lỗi**: Syslog-ng chạy nhưng Splunk không nhận được log.

**Kiểm tra**:
- Kết nối UDP 1514 từ pfSense đến Splunk:

 ```bash
  nc -zvu <Splunk_IP> 1514
 ```
- Firewall trên Splunk có chặn UDP 1514 không
- Cấu hình destination trong syslog-ng có đúng IP không
- Restart syslog-ng:
  service syslog-ng restart

---

## 11. Telegram bot không phản hồi

**Lỗi**: Bot không gửi tin nhắn dù đã cấu hình đúng.

**Kiểm tra**:
- Token có đúng không (thử gọi API):

 ```bash
  curl https://api.telegram.org/bot<TOKEN>/getMe
 ```

- Chat ID có đúng không
- Bot đã được thêm vào nhóm chưa
- Kiểm tra log Splunk:

 ```bash
  sudo tail -f /opt/splunk/var/log/splunk/splunkd.log | grep -i telegram
 ```
---

## 12. Suricata bị quá tải, bỏ sót gói

**Lỗi**: Tấn công mạnh nhưng Suricata không phát hiện.

**Giải pháp**:
- Giảm tốc độ tấn công (dùng --interval thay vì --flood)
- Tăng tài nguyên cho pfSense (RAM, CPU)
- Kiểm tra packet loss:

 ```bash
  netstat -I em0 -w 1
 ```
- Bật chế độ IPS nếu cần chặn

---

## 13. Splunk Free hết hạn

**Lỗi**: Splunk báo hết hạn license.

**Giải pháp**:
- Chuyển sang Splunk Free (giới hạn 500MB/ngày)
- Hoặc xin Developer License (6 tháng, 10GB/ngày)
- Không thể tạo tài khoản mới để gia hạn

---

## 14. Lỗi kết nối giữa các máy ảo

**Lỗi**: Không ping được giữa các máy ảo.

**Kiểm tra**:
- Chế độ mạng VMware: NAT, Bridged, Host-only
- IP các máy có cùng dải không
- Firewall trên pfSense có chặn không
- Kiểm tra route:

 ```bash
  ip route
 ```

---

## 15. Alert gửi quá nhiều tin nhắn trùng lặp

**Lỗi**: Cùng một cuộc tấn công nhưng nhận nhiều tin nhắn.

**Giải pháp**:
- Sử dụng alert.category thay vì alert.signature trong message
- Thêm throttle trong Alert:

 ```bash
  Throttle: 60 seconds
 ```
- Gom nhóm theo bin _time span=5m trong SPL

---

## Tổng kết

| # | Lỗi | Nguyên nhân chính |
|---|-----|-------------------|
| 1 | Splunk không nhận log | Data Input, syslog-ng |
| 2 | Log không parse | props.conf, transforms.conf |
| 3 | Telegram không gửi | Token, chat_id, script |
| 4 | Thời gian sai | Timezone |
| 5 | Suricata không alert | Rule, interface |
| 6 | Lỗi cổng 5140 | syslog-ng config |
| 7 | Splunk không khởi động | Permission |
| 8 | Alert không kích hoạt | Cron, SPL |
| 9 | Rule không match | Điều kiện rule |
| 10 | Syslog-ng không gửi | Kết nối UDP |
| 11 | Bot không phản hồi | Token, chat_id |
| 12 | Suricata quá tải | Tốc độ tấn công |
| 13 | Splunk hết hạn | License |
| 14 | Lỗi kết nối máy ảo | Chế độ mạng |
| 15 | Alert trùng lặp | Thiếu throttle |
