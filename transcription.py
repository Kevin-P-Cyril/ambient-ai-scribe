import os

os.environ["PATH"] += os.pathsep + r"C:\Users\yadav\Downloads\ffmpeg-2026-06-10-git-b29bdd3715-essentials_build\ffmpeg-2026-06-10-git-b29bdd3715-essentials_build\bin"

import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    print(transcribe_audio("sample.mp3.mpeg"))