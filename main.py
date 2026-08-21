import os
import telebot
import google.generativeai as genai
import random
import time
from flask import Flask
from threading import Thread

# 1. Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
GEMINI_API_KEY = os.environ.get('GEMINI_KEY', 'YOUR_GEMINI_API_KEY_HERE')
GROUP_ID = os.environ.get('GROUP_ID', '-100123456789') # Put your Group ID here

OWNER_DM_LINK = "https://t.me/YOUR_USERNAME"  
GROUP_LINK = "https://t.me/YOUR_GROUP_LINK"       
BAD_WORDS = ['badword1', 'porn', 'sex', 'xxx', 'chutiya'] 

# List of conversation starters
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
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Flask for UptimeRobot
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Function to send random topics automatically
def auto_topic_starter():
    while True:
        time.sleep(3600)  # Waits for 1 hour (3600 seconds)
        random_topic = random.choice(TOPICS)
        try:
            bot.send_message(GROUP_ID, f"💡 **Topic of the hour:** {random_topic}")
        except Exception as e:
            print(f"Error sending topic: {e}")

# --- Handlers ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "I'm your AI Bot! I keep the group active and answer your questions. 🤖")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_type = message.chat.type
    
    # 1. Moderation (Only in Groups)
    if chat_type in ['group', 'supergroup']:
        if message.text:
            text_lower = message.text.lower()
            if any(word in text_lower for word in BAD_WORDS):
                bot.delete_message(message.chat.id, message.message_id)
                return

    # 2. Owner Info
    if message.text and any(word in message.text.lower() for word in ['owner', 'admin']):
        bot.reply_to(message, f"Contact Owner: {OWNER_DM_LINK}\nJoin Group: {GROUP_LINK}")
        return

    # 3. AI Response
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"AI Error: {e}")

if __name__ == "__main__":
    # Start Keep-Alive thread
    t1 = Thread(target=run)
    t1.start()
    
    # Start Auto-Topic thread
    t2 = Thread(target=auto_topic_starter)
    t2.start()
    
    bot.infinity_polling()
    
