import io
import os
from fastapi.testclient import TestClient

import transcription
import soap_generator
import icd_rag_search


def test_upload_audio_success(monkeypatch):
    # Mock heavy functions
    monkeypatch.setattr(transcription, 'transcribe_audio', lambda path: 'mock transcript')
    monkeypatch.setattr(soap_generator, 'generate_soap', lambda t: {'Assessment': 'mock assessment'})
    monkeypatch.setattr(icd_rag_search, 'get_icd_codes', lambda a: ['A00'])

    from main import app

    client = TestClient(app)

    data = {
        'file': ('test.wav', io.BytesIO(b'RIFF....'), 'audio/wav')
    }

    resp = client.post('/upload-audio', files=data)
    assert resp.status_code == 200
    body = resp.json()
    assert body['transcript'] == 'mock transcript'
    assert isinstance(body['soap_note'], dict)
    assert body['icd_codes'] == ['A00']


def test_upload_audio_invalid_type():
    from main import app
    client = TestClient(app)

    data = {
        'file': ('test.txt', io.BytesIO(b'not audio'), 'text/plain')
    }

    resp = client.post('/upload-audio', files=data)
    assert resp.status_code == 400