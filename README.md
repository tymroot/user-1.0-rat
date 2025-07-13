![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2B-lightgrey)

# user

**user** is a multifunctional Python-based remote access and control system that enables full interaction with a Windows machine through a Discord bot.  
Designed for persistent, stealthy execution, it offers extensive functionality for system monitoring, command automation, and environment control.

The tool is structured for reliability and performance under Windows environments, running silently in the background after initiation.

---

## Key Features

- File locking and unlocking with AES encryption
- Screenshot and webcam capture
- System reboot trigger
- Keystroke logging
- Public and local IP discovery
- Native Windows alert/message boxes
- System process termination (explorer.exe, svchost.exe)
- Self-persistence via watchdog + temp injection
- Fully controlled over Discord text commands

---

## Requirements (Windows only)

### 1. Python Setup

Ensure Python 3.10 or above is installed on the system.  
Download it from: https://www.python.org/downloads/windows/

### 2. Required Libraries

Install all dependencies with:

```bash
pip install -r requirements.txt
