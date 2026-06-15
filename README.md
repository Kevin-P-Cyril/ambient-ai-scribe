# Ambient Clinical Scribe

## Overview

Ambient Clinical Scribe is a healthcare AI application that converts doctor-patient conversations into text using automatic speech recognition (ASR). The system allows users to upload medical audio recordings and generates accurate transcripts for further clinical documentation.

## Features

* Audio file upload
* Speech-to-text transcription using OpenAI Whisper
* FastAPI backend for audio processing
* Clinical conversation transcription workflow
* Pydantic schema validation

## Tech Stack

* Python
* FastAPI
* OpenAI Whisper
* Pydantic
* Uvicorn

## Project Structure

```text
ambient_clinical_scribe/
├── main.py
├── transcription.py
├── schemas.py
├── requirements.txt
├── README.md
```

## Installation

### Clone Repository

```bash
git clone <repository-url>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend Server

```bash
python -m uvicorn main:app --reload
```

## Week 1 Deliverables

* FastAPI backend initialization
* Audio ingestion pipeline
* Medical audio upload functionality
* Speech-to-text transcription using Whisper ASR
* Processing of clinical conversation recordings

## Future Enhancements

* Speaker diarization (Doctor/Patient separation)
* SOAP note generation
* ICD code recommendation
* Clinical summarization

## Author

Naresh Kumar


