import os

ffmpeg_path = os.environ.get("FFMPEG_PATH")
if ffmpeg_path:
    os.environ["PATH"] += os.pathsep + ffmpeg_path

_model = None

def _get_model():
    global _model
    try:
        import whisper
    except ImportError as exc:
        raise ImportError(
            "openai-whisper is not installed in this environment. "
            "Install it with `pip install openai-whisper` or use a venv that has it."
        ) from exc

    if _model is None:
        _model = whisper.load_model("base")
    return _model

def transcribe_audio(audio_path):
    model = _get_model()
    result = model.transcribe(audio_path)
    return result.get("text", "")

if __name__ == "__main__":
    print(transcribe_audio("sample.mp3.mpeg"))