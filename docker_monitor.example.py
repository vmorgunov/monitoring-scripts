import docker
import requests
import socket
#finale test

# Telegram settings
TELEGRAM_TOKEN = ""
CHAT_ID = ""

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
        "chat_id": CHAT_ID,
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

            # If the container is not running, send a message
            if container_status != "running":
                message = (
                    f"⚠️ <b>Docker Container Alert</b>\n"
                    f"Server IP: <b>{server_ip}</b>\n"
                    f"Container: <b>{container_name}</b>\n"
                    f"Status: <b>{container_status}</b>\n"
                )
                send_telegram_message(message)

    except Exception as e:
        print(f"Error monitoring containers: {e}")

if __name__ == "__main__":
    monitor_docker_containers()