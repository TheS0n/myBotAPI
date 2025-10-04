import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# متغیرهای محیطی
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH"))
SESSION_STRING = os.environ.get("SESSION")  # Session String
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))  # numeric channel id

# ساخت کلاینت با Session String
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=[CHANNEL_ID]))
async def handler(event):
    text = event.message.message or ""
    await client.send_message("me", f"📢 پست جدید از کانال:\n\n{text}")
    print("پیام به Saved Messages فرستاده شد ✅")

print("ربات ران شد...")
client.start()
client.run_until_disconnected()
