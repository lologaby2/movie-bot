import os import json import yt_dlp import tempfile import shutil from faster_whisper import WhisperModel from openai import OpenAI from utils import translate_and_rewrite from fingerprint_utils import compute_video_hash, is_duplicate

model = WhisperModel("medium", compute_type="float16") openai_api_key = os.getenv("OPENAI_API_KEY")

HISTORY_PATH = "history.json"

if not os.path.exists(HISTORY_PATH): with open(HISTORY_PATH, 'w') as f: json.dump([], f)

def download_video(url): ydl_opts = { 'format': 'mp4', 'outtmpl': 'downloads/%(id)s.%(ext)s', 'quiet': True, 'no_warnings': True, } with yt_dlp.YoutubeDL(ydl_opts) as ydl: info = ydl.extract_info(url, download=True) video_path = ydl.prepare_filename(info) return video_path, info.get("id", "unknown")

def transcribe_audio(video_path): segments, _ = model.transcribe(video_path, vad_filter=True) english_text = "\n".join([seg.text for seg in segments]) return english_text

def check_duplicate(video_path): new_hash = compute_video_hash(video_path) with open(HISTORY_PATH, 'r') as f: history = json.load(f)

for item in history:
    if is_duplicate(new_hash, item["hash"], threshold=0.10):
        return True
return False

def save_to_history(video_id, video_path): with open(HISTORY_PATH, 'r') as f: history = json.load(f) video_hash = compute_video_hash(video_path) history.append({"id": video_id, "hash": video_hash}) with open(HISTORY_PATH, 'w') as f: json.dump(history, f, indent=2)

def process_tiktok_video(url): video_path, video_id = download_video(url)

if check_duplicate(video_path):
    raise Exception("🚫 هذا الفيديو مشابه لفيديو سابق")

english_text = transcribe_audio(video_path)
final_text = translate_and_rewrite(english_text, openai_api_key)

save_to_history(video_id, video_path)
return {"final_text": final_text, "video_id": video_id}

