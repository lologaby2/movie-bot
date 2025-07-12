import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تحميل الإعدادات
CONFIG_PATH = "config.json"
CHANNELS_PATH = "channels.txt"
MUSIC_FOLDER = "music"
os.makedirs(MUSIC_FOLDER, exist_ok=True)

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {
        "daily_time": "07:00",
        "min_duration": 50,
        "max_duration": 90,
        "min_views": 2000000,
        "match_threshold": 0.10,
        "audio_volume": 1.0,
        "music_volume": 0.2,
        "auto_classify": True,
        "force_blur_subtitles": True,
        "language": "ar"
    }

bot_status = {"stopped": False}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ أضف موسيقى", callback_data="add_music")],
        [InlineKeyboardButton("📺 أضف قناة", callback_data="add_channel")],
        [InlineKeyboardButton("🎬 أنشئ فيديو الآن", callback_data="make_video")],
        [
            InlineKeyboardButton("⏹️ إيقاف البوت", callback_data="stop_bot"),
            InlineKeyboardButton("▶️ استئناف", callback_data="resume_bot")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 مرحباً! هذا بوت ملخصات الأفلام. اختر خيارًا:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if bot_status["stopped"] and query.data != "resume_bot":
        await query.edit_message_text("🚫 البوت متوقف مؤقتًا. اضغط ▶️ لاستئناف.")
        return

    if query.data == "add_music":
        await query.edit_message_text("🎵 أرسل الآن ملف الموسيقى (mp3).")
        context.user_data['awaiting_music'] = True

    elif query.data == "add_channel":
        await query.edit_message_text("📺 أرسل رابط قناة تيك توك.")
        context.user_data['awaiting_channel'] = True

    elif query.data == "make_video":
        await query.edit_message_text("⚙️ جاري معالجة الفيديو... (ميزة قيد التطوير)")
        # لاحقًا: تنفيذ الإنشاء التلقائي هنا

    elif query.data == "stop_bot":
        bot_status["stopped"] = True
        await query.edit_message_text("✅ تم إيقاف البوت مؤقتًا.")

    elif query.data == "resume_bot":
        bot_status["stopped"] = False
        await query.edit_message_text("✅ تم استئناف البوت.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_music'):
        file = await update.message.audio.get_file()
        file_path = os.path.join(MUSIC_FOLDER, f"{file.file_id}.mp3")
        await file.download_to_drive(file_path)
        await update.message.reply_text("✅ تم حفظ الموسيقى.")
        context.user_data['awaiting_music'] = False

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_channel'):
        link = update.message.text.strip()
        if link.startswith("http"):
            with open(CHANNELS_PATH, 'a', encoding='utf-8') as f:
                f.write(link + "\n")
            await update.message.reply_text("📺 تم حفظ القناة.")
        else:
            await update.message.reply_text("❌ الرابط غير صالح.")
        context.user_data['awaiting_channel'] = False

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ يجب تحديد متغير BOT_TOKEN.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.run_polling()
