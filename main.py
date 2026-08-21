import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import os
from pyrogram import Client, filters
import google.generativeai as genai
import random
import time
from flask import Flask
from threading import Thread

# 1. Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
GEMINI_API_KEY = os.environ.get('GEMINI_KEY', 'YOUR_GEMINI_API_KEY_HERE')
GROUP_ID = os.environ.get('GROUP_ID', '-100123456789')

OWNER_DM_LINK = "https://t.me/YOUR_USERNAME"  
GROUP_LINK = "https://t.me/YOUR_GROUP_LINK"       
BAD_WORDS = ['badword1', 'porn', 'sex', 'xxx', 'chutiya'] 

TOPICS = [
    "Hey everyone! What's the most interesting thing you learned today?",
    "If you could travel anywhere in the world right now, where would you go?",
    "What's your favorite hobby or way to relax?",
    "Does anyone have any cool tech tips or tricks to share today?",
    "What's a movie or show you'd recommend to everyone here?",
    "If you could have dinner with any famous person, who would it be?"
]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Pyrogram Bot Setup (As per your screenshot)
app_bot = Client(
    "ai_mod_bot",
    api_id=int(os.environ.get("API_ID", "123456")), # Put your Telegram API ID here
    api_hash=os.environ.get("API_HASH", "YOUR_API_HASH"),
    bot_token=TELEGRAM_BOT_TOKEN
)

# Flask server for UptimeRobot (24/7 Active)
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def auto_topic_starter():
    while True:
        time.sleep(3600)  # Waits for 1 hour
        random_topic = random.choice(TOPICS)
        try:
            app_bot.send_message(int(GROUP_ID), f"💡 **Topic of the hour:** {random_topic}")
        except Exception as e:
            print(f"Error sending topic: {e}")

# --- Handlers for Pyrogram ---
@app_bot.on_message(filters.command(["start", "help"]))
async def send_welcome(client, message):
    await message.reply_text("I'm your AI Bot! I keep the group active and answer your questions. 🤖")

@app_bot.on_message(filters.text & ~filters.private)
async def handle_group_messages(client, message):
    text_lower = message.text.lower()
    
    # 1. Bad Words Check
    if any(word in text_lower for word in BAD_WORDS):
        try:
            await message.delete()
            return
        except:
            pass

    # 2. Owner Info
    if any(word in text_lower for word in ['owner', 'admin']):
        await message.reply_text(f"Contact Owner: {OWNER_DM_LINK}\nJoin Group: {GROUP_LINK}")
        return

    # 3. AI Response
    try:
        response = model.generate_content(message.text)
        await message.reply_text(response.text)
    except Exception as e:
        print(f"AI Error: {e}")

if __name__ == "__main__":
    # Start Keep-Alive thread
    t1 = Thread(target=run)
    t1.start()
    
    # Start Auto-Topic thread
    t2 = Thread(target=auto_topic_starter)
    t2.start()
    
    # Run Pyrogram Bot
    app_bot.run()
    
