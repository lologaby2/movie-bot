# movie_pipeline.py

import os
import json
import requests
import uuid
from moviepy.editor import VideoFileClip
from alignment_manager import extract_alignment_from_audio


def download_tiktok_video(link: str, output_path='data/source.mp4'):
    video_id = str(uuid.uuid4())[:8]
    out_path = f"data/{video_id}.mp4"
    
    api_url = "https://tikwm.com/api/"
    params = {"url": link}
    try:
        r = requests.get(api_url, params=params).json()
        video_url = r['data']['play']
        video = requests.get(video_url)
        with open(out_path, 'wb') as f:
            f.write(video.content)
        return out_path
    except:
        raise Exception("❌ فشل تحميل الفيديو من تيك توك")


def extract_english_audio(video_path, output_path=None):
    if output_path is None:
        output_path = video_path.replace('.mp4', '.mp3')
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_path)
    return output_path


def call_openai_api(text: str):
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
    هذا نص إنجليزي من ملخص فيلم، ترجمه إلى العربية مع إعادة صياغته بأسلوب راوي سينمائي مشوق، وابتعد عن الحرفية.

    النص:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def process_tiktok_video(link: str):
    video_path = download_tiktok_video(link)
    audio_path = extract_english_audio(video_path)
    alignment = extract_alignment_from_audio(audio_path)
    full_text = "\n".join([seg['text'] for seg in alignment])
    translated_text = call_openai_api(full_text)

    translated_lines = translated_text.split(". ")
    for i in range(min(len(alignment), len(translated_lines))):
        alignment[i]['translated'] = translated_lines[i].strip()

    with open("data/alignment.json", "w", encoding='utf-8') as f:
        json.dump(alignment, f, ensure_ascii=False, indent=2)

    return {
        "video_id": os.path.splitext(os.path.basename(video_path))[0],
        "final_text": translated_text
    }
