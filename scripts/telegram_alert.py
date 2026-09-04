#!/usr/bin/env python3
import sys, json, urllib.request
from datetime import datetime, timedelta
import os

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set", file=sys.stderr)
    sys.exit(1)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as response:
        return response.read()

def format_time(time_val):
    try:
        if isinstance(time_val, (int, float)):
            dt = datetime.fromtimestamp(time_val) + timedelta(hours=7)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(time_val, str) and time_val.replace('.', '').isdigit():
            dt = datetime.fromtimestamp(float(time_val)) + timedelta(hours=7)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        try:
            dt = datetime.strptime(time_val, '%Y-%m-%dT%H:%M:%S.%f%z')
            if dt.tzinfo is not None:
                dt = dt.astimezone().replace(tzinfo=None)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return time_val
    except:
        return str(time_val)

if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        result = input_data.get('result', {})

        src_ip = result.get('src_ip', 'N/A')
        dest_ip = result.get('dest_ip', 'N/A')
        dest_port = result.get('dest_port', 'N/A')
        signature = result.get('signature', 'Unknown')
        severity_raw = result.get('severity_id', 'N/A')
        dvc = result.get('dvc', 'N/A')

        try:
            severity = int(severity_raw)
        except:
            severity = 'N/A'
        severity_map = {1: "🔴 CRITICAL", 2: "🟠 HIGH", 3: "🟡 MEDIUM"}
        severity_text = severity_map.get(severity, f"Severity: {severity_raw}")

        time_val = result.get('_time', 'N/A')
        formatted_time = format_time(time_val)

        message = f"""🚨 SCAN ATTACK DETECTED

Time   : {formatted_time}
Source : {src_ip}
Target : {dest_ip}:{dest_port}
Type   : {signature}
Risk   : {severity_text}
Device : pfSense"""

        send_telegram(message)
    except Exception as e:
        send_telegram(f"❌ Error: {str(e)}")