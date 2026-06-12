from fastapi import FastAPI, UploadFile, File
from app.transcriber import transcribe_audio

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ambient AI Scribe"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    transcript = transcribe_audio(file_path)

    return {
        "filename": file.filename,
        "transcript": transcript
    }