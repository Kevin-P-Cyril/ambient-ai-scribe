Ambient Clinical Scribe
Overview

Ambient Clinical Scribe is a healthcare AI application that converts doctor–patient conversations into structured clinical documentation. The system leverages Automatic Speech Recognition (ASR), Large Language Models (LLMs), and Retrieval-Augmented Generation (RAG) to automate clinical documentation and assist in medical coding.

The application enables clinicians to upload medical audio recordings, transcribe conversations, generate structured SOAP notes, and recommend relevant ICD-10 diagnosis codes for clinical documentation.

Features
Week 1 – Audio Ingestion and Speaker Diarization
Audio file upload and ingestion pipeline
FastAPI backend for audio processing
Speech-to-text transcription using OpenAI Whisper
Clinical conversation transcription workflow
Speaker diarization (Doctor/Patient identification)
Pydantic schema validation
JSON-based API responses
Week 2 – SOAP Note Generation
Prompt engineering for structured clinical documentation
Automatic SOAP note generation
Clinical information extraction
Pydantic-based structured JSON validation
Automatic validation of generated SOAP notes
Week 3 – ICD-10 Recommendation System
ICD-10 dataset preparation and preprocessing
Semantic embedding generation
ChromaDB vector database creation
Retrieval-Augmented Generation (RAG) pipeline
ICD-10 semantic search
Top-3 ICD-10 diagnosis code recommendations
SOAP-to-ICD integration
Tech Stack
Python
FastAPI
OpenAI Whisper
Google Gemini
ChromaDB
Sentence Transformers
Pandas
Pydantic
Uvicorn
Project Architecture
                    Doctor–Patient Audio
                             │
                             ▼
                    Audio Upload (FastAPI)
                             │
                             ▼
              OpenAI Whisper Speech-to-Text
                             │
                             ▼
                  Speaker Diarization
                  (Doctor / Patient)
                             │
                             ▼
                  Clinical Transcript
                             │
                             ▼
               Gemini Prompt Engineering
                             │
                             ▼
                  Structured SOAP Note
                             │
                             ▼
              Extract Assessment Section
                             │
                             ▼
              Sentence Transformer
                 Embedding Generation
                             │
                             ▼
               ChromaDB Vector Search
                             │
                             ▼
            Top-3 ICD-10 Recommendations
                             │
                             ▼
              Final Structured Response
Project Structure
ambient-ai-scribe/
│
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
├── setup.bat
├── run.bat
├── ICDCodeSet.csv
├── icd_clean.csv
└── .gitignore

Note: The icd_db/ folder is generated locally after running build_icd_db.py and is excluded from GitHub using .gitignore.

Installation
Clone Repository
git clone <repository-url>
cd ambient-ai-scribe
Install Dependencies
pip install -r requirements.txt

or

setup.bat
Running the Application

Run:

run.bat

or

python -m uvicorn main:app --reload
API Documentation

After starting the server, open:

http://127.0.0.1:8000/docs
System Workflow
Upload a doctor–patient conversation audio file.
Convert speech into text using OpenAI Whisper.
Identify Doctor and Patient speakers.
Generate a structured SOAP note.
Extract the Assessment section.
Convert the assessment into embeddings.
Perform semantic similarity search using ChromaDB.
Retrieve the Top-3 most relevant ICD-10 diagnosis codes.
Return the SOAP note along with ICD-10 recommendations.
Week-wise Roadmap
Week 1 – Audio Ingestion and Speaker Diarization
✅ Audio upload
✅ Whisper integration
✅ Transcript generation
✅ Speaker diarization
Week 2 – SOAP Note Generation
✅ Clinical information extraction
✅ SOAP note generation
✅ Structured JSON validation
Week 3 – ICD-10 Recommendation System
✅ ICD-10 dataset preprocessing
✅ ChromaDB vector database creation
✅ Embedding generation
✅ RAG-based semantic retrieval
✅ Top-3 ICD-10 recommendations
✅ SOAP-to-ICD integration
Week 4 – Human-in-the-Loop Dashboard (Planned)
⬜ Clinical dashboard
⬜ Review and edit SOAP notes
⬜ Review and edit ICD-10 recommendations
⬜ Export clinical documentation
Deliverables
Week 1
FastAPI backend
Audio upload endpoint
Whisper transcription
Speaker diarization
Week 2
SOAP note generation
Clinical information extraction
Structured JSON output
Week 3
ICD-10 dataset preparation
ChromaDB vector database
Semantic search
Retrieval-Augmented Generation (RAG)
Top-3 ICD-10 code recommendations
Future Enhancements
Human-in-the-Loop validation dashboard
Confidence scoring for ICD-10 recommendations
Electronic Health Record (EHR) integration
FHIR-compatible clinical documentation
Real-time streaming transcription
Multi-language clinical conversation support
Author
Week 3

Sujitha S
ME Computer Science and Engineering
Thiagarajar College of Engineering
