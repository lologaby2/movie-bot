import os import telebot from movie_pipeline import process_tiktok_video from video_generator import create_final_video from fingerprint_utils import is_similar_to_previous, save_fingerprint

BOT_TOKEN = os.getenv("BOT_TOKEN") bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start']) def start_message(message): keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) keyboard.row("🎥 أرسل رابط تيك توك", "📤 أرسل فيديو قديم") bot.send_message(message.chat.id, "👋 مرحبًا بك! اختر أحد الخيارات:", reply_markup=keyboard)

@bot.message_handler(func=lambda msg: msg.text == "📤 أرسل فيديو قديم") def ask_for_old_video(message): bot.send_message(message.chat.id, "📁 أرسل الآن الفيديو القديم الذي نُشر سابقًا على قناتك.")

@bot.message_handler(content_types=['video']) def handle_old_video(message): try: file_info = bot.get_file(message.video.file_id) downloaded_file = bot.download_file(file_info.file_path) os.makedirs("old_videos", exist_ok=True) path = f"old_videos/{message.video.file_id}.mp4" with open(path, 'wb') as f: f.write(downloaded_file) save_fingerprint(path) bot.send_message(message.chat.id, "✅ تم حفظ الفيديو والتحقق من بصمته.") except Exception as e: bot.send_message(message.chat.id, f"❌ فشل في معالجة الفيديو: {e}")

@bot.message_handler(func=lambda msg: msg.text and 'tiktok.com' in msg.text) def handle_tiktok_link(message): link = message.text bot.send_message(message.chat.id, "📥 جاري تحميل الفيديو وتحليله...") try: result = process_tiktok_video(link) if is_similar_to_previous(result['video_path']): return bot.send_message(message.chat.id, "⚠️ هذا الفيديو مشابه لفيديو سابق، لن يتم معالجته.")

bot.send_message(message.chat.id, f"📝 النص النهائي (الرجاء تحويله إلى صوت mp3):\n\n{result['final_text']}")
    bot.send_message(message.chat.id, "🎙️ أرسل ملف الصوت بصيغة mp3 لنكمل إنتاج الفيديو.")
    os.makedirs("waiting_audio", exist_ok=True)
    with open(f"waiting_audio/{message.chat.id}.txt", 'w') as f:
        f.write(result['video_id'])
except Exception as e:
    bot.send_message(message.chat.id, f"❌ حدث خطأ: {e}")

@bot.message_handler(content_types=['audio']) def handle_audio(message): user_id = message.chat.id try: with open(f"waiting_audio/{user_id}.txt") as f: video_id = f.read().strip() except FileNotFoundError: return bot.send_message(user_id, "❗ لم يتم العثور على سياق سابق. أرسل رابط تيك توك أولاً.")

bot.send_message(user_id, "🎬 جاري إنتاج الفيديو النهائي بدقة 1080p...")
file_info = bot.get_file(message.audio.file_id)
downloaded_file = bot.download_file(file_info.file_path)

os.makedirs("temp", exist_ok=True)
audio_path = f"temp/{video_id}.mp3"
with open(audio_path, 'wb') as f:
    f.write(downloaded_file)

output_path = create_final_video(video_id, audio_path)

with open(output_path, 'rb') as f:
    bot.send_video(user_id, f, caption="🎉 هذا هو الفيديو النهائي!")

bot.infinity_polling()

