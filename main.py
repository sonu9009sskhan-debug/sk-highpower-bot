import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
import random
from flask import Flask
from threading import Thread

# Flask (24/7)
web_app = Flask('')
@web_app.route('/')
def home():
    return "Bot is Active!"
def run_web():
    web_app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# Bot
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "7610806090:AAEF1XxQi-6jInaY8ZbB_3HR4BhIEcGr6Z0"
app = Client("sk_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
LINK = "https://t.me/+ZJDUfVhCpco1ZDA1"

@app.on_message(filters.all)
async def handler(client, message):
    if not message.from_user or message.from_user.is_self: return
    if message.chat.type.name == "PRIVATE":
        await message.reply_text(f"स्वागत है! ग्रुप लिंक: {LINK}")
        return
    text = message.text.lower() if message.text else ""
    if any(x in text for x in ["http", "t.me", "www."]) and LINK not in text:
        try:
            await message.delete()
            await message.reply_text("🚫 लिंक मना है!")
        except: pass

if __name__ == "__main__":
    keep_alive()
    app.run()
    
