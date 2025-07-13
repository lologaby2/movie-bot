import os
import cv2
from moviepy.editor import (
    VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
)
from fingerprint_utils import extract_fingerprint, save_fingerprint, is_duplicate

VIDEOS_FOLDER = "videos"
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def create_final_video(video_id, audio_path):
    video_path = os.path.join(VIDEOS_FOLDER, f"{video_id}.mp4")
    output_path = os.path.join(OUTPUT_FOLDER, f"final_{video_id}.mp4")

    # التحقق من التكرار
    new_fp = extract_fingerprint(video_path)
    if is_duplicate(new_fp):
        raise Exception("🚫 هذا الفيديو مشابه لفيديو سابق ولن يتم إعادة إنتاجه.")
    save_fingerprint(video_id, new_fp)

    # تحميل الفيديو والصوت
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path).volumex(1.0)

    # المزامنة: تطابق مدة الفيديو مع الصوت عبر التسريع أو التبطيء
    ratio = audio.duration / video.duration
    video = video.fx(lambda clip: clip.speedx(ratio))

    # دمج الصوت والفيديو
    final_video = video.set_audio(audio)

    # تصدير الفيديو النهائي بدقة 1080p
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        threads=4,
        preset="medium"
    )

    return output_path
