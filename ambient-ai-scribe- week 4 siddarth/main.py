from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import importlib

# Optional heavy imports (Whisper, Torch, large libs) — import lazily so
# the app can start even when those packages are not present.
try:
    from transcription import transcribe_audio
except Exception:
    transcribe_audio = None

try:
    from soap_generator import generate_soap
except Exception:
    generate_soap = None

try:
    from icd_rag_search import get_icd_codes
except Exception:
    get_icd_codes = None

try:
    from export_utils import generate_pdf_from_soap, generate_docx_from_soap, remove_file
except Exception:
    generate_pdf_from_soap = generate_docx_from_soap = remove_file = None
from fastapi import BackgroundTasks
from db import init_db, create_patient, get_patients, save_encounter, get_encounters_for_patient
from db import update_encounter
import asyncio
import json

import shutil
import os
import tempfile
import traceback
import mimetypes

# Max upload size (50 MB)
MAX_UPLOAD_SIZE = 50 * 1024 * 1024

app = FastAPI()


@app.on_event('startup')
def startup_event():
    try:
        init_db()
    except Exception:
        pass


# Serve the single-page frontend
BASE_DIR = os.path.dirname(__file__)
FRONTEND_INDEX = os.path.join(BASE_DIR, "frontend", "index.html")
FRONTEND_STATIC = os.path.join(BASE_DIR, "frontend", "static")


@app.get("/")
def home():
    return FileResponse(FRONTEND_INDEX)


@app.get('/health')
def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory=FRONTEND_STATIC), name="static")


@app.post('/patients')
def api_create_patient(payload: dict):
    name = payload.get('name')
    metadata = payload.get('metadata')
    if not name:
        raise HTTPException(status_code=400, detail='Missing name')
    pid = create_patient(name, metadata)
    return {'id': pid}


@app.get('/patients')
def api_get_patients():
    return get_patients()


@app.post('/patients/{patient_id}/encounters')
def api_save_encounter(patient_id: int, payload: dict):
    transcript = payload.get('transcript')
    soap_note = payload.get('soap')
    icd_codes = payload.get('icd_codes') or []
    eid = save_encounter(patient_id, transcript, soap_note, icd_codes)
    return {'id': eid}


@app.put('/encounters/{encounter_id}')
def api_update_encounter(encounter_id: int, payload: dict):
    soap = payload.get('soap')
    icd_codes = payload.get('icd_codes')
    transcript = payload.get('transcript')
    updated = update_encounter(encounter_id, soap_obj=soap, icd_list=icd_codes, transcript=transcript)
    if updated:
        return {'status': 'ok'}
    raise HTTPException(status_code=404, detail='Encounter not found')


@app.put('/api/encounters/{encounter_id}')
def api_update_encounter_alias(encounter_id: int, payload: dict):
    return api_update_encounter(encounter_id, payload)


@app.put('/encounters/{encounter_id}/icd')
def api_update_encounter_icd(encounter_id: int, payload: dict):
    icd_codes = payload.get('icd_codes')
    if icd_codes is None:
        raise HTTPException(status_code=400, detail='Missing icd_codes in request body')
    updated = update_encounter(encounter_id, icd_list=icd_codes)
    if updated:
        return {'status': 'ok'}
    raise HTTPException(status_code=404, detail='Encounter not found')


@app.put('/api/encounters/{encounter_id}/icd')
def api_update_encounter_icd_alias(encounter_id: int, payload: dict):
    return api_update_encounter_icd(encounter_id, payload)


@app.get('/patients/{patient_id}/encounters')
def api_get_encounters(patient_id: int):
    return get_encounters_for_patient(patient_id)


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # Robust audio validation: prefer content-type, fall back to extension or file header sniffing
    content_type = (file.content_type or "").lower()
    is_audio = False
    if content_type.startswith("audio"):
        is_audio = True
    else:
        # guess from filename extension
        guessed, _ = mimetypes.guess_type(file.filename or "")
        if guessed and guessed.startswith("audio"):
            is_audio = True
        else:
            # peek at the first bytes to detect common audio file signatures (ID3, RIFF, ftyp/mp4)
            try:
                head = await file.read(16)
                await file.seek(0)
                if head.startswith(b'ID3'):
                    is_audio = True
                elif head.startswith(b'RIFF'):
                    is_audio = True
                elif len(head) >= 8 and head[4:8] == b'ftyp':
                    is_audio = True
                elif len(head) >= 2 and head[0] == 0xFF:
                    # probable MP3 frame
                    is_audio = True
            except Exception:
                # if anything goes wrong, we'll consider it not audio
                try:
                    await file.seek(0)
                except Exception:
                    pass

    if not is_audio:
        raise HTTPException(status_code=400, detail="Invalid file type; please upload an audio file")

    # Verify that the optional backends are available
    if transcribe_audio is None:
        raise HTTPException(status_code=503, detail="Transcription backend is not available on the server")
    if generate_soap is None:
        raise HTTPException(status_code=503, detail="SOAP generation backend is not available on the server")

    tmp_path = None
    try:
        try:
            # Save to a temp file while enforcing size limit
            suffix = os.path.splitext(file.filename or "")[1] or ".audio"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp_path = tmp.name
                total = 0
                # UploadFile.read is async
                while True:
                    chunk = await file.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_UPLOAD_SIZE:
                        raise HTTPException(status_code=413, detail="File too large")
                    tmp.write(chunk)

                # Run blocking/CPU tasks in threadpool to avoid blocking the event loop
                # Be defensive: if transcription or SOAP generation fail, log and continue with best-effort results
                transcript = ""
                try:
                    transcript = await asyncio.to_thread(transcribe_audio, tmp_path)
                except Exception as e:
                    # log and continue with empty transcript
                    try:
                        tb = traceback.format_exc()
                        with open(os.path.join(BASE_DIR, 'server_error.log'), 'a', encoding='utf-8') as lf:
                            lf.write('--- transcription error ---\n')
                            lf.write(tb)
                            lf.write('\n')
                    except Exception:
                        pass

                soap_note = None
                try:
                    soap_note = await asyncio.to_thread(generate_soap, transcript)
                except Exception as e:
                    # log and replace with minimal SOAP note
                    try:
                        tb = traceback.format_exc()
                        with open(os.path.join(BASE_DIR, 'server_error.log'), 'a', encoding='utf-8') as lf:
                            lf.write('--- soap generation error ---\n')
                            lf.write(tb)
                            lf.write('\n')
                    except Exception:
                        pass
                    soap_note = {
                        'subjective': transcript.strip() or 'No transcript available.',
                        'objective': 'Objective exam findings unavailable.',
                        'assessment': 'SOAP generation failed; see server logs.',
                        'plan': ''
                    }

            assessment = None
            try:
                assessment = soap_note.get("Assessment") or soap_note.get("assessment", "")
            except Exception:
                assessment = ""

            icd_codes = []
            if get_icd_codes is None:
                # ICD lookup is optional — return empty list if unavailable
                icd_codes = []
            else:
                try:
                    icd_codes = await asyncio.to_thread(get_icd_codes, assessment)
                except Exception:
                    icd_codes = []

            # Return everything
            return {
                "transcript": transcript,
                "soap_note": soap_note,
                "icd_codes": icd_codes
            }
        finally:
            # Clean up temp file
            try:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
    except Exception:
        # Log full traceback to server_error.log for debugging
        try:
            tb = traceback.format_exc()
            log_path = os.path.join(BASE_DIR, 'server_error.log')
            with open(log_path, 'a', encoding='utf-8') as lf:
                lf.write('--- /upload-audio exception ---\n')
                lf.write(tb)
                lf.write('\n')
        except Exception:
            pass
        raise HTTPException(status_code=500, detail='Internal Server Error (see server_error.log)')



@app.post('/export')
async def export_note(format: str = 'pdf', background_tasks: BackgroundTasks = None, soap_note: dict = None):
    """Export a SOAP note to PDF or DOCX. POST JSON body with `soap_note` (dict) and optional query param `format` (pdf|docx)."""
    fmt = (format or 'pdf').lower()
    if fmt not in ('pdf', 'docx'):
        raise HTTPException(status_code=400, detail='format must be "pdf" or "docx"')

    if soap_note is None:
        raise HTTPException(status_code=400, detail='Missing soap_note in request body')

    if fmt == 'pdf':
        out_path = generate_pdf_from_soap(soap_note)
        media_type = 'application/pdf'
        filename = 'soap_note.pdf'
    else:
        out_path = generate_docx_from_soap(soap_note)
        media_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        filename = 'soap_note.docx'

    # Schedule file cleanup
    try:
        if background_tasks is not None:
            background_tasks.add_task(remove_file, out_path)
    except Exception:
        pass

    return FileResponse(out_path, media_type=media_type, filename=filename)



@app.websocket('/ws/transcribe')
async def websocket_transcribe(websocket: WebSocket):
    """Accepts binary audio chunks over the websocket and returns partial transcripts.
    Client should send binary messages (raw audio blobs). Send text message '__done__' to finish.
    """
    await websocket.accept()
    tmp_file = None
    try:
        # create a per-connection temp file
        fd, tmp_path = tempfile.mkstemp(suffix='.webm')
        os.close(fd)

        lock = asyncio.Lock()
        stop_event = asyncio.Event()

        last_transcript = ""

        async def periodic_transcribe():
            nonlocal last_transcript
            try:
                while not stop_event.is_set():
                    await asyncio.sleep(3)
                    try:
                        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                            # run transcription in thread pool to avoid blocking
                            transcript = await asyncio.to_thread(transcribe_audio, tmp_path)
                            if transcript and transcript != last_transcript:
                                last_transcript = transcript
                                await websocket.send_json({"transcript": transcript})
                    except Exception as e:
                        try:
                            await websocket.send_json({"error": str(e)})
                        except Exception:
                            pass
            except asyncio.CancelledError:
                pass

        task = asyncio.create_task(periodic_transcribe())

        while True:
            msg = await websocket.receive()
            # handle binary
            if 'bytes' in msg and msg['bytes'] is not None:
                chunk = msg['bytes']
                async with lock:
                    with open(tmp_path, 'ab') as f:
                        f.write(chunk)
            elif 'text' in msg and msg['text'] is not None:
                text = msg['text']
                if text == '__done__':
                    # final transcription
                    try:
                        final = await asyncio.to_thread(transcribe_audio, tmp_path) if os.path.exists(tmp_path) else ''
                        await websocket.send_json({"final_transcript": final})
                    except Exception as e:
                        try:
                            await websocket.send_json({"error": str(e)})
                        except Exception:
                            pass
                    break
                else:
                    # ignore other text messages
                    continue
            else:
                # unknown message type, break
                break

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        try:
            stop_event.set()
        except Exception:
            pass
        try:
            task.cancel()
        except Exception:
            pass
        try:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass



@app.websocket('/ws/stream-asr')
async def websocket_stream_asr(websocket: WebSocket):
    """Low-latency ASR WebSocket using Vosk. Accepts raw 16-bit PCM audio frames (little-endian) as binary messages.
    Sends JSON messages with `partial` or `final` transcripts.
    Requires `vosk` and a VOSK_MODEL_PATH env var or a `model` folder in the project root.
    """
    await websocket.accept()
    recognizer = None
    model = None
    try:
        try:
            from vosk import Model, KaldiRecognizer
        except Exception as e:
            await websocket.send_json({"error": "vosk not installed on server; install vosk and a model"})
            await websocket.close()
            return

        # locate model
        model_path = os.environ.get('VOSK_MODEL_PATH') or os.path.join(os.path.dirname(__file__), 'model')
        if not os.path.exists(model_path):
            await websocket.send_json({"error": f"Vosk model not found at {model_path}. Set VOSK_MODEL_PATH or download model."})
            await websocket.close()
            return

        model = Model(model_path)
        # default sample rate
        sample_rate = 16000
        recognizer = KaldiRecognizer(model, sample_rate)

        patient_override_id = None
        while True:
            msg = await websocket.receive()
            if 'bytes' in msg and msg['bytes'] is not None:
                data = msg['bytes']
                try:
                    is_final = recognizer.AcceptWaveform(data)
                    if is_final:
                        res = recognizer.Result()
                        try:
                            j = json.loads(res)
                            text = j.get('text', '')
                        except Exception:
                            text = res
                        # send final transcript
                        await websocket.send_json({"final": text})
                        # generate SOAP note and ICD suggestions in threadpool
                        try:
                            soap_note = await asyncio.to_thread(generate_soap, text)
                            assessment = soap_note.get('Assessment') or soap_note.get('assessment', '')
                            icd_codes = []
                            if assessment:
                                try:
                                    icd_codes = await asyncio.to_thread(get_icd_codes, assessment)
                                except Exception:
                                    icd_codes = []
                            # persist to DB: use override patient if provided, otherwise first patient or anonymous
                            try:
                                if patient_override_id:
                                    patient_id = patient_override_id
                                else:
                                    patients = get_patients()
                                    if patients and len(patients) > 0:
                                        patient_id = patients[0]['id']
                                    else:
                                        patient_id = create_patient('Anonymous')
                                # save encounter and return id
                                eid = await asyncio.to_thread(save_encounter, patient_id, text, soap_note, icd_codes)
                            except Exception:
                                eid = None
                            # send SOAP, ICDs and encounter id
                            await websocket.send_json({"soap_note": soap_note, "icd_codes": icd_codes, "encounter_id": eid})
                        except Exception as e:
                            try:
                                await websocket.send_json({"error": f"soap_generation_error: {str(e)}"})
                            except Exception:
                                pass
                    else:
                        pres = recognizer.PartialResult()
                        try:
                            pj = json.loads(pres)
                            ptext = pj.get('partial', '')
                        except Exception:
                            ptext = pres
                        await websocket.send_json({"partial": ptext})
                except Exception as e:
                    await websocket.send_json({"error": str(e)})
            elif 'text' in msg and msg['text'] is not None:
                t = msg['text']
                if t == '__done__':
                    # flush
                    if recognizer:
                        try:
                            res = recognizer.FinalResult()
                            try:
                                j = json.loads(res)
                                text = j.get('text', '')
                            except Exception:
                                text = res
                            await websocket.send_json({"final": text})
                        except Exception as e:
                            await websocket.send_json({"error": str(e)})
                    break
                else:
                    # allow client to send a JSON payload with patient_id override
                    try:
                        payload = json.loads(t)
                        if isinstance(payload, dict) and 'patient_id' in payload:
                            try:
                                patient_override_id = int(payload.get('patient_id'))
                            except Exception:
                                patient_override_id = None
                    except Exception:
                        # ignore non-json text
                        pass
                    continue
            else:
                break

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
