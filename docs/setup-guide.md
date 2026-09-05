# Hướng dẫn cài đặt

## 1. Cài pfSense + Suricata

### 1.1. Cài pfSense
- Tải pfSense CE 2.7.2
- Tạo máy ảo với RAM 4GB, CPU 2 cores, disk 20GB
- Cài pfSense, cấu hình WAN/LAN

### 1.2. Cài Suricata
- Vào **Services > Suricata**
- Bật Suricata trên interface LAN/WAN
- Bật **EVE JSON Log** và chọn **FILE**
- Bật các rule trong **emerging-scan.rules**

## 2. Cài Splunk Enterprise
- Tải Splunk Enterprise 9.3.1
- Cài trên Ubuntu Server 22.04
- Khởi động Splunk: `sudo /opt/splunk/bin/splunk start --accept-license`
- Đặt username/password

## 3. Cấu hình Data Input trên Splunk

### 3.1. Tạo Data Input UDP 1514
- Vào **Settings > Data inputs > UDP > New**
- Port: `1514`
- Source type: `suricata`
- Index: `main`
- Click **Save**

### 3.2. Cấu hình TA-suricata
Copy file `props.conf` và `transforms.conf` vào `/opt/splunk/etc/apps/TA-suricata-master/local/`
```bash
cp configs/splunk/props.conf /opt/splunk/etc/apps/TA-suricata-master/local/
cp configs/splunk/transforms.conf /opt/splunk/etc/apps/TA-suricata-master/local/
```

## 4. Cấu hình syslog-ng trên pfSense
- Mở file `/usr/local/etc/syslog-ng.conf`
- Cấu hình theo nội dung trong `configs/pfsense/syslog-ng.conf`
- Khởi động lại syslog-ng: `service syslog-ng restart`

## 5. Cấu hình Alert trên Splunk

### 5.1. Tạo Alert
- Vào **Settings > Searches, reports, and alerts > New Alert**
- Title: `Scan Attack Detected`
- Alert type: `Scheduled`
- Cron: `*/5 * * * *`
- Time Range: `Last 5 minutes`
- SPL: index=main sourcetype=suricata event_type=alert (signature="SCAN" OR category="Scan")
       | table _time, src_ip, dest_ip, dest_port, proto, signature, category, severity_id, action, dvc
       | sort - _time

### 5.2. Trigger Actions
- Add to Triggered Alerts
- Send email
- Telegram Alert (Custom Alert Action)

## 6. Cấu hình Telegram

### 6.1. Tạo Bot Telegram
- Tìm `@BotFather` trên Telegram
- Gửi `/newbot` và làm theo hướng dẫn
- Lưu token

### 6.2. Lấy Chat ID
- Gửi tin nhắn đến bot
- Gọi API: `https://api.telegram.org/bot<TOKEN>/getUpdates`
- Lấy `chat_id` từ response

### 6.3. Cài script Telegram
- Copy `telegram_alert.py` vào `/opt/splunk/etc/apps/search/bin/`
- Cấu hình `alert_actions.conf` trong `/opt/splunk/etc/apps/search/local/`

### 6.4. Cấu hình biến môi trường
- Tạo file `.env` trong `/opt/splunk/etc/apps/search/bin/`
- Thêm token và chat_id thật

## 7. Kiểm tra
- Chạy `nmap -sS 192.168.1.131`
- Kiểm tra alert trên Telegram   
