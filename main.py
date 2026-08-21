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

# Flask server to keep the bot alive on Render
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is running!"

def run():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot credentials
API_ID = 1234567  
API_HASH = "your_api_hash"
BOT_TOKEN = "7610806090:AAGCMhZnwNsL2EdJyuKEucfL5ZcCiVw0Nv8"

OWNER_DM = "@SK_KING_CHILL"
GROUP_LINK = "https://t.me/SK_Chatting_Club"

# Initialize Pyrogram bot client
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Handles messages from Private chats, Groups, and Supergroups explicitly
@bot.on_message(filters.text & ~filters.command & (filters.private | filters.group | filters.supergroup))
async def handle_messages(client, message):
    user_text = message.text.lower()
    
    # Auto reaction (sending ❤️ emoji on message)
    try:
        await message.react("❤️")
    except Exception as e:
        print(f"Reaction error: {e}")

    # Check for owner or group link queries
    if "owner" in user_text or "group" in user_text or "link" in user_text:
        reply_msg = f"👑 **Owner DM:** {OWNER_DM}\n🔗 **Group Link:** {GROUP_LINK}"
        await message.reply_text(reply_msg, disable_web_page_preview=True)
    else:
        # Standard automated reply
        await message.reply_text(f"I have read your message: '{message.text}'. How can I help you with this?")

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting successfully...")
    bot.run()
