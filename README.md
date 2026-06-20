# Ambient Clinical Scribe

## Overview

Ambient Clinical Scribe is a healthcare AI application that converts doctor-patient conversations into structured transcripts using Automatic Speech Recognition (ASR). The system enables clinicians to upload medical audio recordings, process conversations, and generate transcribed outputs for further clinical documentation workflows.

---

## Features

### Week 1 Completed

* Audio file upload and ingestion pipeline
* FastAPI backend for audio processing
* Speech-to-text transcription using OpenAI Whisper
* Clinical conversation transcription workflow
* Basic speaker diarization (Doctor/Patient identification)
* Pydantic schema validation
* JSON-based API responses

---

## Tech Stack

* Python
* FastAPI
* OpenAI Whisper
* Pydantic
* Uvicorn

---

## Project Structure

```text
ambient_clinical_scribe/
├── main.py
├── transcription.py
├── diarization.py
├── schemas.py
├── requirements.txt
├── README.md
```

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
2. Process audio through OpenAI Whisper ASR.
3. Generate transcript text.
4. Apply speaker diarization to distinguish:

   * Doctor
   * Patient
5. Return structured transcript response.

---

## Week 1 Deliverables (Completed)

* [x] FastAPI backend initialization
* [x] Audio ingestion pipeline
* [x] Medical audio upload functionality
* [x] Speech-to-text transcription using Whisper ASR
* [x] Clinical conversation processing
* [x] Basic speaker diarization (Doctor/Patient separation)

---

## Project Roadmap

### Week 1 : Audio Ingestion and Speaker Diarization

* [x] Audio upload
* [x] Whisper integration
* [x] Transcript generation
* [x] Speaker diarization

### Week 2 : Prompt Engineering for Clinical Structuring

* [ ] SOAP Note Generation
* [ ] Clinical information extraction

### Week 3 : ICD-10 Recommendation System

* [ ] ICD-10 code recommendation
* [ ] Medical coding support

### Week 4 : Human-in-the-Loop Dashboard

* [ ] Clinical dashboard
* [ ] Note review and editing
* [ ] Export functionality
## Quick Start

### Option 1 : Automated Setup (Recommended)

Run:

```text
setup.bat
```

This will :

* Create a Python virtual environment
* Install all required dependencies

### Start the Application

Run:

```text
run.bat
```

This will :

* Activate the virtual environment
* Start the FastAPI server

### Access API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

### Test Workflow

1. Open `/upload-audio`
2. Click **Try it out**
3. Upload an audio file
4. Click **Execute**
5. View the generated transcript and speaker labels

---

## Author of week 1

**Naresh Kumar**
