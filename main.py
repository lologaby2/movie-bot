import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7947209199:AAFOKlozQ0Ht4lwYuf-1RTbL-peFQ1mPILg"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("📥 أضف قناة"),
        KeyboardButton("🎵 أضف موسيقى"),
        KeyboardButton("🎬 اطلب فيديو الآن"),
        KeyboardButton("🛑 أوقف البوت")
    )
    bot.send_message(message.chat.id, "مرحبًا بك في بوت ملخصات الأفلام 🎬", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎵 أضف موسيقى")
def add_music(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        KeyboardButton("🎬 أكشن"),
        KeyboardButton("😢 دراما"),
        KeyboardButton("😂 كوميدي"),
        KeyboardButton("😱 رعب"),
        KeyboardButton("🌄 وثائقي"),
        KeyboardButton("🌑 غامض")
    )
    bot.send_message(message.chat.id, "اختر نوع الموسيقى لهذه الملف:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_for_audio)

def ask_for_audio(message):
    selected_category = message.text.strip()
    bot.send_message(message.chat.id, f"أرسل الآن ملف الموسيقى لتصنيف: {selected_category}")
    bot.register_next_step_handler(message, save_music_file, selected_category)

def save_music_file(message, category):
    if not message.audio:
        bot.send_message(message.chat.id, "❌ الرجاء إرسال ملف صوتي بصيغة mp3.")
        return
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = f"music/{category}_{message.audio.file_id}.mp3"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, f"✅ تم حفظ الموسيقى تحت تصنيف: {category}")

bot.infinity_polling()
