import os import json import uuid import yt_dlp from moviepy.editor import VideoFileClip from faster_whisper import WhisperModel import openai

تحميل الإعدادات

CONFIG_PATH = "config.json" with open(CONFIG_PATH, 'r', encoding='utf-8') as f: config = json.load(f)

openai.api_key = os.getenv("OPENAI_API_KEY")

def download_video(url): video_id = str(uuid.uuid4()) output_path = f"downloads/{video_id}.mp4" os.makedirs("downloads", exist_ok=True)

ydl_opts = {
    'outtmpl': output_path,
    'format': 'mp4/bestvideo[ext=mp4]+bestaudio/best',
    'quiet': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
return video_id, output_path

def extract_audio(video_path): audio_path = video_path.replace(".mp4", ".mp3") clip = VideoFileClip(video_path) clip.audio.write_audiofile(audio_path, logger=None) return audio_path

def transcribe_audio(audio_path): model = WhisperModel("base", device="cpu", compute_type="int8") segments, _ = model.transcribe(audio_path, beam_size=5) full_text = " ".join([seg.text for seg in segments]) return full_text

def translate_and_rewrite(text): prompt = f"ترجم النص التالي إلى العربية وأعد صياغته ليكون مشوقًا لفيديو يوتيوب:

{text}" response = openai.ChatCompletion.create( model="gpt-4", messages=[{"role": "user", "content": prompt}], temperature=0.7 ) return response.choices[0].message.content.strip()

def process_tiktok_video(url): video_id, video_path = download_video(url) audio_path = extract_audio(video_path) transcript = transcribe_audio(audio_path) final_text = translate_and_rewrite(transcript)

return {
    "video_id": video_id,
    "video_path": video_path,
    "final_text": final_text
}

