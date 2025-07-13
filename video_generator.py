import os from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip

def create_final_video(video_id, audio_path): video_path = f"downloads/{video_id}.mp4" output_path = f"final/{video_id}_final.mp4"

os.makedirs("final", exist_ok=True)

video = VideoFileClip(video_path)
audio = AudioFileClip(audio_path).volumex(1.0)

# ضبط مستوى صوت الموسيقى الخلفية إذا وجدت
music_volume = float(os.getenv("MUSIC_VOLUME", 0.2))
if os.path.exists("music/background.mp3"):
    music = AudioFileClip("music/background.mp3").volumex(music_volume)
    final_audio = audio.set_duration(video.duration).fx(lambda a: a.volumex(1.0)).audio_fadein(1).audio_fadeout(1)
    final_audio = final_audio.overlay(music.set_duration(video.duration))
else:
    final_audio = audio

video = video.set_audio(final_audio)
video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=30, preset='medium')

return output_path

