from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1"
)

diarization = pipeline("nishi.mp3")

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{speaker}: {turn.start:.1f}s -> {turn.end:.1f}s")
    