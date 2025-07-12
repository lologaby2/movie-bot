import os
import uuid
import yt_dlp
from moviepy.editor import VideoFileClip
from faster_whisper import WhisperModel
import openai
import requests

# تحميل الفيديو من تيك توك
def download_tiktok_video(tiktok_url: str) -> str:
    video_id = str(uuid.uuid4())
    os.makedirs("downloads", exist_ok=True)
    output_path = f"downloads/{video_id}.mp4"

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([tiktok_url])

    return video_id

# استخراج الصوت بصيغة mp3
def extract_audio(video_id: str) -> str:
    video_path = f"downloads/{video_id}.mp4"
    audio_path = f"downloads/{video_id}.mp3"

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, logger=None)
    return audio_path

# تفريغ النص الإنجليزي باستخدام Whisper
def extract_english_text(audio_path: str) -> str:
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    english_text = " ".join([seg.text.strip() for seg in segments])
    return english_text

# ترجمة النص إلى العربية باستخدام OpenAI
def translate_to_arabic(english_text: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "ترجم النص التالي إلى العربية ترجمة بشرية احترافية:"},
            {"role": "user", "content": english_text}
        ]
    )
    return response.choices[0].message.content.strip()

# إعادة صياغة النص بالعربية باستخدام ChatGPT
def rewrite_arabic_text(arabic_text: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "أعد صياغة هذا النص بأسلوب سردي مشوق وكأنك تحكيه لمتابعين على تيك توك:"},
            {"role": "user", "content": arabic_text}
        ]
    )
    return response.choices[0].message.content.strip()

# دالة رئيسية للتجميع
def process_tiktok_video(tiktok_url: str) -> dict:
    video_id = download_tiktok_video(tiktok_url)
    audio_path = extract_audio(video_id)
    english_text = extract_english_text(audio_path)
    arabic_text = translate_to_arabic(english_text)
    final_text = rewrite_arabic_text(arabic_text)

    return {
        "video_id": video_id,
        "final_text": final_text
    }
