# 🛡️ pfSense-Suricata-Splunk Integration Lab

## 📌 Giới thiệu
Dự án xây dựng hệ thống giám sát an ninh mạng tập trung (SOC Lab) sử dụng:
- **pfSense**: Tường lửa, gateway, chạy Suricata (IDS/IPS)
- **Suricata**: Phát hiện tấn công scan mạng
- **Splunk Enterprise**: Thu thập, lưu trữ, phân tích log
- **Telegram Bot**: Gửi cảnh báo tự động

## 🧱 Mô hình hệ thống
- **pfSense** - Hostname: `pfsense` - IP: `192.168.1.1` - Vai trò: Tường lửa, gateway, chạy Suricata
- **Suricata** - Hostname: (trên pfSense) - IP: `em0 (WAN), em1 (LAN)` - Vai trò: IDS/IPS phát hiện scan
- **Splunk Server** - Hostname: `server` - IP: `192.168.1.138` - Vai trò: Splunk Enterprise (Indexer & Search Head)
- **Ubuntu Client** - Hostname: `ubuntu-client` - IP: `192.168.1.131` - Vai trò: Máy chủ mục tiêu
- **Kali Linux** - Hostname: `kali` - IP: `192.168.187.130` - Vai trò: Máy tấn công (nmap scan)

## 🔄 Luồng dữ liệu
1. Suricata ghi log vào `/var/log/suricata/suricata_*/eve.json`
2. Syslog-ng đọc file và gửi log đến Splunk (UDP 1514)
3. Splunk parse JSON, lưu vào index `main`
4. Alert chạy mỗi 5 phút với SPL
5. Trigger Actions gửi email + Telegram
6. Telegram Bot gửi tin nhắn đến Chat ID

## 🛠️ Công cụ sử dụng
- pfSense 2.7.2
- Suricata 6.0.0
- Splunk Enterprise 9.3.1
- TA-suricata-master
- Syslog-ng 4.4
- Telegram Bot API
- Python 3.10+
- Kali Linux 2026.1 (Nmap)
- Ubuntu Server 22.04 LTS

## 📂 Cấu trúc thư mục
soc-lab-splunk-pfsense-suricata/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docs/
│   ├── architecture.md
│   ├── setup-guide.md
│   ├── incident-response-playbook.md
│   └── troubleshooting.md
├── configs/
│   ├── pfsense/
│   │   └── syslog-ng.conf
│   ├── splunk/
│   │   ├── props.conf
│   │   ├── transforms.conf
│   │   ├── alert_actions.conf
│   │   └── scan_alert.spl
│   └── suricata/
│       └── enabled_rules.txt
├── scripts/
│   └── telegram_alert.py
├── diagrams/
├── screenshots/
└── lab-setup/
    └── vmware-settings.md

## 📚 Tài liệu
- [Hướng dẫn cài đặt](docs/setup-guide.md)
- [Quy trình ứng phó sự cố](docs/incident-response-playbook.md)
- [Xử lý sự cố](docs/troubleshooting.md)

## 👨‍💻 Tác giả
- Nguyễn Văn Khánh (https://github.com/klopkk74)

## 📄 Giấy phép
MIT License