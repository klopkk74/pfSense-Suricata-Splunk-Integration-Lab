# Suricata Rules – Detection on pfSense

## NMAP Scan Detection (emerging-scan.rules)

| SID | Rule Description |
|-----|------------------|
| 2000537 | ET SCAN NMAP -sS window 2048 |
| 2000536 | ET SCAN NMAP -sO |
| 2000538 | ET SCAN NMAP -sA (1) |
| 2000540 | ET SCAN NMAP -sA (2) |
| 2000543 | ET SCAN NMAP -f -sF |
| 2000544 | ET SCAN NMAP -f -sN |
| 2000546 | ET SCAN NMAP -f -sX |
| 2008654 | ET SCAN SQLix SQL Injection |
| 2009358 | ET SCAN Nmap Scripting Engine User-Agent Detected (Nmap Scripting Engine) |
| 2009359 | ET SCAN Nmap Scripting Engine User-Agent Detected (Nmap NSE) |
| 2013778 | ET SCAN NMAP SQL Spider Scan |
| 2018489 | ET SCAN NMAP OS Detection Probe |
| 2022579 | ET SCAN MsSQL Malicious |
| 2021023 | ET SCAN Nmap NSE Heartbleed Request |
| 2021024 | ET SCAN Nmap NSE Heartbleed Response |

---

## DDoS Detection (emerging-dos.rules)

| SID | Rule Description |
|-----|------------------|
| 2019404 | ET DOS Potential Tsunami SYN Flood Denial Of Service Attempt |
| 2009701 | ET DOS DNS BIND 9 Dynamic Update DoS attempt |
| 2019102 | ET DOS Possible SSDP Amplification Scan in Progress |
| 2019018 | ET DOS Possible NTP DDoS Inbound Frequent Un-Authed PEER_LIST_SUM Requests IMPL 0x03 |
| 2019346 | ET DOS Terse HTTP GET Likely LOIC |

---

## SQL Injection Detection (emerging-web_server.rules)

| SID | Rule Description |
|-----|------------------|
| 2006445 | ET WEB_SERVER Possible SQL Injection Attempt SELECT FROM |
| 2006446 | ET WEB_SERVER Possible SQL Injection Attempt UNION SELECT |
| 2006444 | ET WEB_SERVER Possible SQL Injection Attempt INSERT INTO |
| 2006443 | ET WEB_SERVER Possible SQL Injection Attempt DELETE FROM |
| 2011042 | ET WEB_SERVER MYSQL SELECT CONCAT SQL Injection Attempt |
