# Monitoring & Automation Scripts Collection

A collection of Python scripts for monitoring and automation, designed for DevOps, SREs, and Web3 engineers.  
Each script focuses on a specific service or integration (Discord, Docker, GitHub, disk health, etc.), and sends alerts or collects data for proactive incident response.

## Contents

- **discord-monitoring/** — Discord channel monitoring and Telegram notifications
- **disk-monitoring/** — Local disk health and usage monitoring
- **docker-monitoring/** — Docker container status & health checks, with Telegram alerts
- **github-monitoring/** — GitHub repo & commit monitoring, event logging and analytics

---

## Features

- **Cross-platform**: Scripts run on Linux/macOS/Windows (Python 3.8+)
- **Easy configuration**: Uses `.env` files for secrets & tokens (never store these in version control)
- **Plug & play**: Each module works independently

---

---

## Security

- **Never commit your real `.env` files or secrets to the repository!**
- `.gitignore` already includes `.env` patterns for safety.

---

## Contributing

Pull requests and feature suggestions are welcome!  
If you build a new monitor or integration, feel free to submit a PR.

---

## License

MIT License © 2025 VEEEM
