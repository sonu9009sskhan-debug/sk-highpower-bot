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
import requests

# --- Flask setup (24/7 Uptime) ---
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

# --- Configuration ---
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "7610806090:AAEF1XxQi-6jInaY8ZbB_3HR4BhIEcGr6Z0"
app = Client("sk_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
LINK = "https://t.me/+ZJDUfVhCpco1ZDA1"

# --- AI Toggle Variable (Default OFF) ---
ai_chat = False

# --- AI Function ---
def ask_ai(prompt):
    try:
        url = f"https://api.popcat.xyz/chatbot?msg={requests.utils.quote(prompt)}&owner=SK&botname=SKBot"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("response", "I did not understand, bro!")
    except: pass
    return "My brain is busy right now, bro!"

# --- Command Handler (Only for AI ON/OFF) ---
@app.on_message(filters.command(["ai_on", "ai_off"]))
async def command_handler(client, message):
    global ai_chat
    cmd = message.command[0]
    if cmd == "ai_on":
        ai_chat = True
        await message.reply_text("🤖 AI Chat has been ENABLED by admin.")
    elif cmd == "ai_off":
        ai_chat = False
        await message.reply_text("🤖 AI Chat has been DISABLED.")

# --- Permanent Handler (Greetings, Links & AI) ---
@app.on_message(filters.all)
async def handler(client, message):
    if not message.from_user or message.from_user.is_self: return
    text = message.text.lower() if message.text else ""

    # 1. Permanent Greetings System
    if any(w in text for w in ["assalam", "salam"]):
        await message.reply_text("Walaikum Assalam Warahmatullahi Wabarakatuh! 🙏")
        return
    elif "khuda hafiz" in text:
        await message.reply_text("Allah Hafiz! 👋")
        return
    elif "allah hafiz" in text:
        await message.reply_text("Khuda Hafiz! 👋")
        return

    # 2. Permanent Link Protection System
    if any(x in text for x in ["http", "t.me", "www."]) and LINK not in text:
        try:
            await message.delete()
            await message.reply_text(f"🚫 {message.from_user.mention}, links are not allowed here!")
        except: 
            pass
        return

    # 3. AI Chat System (Works only when /ai_on is active)
    if ai_chat:
        me = await client.get_me()
        is_mentioned = me.username and me.username.lower() in text
        is_reply = message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == me.id
        
        if is_mentioned or is_reply:
            clean_text = text.replace(f"@{me.username.lower()}", "").strip()
            if clean_text:
                await message.reply_text(ask_ai(clean_text))

if __name__ == "__main__":
    keep_alive()
    app.run()
