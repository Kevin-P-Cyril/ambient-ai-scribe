from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=HF_TOKEN
)


def diarize_audio(audio_path):

    diarization = pipeline(audio_path)

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(
            f"start={turn.start:.1f}s "
            f"end={turn.end:.1f}s "
            f"speaker={speaker}"
        )