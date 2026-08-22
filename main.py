asyncio.get_event_loop()
except RuntimeError:
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
# ============================================================

# GitHub पर सुरक्षित रखने के लिए Environment Variables का उपयोग करें
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7610806090:AAG3BtpM8XHkf9cpo0HzecQZ0j536MzbKw8")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")

genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel("gemini-1.5-flash")

app = Client(
    "sk_highpower_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN
)

DM_LINK = "https://t.me/SK_KING_CHILL"
GROUP_LINK = "https://t.me/SK_Chatting_Club"
REACTIONS = ["👍", "❤️", "🔥", "⚡", "👏", "🎉"]


@app.on_message(filters.command("start"))
async def start(client, message):
  await message.reply_text(
      "Hello! I am your AI Group Manager powered by Gemini. 🤖✨"
  )


@app.on_message(filters.regex(r"https?://\S+") & ~filters.me)
async def block_links(client, message):
  try:
    await message.delete()
    await message.reply_text("⚠️ Links are not allowed in this group!")
  except Exception as e:
    print(f"Error deleting link: {e}")


@app.on_message(filters.text & ~filters.command("start"))
async def ai_and_links_handler(client, message):
  text = message.text.lower()
  user_message = message.text

  try:
    random_emoji = random.choice(REACTIONS)
    await message.set_reaction(random_emoji)
  except Exception as e:
    print(f"Reaction error: {e}")

  if "dm" in text or "message" in text or "inbox" in text:
    await message.reply_text(f"Contact me directly here:\n👉 {DM_LINK}")
  elif "group" in text or "link" in text or "join" in text:
    await message.reply_text(f"Join our official group here:\n👉 {GROUP_LINK}")
  elif "hello" in text or "hi" in text or "hey" in text:
    await message.reply_text("Hello! 😊 How can I help you today?")
  else:
    try:
      response = ai_model.generate_content(user_message)
      await message.reply_text(response.text)
    except Exception as e:
      print(f"Gemini API Error: {e}")
      await message.reply_text("🤖 Sorry, I am having trouble thinking right now!")
