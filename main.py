from fastapi import FastAPI, UploadFile, File
from transcription import transcribe_audio
from soap_generator import generate_soap
from icd_recommender import recommend_icd
import shutil

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Ambient Clinical Scribe API"}


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    file_path = file.filename

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate transcript
    transcript = transcribe_audio(file_path)

    # Generate SOAP note
    soap_note = generate_soap(transcript)

    

    # Return everything
    return {
        "transcript": transcript,
        "soap_note": soap_note,
        
    }
