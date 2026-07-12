# Ambient AI Scribe — Frontend + Backend

Quick local setup and run instructions for the small frontend added to the FastAPI backend.

Prereqs
- Python 3.10+ (with pip)
- FFmpeg available on PATH (your `transcription.py` sets a PATH override; verify or set your own)

Install
```bash
python -m pip install -r requirements.txt
```

Run
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser. The web UI lets you select or create a patient, upload an audio file, generate a transcript, create a SOAP note, and view ICD suggestions.

Notes
- The frontend lives in the `frontend/` folder and static assets in `frontend/static/`.
- Server file upload endpoint: `POST /upload-audio`.
- If you hit dependency or model-loading issues for `openai-whisper` or `torch`, follow their upstream install docs for your platform/GPU.
# Ambient Clinical Scribe

## Overview

Ambient Clinical Scribe is a healthcare AI application that converts doctor–patient conversations into structured clinical documentation using Automatic Speech Recognition (ASR), Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG). The system enables clinicians to upload medical audio recordings, generate transcripts, create SOAP notes, and recommend ICD-10 diagnosis codes for clinical documentation.

---

## Features

### Week 1 Completed
- Audio file upload and ingestion pipeline
- FastAPI backend for audio processing
- Speech-to-text transcription using OpenAI Whisper
- Clinical conversation transcription workflow
- Speaker diarization (Doctor/Patient identification)
- Pydantic schema validation
- JSON-based API responses

### Week 2 Completed
- SOAP note generation
- Clinical information extraction
- Prompt engineering for structured medical documentation
- JSON validation using Pydantic

### Week 3 Completed
- ICD-10 dataset preparation and preprocessing
- ChromaDB vector database creation
- Sentence Transformer embedding generation
- Retrieval-Augmented Generation (RAG) implementation
- Semantic search for ICD-10 diagnosis codes
- Top-3 ICD-10 recommendation system
- SOAP note and ICD-10 integration

---

## Tech Stack

- Python
- FastAPI
- OpenAI Whisper
- Google Gemini
- ChromaDB
- Sentence Transformers
- Pandas
- Pydantic
- Uvicorn

---

## Project Structure

```text
ambient_clinical_scribe/
├── main.py
├── transcription.py
├── diarization.py
├── soap_generator.py
├── soap_icd_integration.py
├── build_icd_db.py
├── prepare_icd.py
├── icd_rag_search.py
├── schemas.py
├── requirements.txt
├── README.md
├── setup.bat
├── run.bat
├── ICDCodeSet.csv
└── icd_clean.csv
```

> **Note:** The `icd_db/` folder is generated locally after running `build_icd_db.py` and is excluded from GitHub using `.gitignore`.

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ambient_clinical_scribe
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend Server

```bash
python -m uvicorn main:app --reload
```

---

## API Workflow

1. Upload a medical conversation audio file.
2. Process the audio using OpenAI Whisper ASR.
3. Generate the clinical transcript.
4. Apply speaker diarization to identify:
   - Doctor
   - Patient
5. Generate a structured SOAP note.
6. Extract the Assessment section.
7. Perform semantic search on the ICD-10 vector database.
8. Retrieve the Top-3 relevant ICD-10 diagnosis codes.
9. Return the SOAP note with ICD-10 recommendations.

---

## Week 3 Deliverables (Completed)

- ✅ ICD-10 dataset preparation
- ✅ Data preprocessing and cleaning
- ✅ ChromaDB vector database creation
- ✅ Sentence Transformer embedding generation
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Semantic ICD-10 code retrieval
- ✅ Top-3 ICD-10 code recommendations
- ✅ SOAP note and ICD-10 integration

---

## Project Roadmap

### Week 1: Audio Ingestion and Speaker Diarization

- ✅ Audio upload
- ✅ Whisper integration
- ✅ Transcript generation
- ✅ Speaker diarization

### Week 2: Prompt Engineering for Clinical Structuring

- ✅ SOAP Note Generation
- ✅ Clinical information extraction
- ✅ Structured JSON validation

### Week 3: RAG Implementation for ICD-10 Coding Recommendations

- ✅ ICD-10 dataset preparation
- ✅ Embedding generation
- ✅ ChromaDB vector database
- ✅ Semantic retrieval
- ✅ Top-3 ICD-10 code recommendation
- ✅ SOAP-to-ICD integration

### Week 4: Human-in-the-Loop Dashboard

- ⬜ Clinical dashboard
- ⬜ Note review and editing
- ⬜ Export functionality

---

## Quick Start

### Option 1: Automated Setup (Recommended)

Run:

```text
setup.bat
```

This will:

- Create a Python virtual environment
- Install all required dependencies

### Start the Application

Run:

```text
run.bat
```

This will:

- Activate the virtual environment
- Start the FastAPI server

### Access API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

### Test Workflow

1. Open `/upload-audio`
2. Click **Try it out**
3. Upload a medical audio file
4. Click **Execute**
5. View the generated transcript
6. Review the generated SOAP note
7. View the recommended Top-3 ICD-10 diagnosis codes

---

## Author


**Sujitha S**
ME Computer Science and Engineering
Thiagarajar College of Engineering

## Tests

Run the unit tests (mocks used for heavy model calls):

```bash
pip install -r requirements.txt
pytest -q
```

The tests are located in the `tests/` folder and cover the `/upload-audio` endpoint with mocked transcription and processing functions.

## Frontend (React + Vite)

I scaffolded a React + Vite frontend in `frontend-react/`. To run it locally:

```bash
cd frontend-react
npm install
npm run dev
```

The Vite dev server runs on port 5173 and proxies `/upload-audio` to the backend at `http://localhost:8000` (so run the FastAPI server first).

## Production (Docker)

You can run a production setup locally using Docker and docker-compose. This builds the backend and frontend images and serves the frontend via nginx.

```bash
docker-compose build
docker-compose up -d
```

Frontend will be available on http://localhost:8080 and the backend API on http://localhost:8000. The nginx config proxies `/upload-audio` to the backend when running in Docker Desktop.

## Exporting SOAP notes (PDF / Word)

The backend exposes an endpoint to export SOAP notes:

- `POST /export?format=pdf` — returns a PDF file
- `POST /export?format=docx` — returns a Word `.docx` file

Request body (JSON):

```json
{
   "soap_note": { "Subjective": "...", "Objective": "...", "Assessment": "...", "Plan": "..." }
}
```

Notes:
- PDF generation uses `WeasyPrint` (server-side). The Dockerfile installs the necessary system libraries. On native installs you must install the OS packages required by WeasyPrint before installing Python packages.
- Word export uses `python-docx`.
- On Windows with Python 3.13, the project is pinned to `numpy==2.4.6` and `vosk==0.3.45` to match available binary wheels.
- If Whisper needs FFmpeg, set `FFMPEG_PATH` to the FFmpeg `bin` directory instead of editing source files.


