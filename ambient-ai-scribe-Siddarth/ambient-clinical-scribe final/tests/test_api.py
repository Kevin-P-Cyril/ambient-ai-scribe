import io
from fastapi.testclient import TestClient


def test_upload_audio_success(monkeypatch):
    import main as main_module

    # Mock heavy functions. main.py does `from transcription import
    # transcribe_audio`, so we must patch the name bound in main's own
    # namespace, not the source module's attribute.
    monkeypatch.setattr(main_module, 'transcribe_audio', lambda path: 'mock transcript')
    monkeypatch.setattr(main_module, 'generate_soap', lambda t: {'assessment': 'mock assessment'})
    monkeypatch.setattr(main_module, 'get_icd_codes', lambda a: ['A00'])

    client = TestClient(main_module.app)

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