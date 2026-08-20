import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client, filters
import requests
from flask import Flask
from threading import Thread

# 24/7 uptime setup (ZENIX setup)
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

# Bot Credentials
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "7610806090:AAEF1XxQi-6jInaY8ZbB_3HR4BhIEcGr6Z0"
app = Client("sk_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
LINK = "https://t.me/+ZJDUfVhCpco1ZDA1"

# Link protection toggle status (Default: Active)
link_protection_active = True

# AI Chat Function (Nova bot style)
def ask_ai(prompt):
    try:
        url = f"https://api.popcat.xyz/chatbot?msg={requests.utils.quote(prompt)}&owner=SK&botname=SKBot"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data.get("response", "I didn't get that, bro. Say it again!")
    except:
        pass
    return "My brain is a bit busy right now, bro. Let's talk in a bit! 😎"

@app.on_message(filters.all)
async def handler(client, message):
    global link_protection_active
    if not message.from_user or message.from_user.is_self: return
    
    # 1. Private (DM) Chat
    if message.chat.type.name == "PRIVATE":
        await message.reply_text(f"Welcome, bro! 👍\nClick here to join the group: {LINK}")
        return

    text = message.text.lower() if message.text else ""

    # 2. Command System (Rose Bot style)
    # Lock Links Command: /locklink or /blocklink
    if text in ["/locklink", "/blocklink"]:
        link_protection_active = True
        await message.reply_text("🔒 Link protection is now **ENABLED** in the group! No unauthorized links allowed.")
        return

    # Unlock Links Command: /unlocklink
    if text in ["/unlocklink"]:
        link_protection_active = False
        await message.reply_text("🔓 Link protection is now **DISABLED**. Links are allowed now.")
        return

    # 3. Link Protection Check (Deletes links if active)
    if link_protection_active and any(x in text for x in ["http", "t.me", "www."]) and LINK not in text:
        try:
            await message.delete()
            await message.reply_text(f"🚫 {message.from_user.mention}, sending links is not allowed here!")
        except: 
            pass
        return

    # 4. Greetings and Reactions
    try:
        if any(word in text for word in ["hi", "hello", "hii", "hey"]):
            await message.react("👍")
            await message.reply_text(f"Hello! {message.from_user.mention} 😊 How can I help you today?")
            return
        elif any(word in text for word in ["salam", "assalam"]):
            await message.react("❤️")
            await message.reply_text(f"Walaikum Assalam Warahmatullahi Wabarakatuh! {message.from_user.mention} 🙏")
            return
        elif any(word in text for word in ["kaise ho", "kya haal", "how are you"]):
            await message.react("🔥")
            await message.reply_text(f"I am doing great, bro! How about you? 😎 {message.from_user.mention}")
            return
    except:
        pass

    # 5. Group AI Chat (When someone tags or replies to the bot)
    me = await client.get_me()
    is_mentioned = me.username and me.username.lower() in text
    is_reply = message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == me.id

    if is_mentioned or is_reply:
        clean_text = text.replace(f"@{me.username.lower()}", "").strip()
        if clean_text:
            await message.react("✍️")
            ai_reply = ask_ai(clean_text)
            await message.reply_text(ai_reply)

if __name__ == "__main__":
    keep_alive()
    app.run()
        
