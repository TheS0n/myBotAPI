import os
import asyncio
from threading import Thread
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ---------- متغیرهای محیطی ----------
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

# ---------- Telethon client ----------
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=[CHANNEL_ID]))
async def handler(event):
    text = event.message.message or ""
    await client.send_message("me", f"📢 پست جدید:\n\n{text}")
    print("پیام به Saved Messages فرستاده شد ✅")

# ---------- Flask app برای healthcheck ----------
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running ✅", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)

# ---------- اجرای همزمان Flask و Telethon ----------
async def start_telethon():
    await client.start()
    print("Telethon started")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Flask در یک thread جداگانه ران شود
    Thread(target=run_flask, daemon=True).start()
    # Telethon در main thread asyncio اجرا شود
    asyncio.get_event_loop().run_until_complete(start_telethon())
