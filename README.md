# Ambient Clinical Scribe

## Overview

Ambient Clinical Scribe is a healthcare AI application that converts doctor-patient conversations into structured clinical documentation using Artificial Intelligence. The system transcribes medical conversations, generates SOAP notes, and recommends ICD-10 codes to assist healthcare professionals in clinical documentation.

---

## Features

### Week 1 Completed

- Audio file upload and ingestion pipeline
- FastAPI backend for audio processing
- Speech-to-text transcription using OpenAI Whisper
- Clinical conversation transcription
- Basic speaker diarization (Doctor/Patient identification)
- Pydantic schema validation
- JSON-based API responses

### Week 2 Completed

- Prompt engineering for clinical structuring
- Automatic SOAP note generation
- Extraction of Subjective, Objective, Assessment, and Plan
- Structured clinical documentation workflow

### Week 3 Completed

- ICD-10 dataset integration
- ICD dataset preprocessing
- Clean dataset generation
- ICD recommendation module
- Foundation for RAG-based ICD search

---

## Tech Stack

- Python
- FastAPI
- OpenAI Whisper
- Google Gemini API
- Pandas
- Pydantic
- Uvicorn

---

## Project Structure

```text
ambient_ai_scribe/

├── main.py
├── transcription.py
├── diarization.py
├── soap_generator.py
├── icd_recommender.py
├── prepare_icd.py
├── ICDCodeSet.csv
├── icd_clean.csv
├── schemas.py
├── requirements.txt
├── setup.bat
├── run.bat
├── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ambient_ai_scribe
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

```text
Medical Audio
      ↓
Audio Upload
      ↓
OpenAI Whisper ASR
      ↓
Transcript Generation
      ↓
Speaker Identification
      ↓
SOAP Note Generation
      ↓
ICD-10 Recommendation
```

---

## Week 1 Deliverables

- [x] FastAPI backend initialization
- [x] Audio upload pipeline
- [x] Whisper ASR integration
- [x] Transcript generation
- [x] Basic speaker diarization
- [x] Swagger API testing

---

## Week 2 Deliverables

- [x] Prompt Engineering
- [x] SOAP Note Generation
- [x] Subjective extraction
- [x] Objective extraction
- [x] Assessment generation
- [x] Plan generation

---

## Week 3 Deliverables

- [x] ICD-10 dataset integration
- [x] ICD dataset preprocessing
- [x] Clean dataset creation
- [x] Basic ICD recommendation module
- [ ] RAG-based ICD retrieval
- [ ] Vector database integration

---

## Project Roadmap

### Week 1

- Audio Ingestion
- Whisper ASR
- Speaker Diarization

### Week 2

- Prompt Engineering
- SOAP Note Generation

### Week 3

- ICD-10 Recommendation
- Dataset Preprocessing
- RAG Preparation

### Week 4

- Human-in-the-Loop Dashboard
- Clinical Note Editing
- Export Functionality

---

## Current Workflow

1. Upload a medical audio file.
2. Convert speech into text using Whisper.
3. Identify Doctor and Patient conversation.
4. Generate a structured SOAP note.
5. Recommend ICD-10 codes based on clinical assessment.

---

## Author

**Naresh Kumar**

