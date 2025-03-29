import psutil
import time
import requests
import socket

# Telegram settings
TELEGRAM_TOKEN = ""
CHAT_ID = ""

# Threshold values in percentage
THRESHOLDS = [85, 90, 95]

# Storage for sent alerts
sent_alerts = set()

# Function to send messages to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

# Main monitoring function
def monitor_disk_space():
    global sent_alerts
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    while True:
        disk_usage = psutil.disk_usage('/')
        used_percent = disk_usage.percent
        free_space_gb = disk_usage.free / (1024 ** 3)  # Convert to gigabytes

        for threshold in THRESHOLDS:
            if used_percent >= threshold and threshold not in sent_alerts:
                message = (f"⚠️ <b>Disk Space Alert</b>\n"
                           f"Server: {hostname} ({ip_address})\n"
                           f"Used: {used_percent}%\n"
                           f"Free Space: {free_space_gb:.2f} GB\n"
                           f"Threshold: {threshold}%")
                send_telegram_message(message)
                sent_alerts.add(threshold)

        # Remove sent alerts if usage is below the threshold
        for threshold in list(sent_alerts):
            if used_percent < threshold:
                sent_alerts.remove(threshold)

        print("Checking disk space...")  # For logging and visual feedback
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    try:
        monitor_disk_space()
    except KeyboardInterrupt:
        print("Script terminated by user")

test