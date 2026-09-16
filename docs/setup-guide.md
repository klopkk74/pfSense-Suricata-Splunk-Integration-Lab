# HƯỚNG DẪN CÀI ĐẶT

> **Lưu ý**: File này chỉ tập trung vào cài đặt và cấu hình. Tham khảo thêm:
> - [Kiến trúc hệ thống](architecture.md)
> - [Yêu cầu hệ thống](../README.md)
> - [Xử lý lỗi thường gặp](troubleshooting.md)
> - [Quy trình ứng phó](incident-response-playbook.md)
> - [Cấu hình máy ảo](../lab-setup/vmware-settings.md)

---

## MỤC LỤC

1. [Cài đặt pfSense](#1-cài-đặt-pfsense)
2. [Cài đặt Suricata](#2-cài-đặt-suricata)
3. [Cài đặt Splunk Enterprise](#3-cài-đặt-splunk-enterprise)
4. [Cấu hình Syslog-ng](#4-cấu-hình-syslog-ng)
5. [Cấu hình Data Input trên Splunk](#5-cấu-hình-data-input-trên-splunk)
6. [Cấu hình Alert trên Splunk](#6-cấu-hình-alert-trên-splunk)
7. [Cấu hình Telegram](#7-cấu-hình-telegram)

---

## 1. CÀI ĐẶT PFSENSE

### 1.1. Tải pfSense CE 2.7.2

Tải file ISO từ trang chủ: https://www.pfsense.org/download/

### 1.2. Tạo máy ảo trên VMware

Tham chiếu cấu hình chi tiết tại: [`lab-setup/vmware-settings.md`](../lab-setup/vmware-settings.md)

Cấu hình tối thiểu: RAM 4 GB, CPU 2 cores, Disk 20 GB, 2 card mạng (WAN: Bridged, LAN: VMnet1).

### 1.3. Cài đặt pfSense

- Cài từ file ISO, chọn phân vùng mặc định.
- Cấu hình WAN (DHCP hoặc IP tĩnh) và LAN (<pfsense_IP>/24).
- Đặt mật khẩu admin.

### 1.4. Cấu hình ban đầu

- Truy cập https://<pfsense_IP>, chạy Setup Wizard.
- Cấu hình hostname, domain, DNS, WAN/LAN interface.

---

## 2. CÀI ĐẶT SURICATA

### 2.1. Cài đặt Suricata trên pfSense

- Vào System > Package Manager > Available Packages, tìm và cài Suricata.

### 2.2. Cấu hình Suricata

- Vào Services > Suricata, thêm interface WAN.
- Bật EVE JSON Log (chọn FILE), chọn chế độ IDS.

### 2.3. Bật rule phát hiện tấn công

Vào Services > Suricata > WAN Categories, bật các rule:
- emerging-scan.rules
- emerging-dos.rules
- emerging-web_server.rules

### 2.4. Cập nhật rule

Vào Services > Suricata > Updates, nhấn Update Rules.

### 2.5. Khởi động Suricata

Vào Services > Suricata > Interfaces, nhấn Play để khởi động trên WAN.

---

## 3. CÀI ĐẶT SPLUNK ENTERPRISE

### 3.1. Tải Splunk Enterprise

Tải từ: https://www.splunk.com/en_us/download/splunk-enterprise.html

### 3.2. Cài đặt trên Ubuntu Server 22.04

```bash
cd /tmp
tar -xvzf splunk-10.4.2-*.tgz -C /opt
sudo /opt/splunk/bin/splunk start --accept-license
```

### 3.3. Bật khởi động cùng hệ thống

```bash
sudo /opt/splunk/bin/splunk enable boot-start
```

---

## 4. CẤU HÌNH SYSLOG-NG

### 4.1. Copy file cấu hình

File cấu hình mẫu: configs/pfsense/syslog-ng.conf

Copy file vào pfSense:

```bash
scp configs/pfsense/syslog-ng.conf admin@<pfsense_IP>:/usr/local/etc/syslog-ng.conf
```

### 4.2. Khởi động lại Syslog-ng

```bash
service syslog-ng restart
```

---

## 5. CẤU HÌNH DATA INPUT TRÊN SPLUNK

### 5.1. Tạo UDP Data Input

- Vào Settings > Data inputs > UDP > New Local UDP.
- Cấu hình Port 1514, Source type suricata, Index main.

### 5.2. Cấu hình TA-suricata

- Cài app TA-suricata từ Splunkbase: https://splunkbase.splunk.com/app/3946
- Copy file cấu hình:

```bash
cp configs/splunk/props.conf /opt/splunk/etc/apps/TA-suricata-master/local/
cp configs/splunk/transforms.conf /opt/splunk/etc/apps/TA-suricata-master/local/
```

- Khởi động lại Splunk:

```bash
sudo /opt/splunk/bin/splunk restart
```

---

## 6. CẤU HÌNH ALERT TRÊN SPLUNK

### 6.1. Tạo Alert phát hiện Scan

- Vào Settings > Searches, reports, and alerts > New Alert.
- Title: Scan Attack Detected
- Alert type: Scheduled, Cron: */5 * * * *, Time Range: Last 5 minutes.
- SPL:
  
```bash
index=main sourcetype=suricata event_type=alert
(
    alert.category="Detection of a Network Scan" OR
    alert.category="Attempted Information Leak" OR
    alert.signature="*SCAN*" OR
    alert.signature="*Scan*" OR
    alert.signature="*scan*" OR
    alert.signature="*Nmap*" OR
    alert.signature="*Nikto*" OR
    alert.signature="*Masscan*" OR
    alert.signature="*Zmap*" OR
    alert.signature="*Portscan*" OR
    alert.signature="*Port Scan*" OR
    alert.signature="*SYN Scan*" OR
    alert.signature="*XMAS*" OR
    alert.signature="*NULL Scan*" OR
    alert.signature="*FIN Scan*" OR
    alert.signature="*ACK Scan*" OR
    alert.signature="*UDP Scan*" OR
    alert.signature="*Suspicious inbound*" OR
    alert.signature="*Suspicious outbound*"
)
NOT (
    alert.category="Attempted Denial of Service" OR
    alert.signature="*DOS*" OR
    alert.signature="*DDoS*" OR
    alert.signature="*Flood*" OR
    alert.signature="*Brute*" OR
    alert.signature="*Login*" OR
    alert.signature="*Auth*" OR
    alert.category="*Trojan*" OR
    alert.category="*Malware*" OR
    alert.category="*Policy*" OR
    alert.signature="*Exfiltration*"
)
| eval Attack_Type = case(
    match(alert.signature, "(?i)nmap"), "Nmap Scan",
    match(alert.signature, "(?i)nikto"), "Nikto Scan",
    match(alert.signature, "(?i)masscan"), "Masscan Scan",
    match(alert.signature, "(?i)zmap"), "Zmap Scan",
    match(alert.signature, "(?i)syn scan"), "SYN Scan",
    match(alert.signature, "(?i)xmas"), "XMAS Scan",
    match(alert.signature, "(?i)null scan"), "NULL Scan",
    match(alert.signature, "(?i)fin scan"), "FIN Scan",
    match(alert.signature, "(?i)ack scan"), "ACK Scan",
    match(alert.signature, "(?i)udp scan"), "UDP Scan",
    match(alert.signature, "(?i)portscan|port scan"), "Port Scan",
    match(alert.signature, "(?i)suspicious inbound"), "Suspicious Inbound Scan",
    match(alert.signature, "(?i)suspicious outbound"), "Suspicious Outbound Scan",
    match(alert.signature, "(?i)scan"), "Generic Scan",
    true(), "Other Scan"
)
| table _time, src_ip, dest_ip, dest_port, Attack_Type, alert.signature, alert.category, alert.severity, proto, dvc, action
| sort -_time
```

### 6.2. Tạo Alert phát hiện DDoS

- Title: DDoS Attack Detected
- Alert type: Scheduled, Cron: */5 * * * *, Time Range: Last 5 minutes.
- SPL:
  
```bash
index=main sourcetype=suricata event_type=alert
(
    alert.category="Attempted Denial of Service" OR
    alert.signature="*SYN Flood*" OR
    alert.signature="*UDP Flood*" OR
    alert.signature="*ICMP Flood*" OR
    alert.signature="*DoS*" OR
    alert.signature="*DDoS*"
)
NOT (
    alert.signature="*SCAN*" OR
    alert.category="*Scan*" OR
    alert.signature="*Brute*" OR
    alert.signature="*Login*" OR
    alert.signature="*Auth*" OR
    alert.signature="*Vulnerability*" OR
    alert.signature="*Nessus*" OR
    alert.signature="*OpenVAS*" OR
    alert.category="*Trojan*" OR
    alert.category="*Malware*" OR
    alert.signature="*Exfiltration*" OR
    alert.signature="*Data Loss*" OR
    alert.category="*Policy*" OR
    alert.signature="*POLICY*"
)
| eval Attack_Type = case(
    match(alert.signature, "(?i)syn flood"), "SYN Flood",
    match(alert.signature, "(?i)udp flood"), "UDP Flood",
    match(alert.signature, "(?i)icmp"), "ICMP Flood",
    match(alert.signature, "(?i)dos"), "DoS Attack",
    true(), "Other DDoS"
)
| table _time, src_ip, dest_ip, dest_port, Attack_Type, alert.signature, alert.category, alert.severity, proto, dvc, action
| sort -_time
```

### 6.3. Tạo Alert phát hiện SQL Injection

- Title: SQL Injection Detected
- Alert type: Scheduled, Cron: */5 * * * *, Time Range: Last 5 minutes.
- SPL:

```bash
index=main sourcetype=suricata event_type=alert
(
    alert.signature="*SQL Injection*" OR
    alert.signature="*UNION*SELECT*" OR
    alert.signature="*SELECT*FROM*" OR
    alert.signature="*Blind SQL*" OR
    alert.signature="*Time-based SQL*" OR
    alert.signature="*Error-based SQL*" OR
    (alert.category="Web Application Attack" AND alert.signature="*SQL*")
)
NOT (alert.signature="*SCAN*" OR alert.category="*Scan*")
| eval Attack_Type = case(
    match(alert.signature, "(?i)union.*select"), "UNION SELECT Injection",
    match(alert.signature, "(?i)select.*from"), "SELECT FROM Injection",
    match(alert.signature, "(?i)blind"), "Blind SQL Injection",
    match(alert.signature, "(?i)time-based"), "Time-based SQL Injection",
    match(alert.signature, "(?i)error-based"), "Error-based SQL Injection",
    match(alert.signature, "(?i)sql injection"), "SQL Injection",
    true(), "Other SQL Attack"
)
| table _time, src_ip, dest_ip, dest_port, Attack_Type, alert.signature, alert.category, alert.severity, proto, dvc, action
| sort -_time
```

---

## 7. CẤU HÌNH TELEGRAM

### 7.1. Tạo Bot Telegram

- Tìm @BotFather trên Telegram, gửi /newbot, lưu token.

### 7.2. Lấy Chat ID

- Gửi tin nhắn đến bot, gọi API:
  https://api.telegram.org/bot<TOKEN>/getUpdates
- Lấy chat_id từ response.

### 7.3. Cài script Telegram

```bash
cp scripts/telegram_alert.py /opt/splunk/etc/apps/search/bin/
chmod +x /opt/splunk/etc/apps/search/bin/telegram_alert.py
```
### 7.4. Cấu hình biến môi trường

- Tạo file .env trong /opt/splunk/etc/apps/search/bin/ với nội dung:

```bash
TELEGRAM_BOT_TOKEN=<Telegram_token>
TELEGRAM_CHAT_ID=<Telegram_chat_id>
```

### 7.5. Cấu hình alert_actions.conf

- File cấu hình mẫu: configs/splunk/alert_actions.conf

- Copy file vào: /opt/splunk/etc/apps/search/local/alert_actions.conf

### 7.6. Khởi động lại Splunk

```bash
sudo /opt/splunk/bin/splunk restart --run-as-root
```

---

## XỬ LÝ LỖI

- Nếu gặp lỗi, tham khảo: troubleshooting.md
