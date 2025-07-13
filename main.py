import os import telebot from movie_pipeline import process_tiktok_video from video_generator import create_final_video

BOT_TOKEN = os.getenv("BOT_TOKEN") bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start']) def start_message(message): bot.send_message(message.chat.id, "👋 مرحبًا بك! أرسل رابط فيديو تيك توك لبدء المعالجة.")

@bot.message_handler(func=lambda msg: msg.text and 'tiktok.com' in msg.text) def handle_tiktok_link(message): link = message.text bot.send_message(message.chat.id, "📅 جاري تحميل الفيديو وتحليله...") try: result = process_tiktok_video(link, message.chat.id) bot.send_message(message.chat.id, f"🌟 تم انشاء النص: {result['final_text']}\n\n🎤 حوله الى صوت mp3 وارسله.") os.makedirs("waiting_audio", exist_ok=True) with open(f"waiting_audio/{message.chat.id}.txt", 'w') as f: f.write(result['video_id']) except Exception as e: bot.send_message(message.chat.id, f"❌ حدث خطأ: {e}")

@bot.message_handler(content_types=['audio']) def handle_audio(message): user_id = message.chat.id try: with open(f"waiting_audio/{user_id}.txt") as f: video_id = f.read().strip() except FileNotFoundError: return bot.send_message(user_id, "❗ لم يتم العثور على سياق سابق. أرسل رابط تيك توك أولاً.")

bot.send_message(user_id, "🎮 جاري إنتاج الفيديو النهائي بدقة 1080p...")
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

