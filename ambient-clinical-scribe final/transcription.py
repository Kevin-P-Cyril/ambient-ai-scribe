"""Audio transcription + lightweight speaker diarization.

Uses openai-whisper (PyTorch based) instead of faster-whisper/PyAV, since
PyAV needs FFmpeg *development* headers that are rarely present on a fresh
Windows dev machine and cause the install to fail (see README).

Full neural diarization (pyannote.audio) needs a Hugging Face auth token,
a GPU for reasonable speed, and a large model download - overkill for a
free, local, evaluation-scale project. Instead we do a practical
turn-based heuristic: Whisper already splits audio into per-sentence/
per-utterance segments, and in a two-person Q&A style consultation each
new segment is almost always the other person replying. So we alternate
Speaker 1/Speaker 2 on every segment boundary. This is not a substitute
for real diarization (it will misattribute if one person speaks two
sentences in a row without the other responding), but it reliably
produces a readable, alternating Doctor/Patient transcript for the
typical short back-and-forth medical consult, and is dramatically more
robust than trying to guess turns from pause length alone (pause length
varies too much between recordings/mic setups to pick one universal
threshold).
"""

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
        model_size = os.environ.get("WHISPER_MODEL", "base")
        _model = whisper.load_model(model_size)
    return _model


def _diarize_segments(segments):
    """Turn Whisper's segment list into an alternating 'Speaker 1 (Doctor) /
    Speaker 2 (Patient)' transcript, one speaker turn per segment."""
    lines = []
    current_speaker = 1

    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        label = "Speaker 1 (Doctor)" if current_speaker == 1 else "Speaker 2 (Patient)"
        lines.append(f"{label}: {text}")
        current_speaker = 2 if current_speaker == 1 else 1

    return "\n".join(lines)


def transcribe_audio(audio_path, diarize=True):
    """Transcribe an audio file. Returns plain text by default, or a
    pseudo-diarized transcript (Speaker 1/2 turns) when diarize=True and
    Whisper returns segment timestamps."""
    model = _get_model()
    result = model.transcribe(audio_path)

    if diarize:
        segments = result.get("segments") or []
        if segments:
            diarized = _diarize_segments(segments)
            if diarized:
                return diarized

    return result.get("text", "")


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.mp3"
    print(transcribe_audio(path))
