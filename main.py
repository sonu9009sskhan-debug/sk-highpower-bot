import asyncio
import random
from pyrogram import Client, filters

# Asyncio loop fix as per your requirement
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Credentials (Get api_id & api_hash from my.telegram.org)
API_ID = 1234567  
API_HASH = "your_api_hash"
BOT_TOKEN = "7610806090:AAG3BtpM8XHkf9cpo0HzecQZ0j536MzbKw8"

app = Client("my_ai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Your Links
DM_LINK = "https://t.me/SK_KING_CHILL"
GROUP_LINK = "https://t.me/SK_Chatting_Club"

# List of emojis to react automatically
REACTIONS = ["👍", "❤️", "🔥", "⚡", "👏", "🎉"]

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! I am your AI Group Manager and Reaction Bot. 🤖")

# Anti-link system (Deletes links automatically)
@app.on_message(filters.regex(r'https?://\S+') & ~filters.me)
async def block_links(client, message):
    try:
        await message.delete()
        await message.reply_text("⚠️ Links are not allowed in this group!")
    except Exception as e:
        print(f"Error deleting link: {e}")

# Main AI Chat, DM/Group Links & Auto Reaction System
@app.on_message(filters.text & ~filters.command("start"))
async def ai_and_links_handler(client, message):
    text = message.text.lower()
    
    # 1. Automatic Emoji Reaction on incoming messages
    try:
        random_emoji = random.choice(REACTIONS)
        await message.set_reaction(random_emoji)
    except Exception as e:
        print(f"Reaction error (Make sure bot is admin): {e}")

    # 2. DM Link Response
    if "dm" in text or "message" in text or "inbox" in text:
        await message.reply_text(f"Contact me directly here:\n👉 {DM_LINK}")
    
    # 3. Group Link Response
    elif "group" in text or "link" in text or "join" in text:
        await message.reply_text(f"Join our official group here:\n👉 {GROUP_LINK}")
    
    # 4. Hi / Hello Response
    elif "hello" in text or "hi" in text or "hey" in text:
        await message.reply_text("Hello! 😊 How can I help you today?")
    
    # 5. AI Style Smart Reply (General fallback)
    else:
        # Here you can plug in OpenAI/Gemini API response if needed
        await message.reply_text(f"🤖 I heard that: \"{message.text}\". I'm processing your request!")

print("Bot is running smoothly with AI, Links, and Reactions...")
app.run()
        
