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
