# Ambient Clinical Scribe

Infotact Generative AI Internship — Project 1 (Healthcare: Ambient Clinical
Scribe & Automated SOAP Note Generator).

Transcribes a doctor-patient consultation, synthesizes it into a structured
SOAP note, recommends ICD-10 billing codes via RAG, and lets a physician
review/edit/sign off through a web dashboard — 100% on a free, local stack
(no paid APIs).

---

## Architecture

| Component            | Technology                              | Notes |
|-----------------------|------------------------------------------|-------|
| Backend / API          | Python 3.11, FastAPI                     | `main.py` |
| ASR (speech-to-text)   | `openai-whisper` (PyTorch)               | `transcription.py`; pause-based Speaker 1/2 turn splitting |
| SOAP synthesis (LLM)   | Local Ollama model, Pydantic-validated   | `soap_generator.py`; falls back to rule-based extraction if Ollama isn't running |
| ICD-10 recommendation  | ChromaDB + `sentence-transformers` (RAG) | `icd_rag_search.py`; falls back to keyword matching if the vector DB hasn't been built yet |
| Storage                | SQLite                                   | `db.py` |
| Export                 | `fpdf2` (PDF), `python-docx` (DOCX)      | `export_utils.py` — no GTK/system dependency, Windows-safe |
| Frontend (primary, working)      | Static HTML/CSS/JS served by FastAPI | `frontend/` — upload audio, edit SOAP note, approve ICD codes, sign off, download EHR JSON, export PDF, patient history |
| Frontend (React dashboard, WIP)  | React + MUI + Vite                   | `frontend-react/` — scaffolding is in place but not yet wired to the API; use `frontend/` for the working demo |

Every AI stage degrades gracefully: if Ollama or the ICD vector DB aren't
available, the app still returns a usable (if less sophisticated) result
instead of erroring out. This is intentional so a fresh checkout always
runs end-to-end, even before every optional local model is installed.

---

## Prerequisites (Windows)

- **Python 3.11** (not 3.13 — several ML packages don't have prebuilt wheels
  for 3.13 yet and will fail to build from source)
- **FFmpeg** on PATH (required by `openai-whisper`) — https://ffmpeg.org/download.html
- **Ollama** (optional, for real LLM-generated SOAP notes) — https://ollama.com,
  then `ollama pull llama3.2`
- **Node.js + npm** (optional, only needed if you continue the `frontend-react` dashboard)

## Setup

```bat
setup.bat
```

This creates a virtual environment, installs backend dependencies, copies
`.env.example` to `.env`, and builds the ICD-10 RAG vector database
(`prepare_icd.py` → `build_icd_db.py`) from `ICDCodeSet.csv`.

## Run

```bat
run.bat
```

Open **http://localhost:8000** — the working dashboard is served directly
by FastAPI from `frontend/`.

## Workflow

1. Create/select a patient.
2. Upload a consultation audio file (try the bundled `CAR0001.mp3.mp3` sample).
3. Review the transcript, edit the generated SOAP note fields, and check/uncheck
   suggested ICD-10 codes.
4. Click **Save Encounter**, then **Finalize & Sign Off** (human-in-the-loop
   requirement).
5. **Download EHR JSON** for the signed-off payload, or **Export PDF** for a
   printable note.

## Tests

```bat
.venv\Scripts\activate
pytest tests/ -q
```

---

## Known limitations / next steps

- `frontend-react/` is a scaffold (MUI layout, routing) but is not yet wired
  to the backend — treat it as a Week-4-and-beyond stretch goal, not the
  graded deliverable. The static `frontend/` dashboard is the functional one.
- Speaker diarization is a pause-based heuristic on Whisper's segment
  timestamps, not a trained diarization model (`pyannote.audio` was tried
  but needs a Hugging Face token + heavy model download, which conflicts
  with the "100% free/local, run anywhere" constraint).
- ICD-10 RAG search returns the top-3 nearest neighbors by embedding
  similarity; it is a recommendation aid, not a certified coding tool —
  the "Medical Coder" persona is expected to review before billing.

---

## GitHub workflow (see `COMMIT_GUIDELINES.md`)

This project is evaluated on 4 full weeks of GitHub activity, not just the
final code. Read `COMMIT_GUIDELINES.md` before pushing anything.
