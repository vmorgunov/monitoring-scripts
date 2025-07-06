import requests
import docker
import socket
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Telegram settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Function to get the server's IP address
def get_server_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception:
        return "Unable to determine IP"

# Function to send messages to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

# Main function to monitor containers
def monitor_docker_containers():
    client = docker.from_env()
    server_ip = get_server_ip()

    try:
        containers = client.containers.list(all=True)

        for container in containers:
            container_name = container.name
            container_status = container.status
            container_health = container.attrs.get("State", {}).get("Health", {}).get("Status", "healthy")

            # If the container is not running or not healthy, send a message
            if container_status != "running" or container_health != "healthy":
                message = (
                    f"⚠️ <b>Docker Container Alert</b>\n"
                    f"Server IP: <b>{server_ip}</b>\n"
                    f"Container: <b>{container_name}</b>\n"
                    f"Status: <b>{container_status}</b>\n"
                    f"Health: <b>{container_health}</b>\n"
                )
                send_telegram_message(message)

    except Exception as e:
        print(f"Error monitoring containers: {e}")

if __name__ == "__main__":
    monitor_docker_containers()