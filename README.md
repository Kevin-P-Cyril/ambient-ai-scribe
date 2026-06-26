# 🏥 Ambient Clinical Scribe

## Overview

Ambient Clinical Scribe is a healthcare AI application that converts doctor–patient conversations into structured clinical documentation using Automatic Speech Recognition (ASR) and Large Language Models.

The system allows clinicians to upload medical audio recordings, transcribe conversations, generate SOAP notes, and recommend ICD-10 diagnostic codes using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🚀 Features

### Week 1 – Audio Ingestion & Transcription
- Audio file upload and ingestion pipeline
- FastAPI backend for audio processing
- Speech-to-text transcription using OpenAI Whisper
- Clinical conversation transcription workflow
- Basic speaker diarization (Doctor / Patient separation)
- Pydantic schema validation
- JSON-based API responses

---

### Week 2 – Clinical Structuring (SOAP Notes)
- SOAP note generation from clinical transcripts
- Structured medical information extraction
- Prompt engineering for clinical summarization
- Organized clinical documentation output

---

### Week 3 – ICD-10 Recommendation System
- ICD-10 dataset preparation and cleaning
- Vector database creation using embeddings (ChromaDB)
- Semantic search over medical codes
- RAG-based ICD-10 recommendation system
- SOAP-to-ICD mapping pipeline
- Ranked diagnosis suggestion output

---

## 🧠 Tech Stack

- Python
- FastAPI
- OpenAI Whisper
- ChromaDB
- Pydantic
- Uvicorn

---

## 📁 Project Structure

```text
ambient_clinical_scribe/
├── main.py
├── transcription.py
├── diarization.py
├── soap_generator.py
├── soap_icd_integration.py
├── icd_rag_search.py
├── build_icd_db.py
├── prepare_icd.py
├── schemas.py
├── requirements.txt
├── README.md


⚙️ Installation
Clone Repository
git clone <repository-url>
cd ambient_clinical_scribe
Install Dependencies
pip install -r requirements.txt
Run Server
python -m uvicorn main:app --reload


🔄 API Workflow
Upload medical conversation audio
Transcribe using Whisper ASR
Identify speaker roles (Doctor / Patient)
Generate SOAP notes
Extract clinical entities
Recommend ICD-10 codes using RAG
Return structured medical output

📌 Project Roadmap
Week 1: Audio Processing
 Audio upload system
 Whisper transcription
 Speaker diarization
Week 2: SOAP Generation
 Clinical structuring
 SOAP note generation
Week 3: ICD-10 RAG System
 ICD-10 recommendation engine
 Vector database integration
 Semantic medical search
Week 4: Human-in-the-Loop Dashboard
 Clinical review interface
 Editing & validation system
 Export to EHR formats
