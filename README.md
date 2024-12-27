# Creating a README.md file with the provided information

readme_content = """

# Monitoring Scripts

A collection of Python scripts for monitoring system resources and Docker container status. These scripts send alerts to a Telegram chat when thresholds are exceeded or when issues are detected.

---

## Docker Status Monitoring

**Key Points:**

- **Telegram Settings**: Replace `TELEGRAM_TOKEN` and `CHAT_ID` with your bot's token and the chat ID where you want to send alerts.
- **Docker Monitoring**: Checks the status and health of all Docker containers. Sends a Telegram alert if any container is not running or unhealthy.
- **Cron Job**: The script is set to run every 5 minutes via a cron job. Update the path to the script and adjust it as needed for your system.

### Example Cron Job Configuration:

```bash
*/5 * * * * /usr/bin/python3 $HOME/monitoring/docker_monitor.py >> $HOME/monitoring/docker_monitor.log 2>&1
```

---

## Disk Space Monitoring

**Key Points:**

- **Telegram Settings**: Replace `TELEGRAM_TOKEN` and `CHAT_ID` with your bot’s token and the chat ID where alerts should be sent.
- **Disk Usage Monitoring**: Monitors the root filesystem (`/`) and calculates disk usage percentage and available free space in gigabytes.
- **Threshold Alerts**: Sends a Telegram alert when disk usage exceeds predefined thresholds (85%, 90%, or 95%). Alerts include server hostname, IP address, disk usage percentage, free space, and the exceeded threshold.
- **Alert Deduplication**: Ensures that alerts for a specific threshold are sent only once until the disk usage drops below the threshold.
- **Alert Reset**: Automatically removes a threshold from the alert list if disk usage decreases below that threshold.
- **Interval Checking**: The script checks disk usage every 60 seconds in an infinite loop for continuous monitoring.
- **Logging**: Prints “Checking disk space…” to the console for visual feedback during execution.
- **Error Handling**: Handles errors during Telegram message sending and gracefully stops execution when interrupted by the user (e.g., via `Ctrl+C`).
- **Cron Job**: Includes an example cron job configuration to run the script every 5 minutes.

### Example Cron Job Configuration:

```bash
*/5 * * * * /usr/bin/python3 $HOME/monitoring/disk_monitor.py >> $HOME/monitoring/disk_monitor.log 2>&1
```

---

## Prerequisites

1. **Python 3.6+** is required to run these scripts.
2. Install required libraries using pip:
   ```bash
   pip install psutil requests
   ```

---

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/monitoring-scripts.git
   cd monitoring-scripts
   ```

2. Update the `TELEGRAM_TOKEN` and `CHAT_ID` in both scripts with your bot’s token and the chat ID for notifications.

3. Make the scripts executable:

   ```bash
   chmod +x docker_monitor.py disk_monitor.py
   ```

4. (Optional) Add the cron job configurations to automate execution.

---

## Contribution

Feel free to contribute by creating a pull request or opening an issue for suggestions or bug fixes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
"""

# Writing the content to a README.md file

with open("README.md", "w") as file:
file.write(readme_content)

"README.md file has been created successfully."
