from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

# تحميل الإعدادات من config.json
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = "7947209199:AAFOKlozQ0Ht4lwYuf-1RTbL-peFQ1mPILg"

# الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📥 أضف قناة", "🎵 أضف موسيقى"],
        ["🎬 اطلب فيديو الآن", "🛑 أوقف البوت"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("مرحبًا بك في بوت ملخصات الأفلام 🎥", reply_markup=reply_markup)

# نقطة البداية
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
