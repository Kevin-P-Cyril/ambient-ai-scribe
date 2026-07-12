"""LLM Synthesis Engine: transcript -> structured SOAP note.

Primary path: a local Ollama model (free, runs on-device — see project
README for the 100% free/local stack rationale), prompted with strict
few-shot instructions to return SOAP JSON, which is then validated
against the `SOAPNote` Pydantic schema.

Fallback path: if Ollama isn't running / no model is pulled, we fall back
to a lightweight rule-based extractor so `/upload-audio` still returns a
usable (if less clinically nuanced) SOAP note instead of a 500 error.
"""

import json
import os
import re
import warnings

from schemas import SOAPNote

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """You are a clinical scribe assistant. Read the transcript of a
doctor-patient conversation and produce a SOAP note.

Rules:
- Only extract medically relevant information; ignore small talk/greetings.
- Subjective: symptoms and history reported by the patient, in their own context.
- Objective: vital signs / exam findings explicitly mentioned (state 'Not documented' if none).
- Assessment: the clinician's diagnosis or clinical impression.
- Plan: prescribed medications, tests, follow-up instructions.
- Respond with ONLY a JSON object with exactly these keys:
  "subjective", "objective", "assessment", "plan" (all strings, no nesting, no markdown).
"""


def _first_sentences(text, count=2):
    parts = [s.strip() for s in re.split(r'[.?!]\s*', text) if s.strip()]
    return ' '.join(parts[:count]) if parts else text.strip()


def _rule_based_soap(transcript):
    """Deterministic fallback used when the local LLM is unavailable."""
    transcript = transcript.strip() or 'No transcript available.'
    subjective = _first_sentences(transcript, 2)

    if re.search(r'\b(fevers?|fever|cough|sore throat|headache|fatigue|pain|chest|shortness of breath|dyspnea|nausea|vomiting|diarrhea|weakness)\b', transcript, re.I):
        assessment = 'Symptoms are consistent with an acute infection; follow-up and supportive care are recommended.'
    elif re.search(r'\b(diabetes|hypertension|asthma|COPD|arthritis|depression|anxiety)\b', transcript, re.I):
        assessment = 'Chronic disease management with current symptoms noted; optimize therapy and monitor closely.'
    else:
        assessment = 'Clinical impression is non-specific; further evaluation is recommended.'

    return {
        'subjective': subjective,
        'objective': 'Objective exam findings are unavailable in the transcript; obtain vitals and physical exam data as needed.',
        'assessment': assessment,
        'plan': 'Recommend follow-up, symptomatic relief, and diagnostics as clinically indicated.',
    }


def _clean_soap_dict(raw):
    """Normalize keys/None values so it always validates against SOAPNote."""
    if not isinstance(raw, dict):
        raise ValueError("LLM did not return a JSON object")
    normalized = {k.lower(): v for k, v in raw.items()}
    cleaned = {}
    for field in ("subjective", "objective", "assessment", "plan"):
        value = normalized.get(field)
        cleaned[field] = str(value).strip() if value else "Not documented."
    return cleaned


def _llm_soap(transcript):
    import ollama  # imported lazily so the module still loads without it installed

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Transcript:\n{transcript}"},
        ],
        format="json",
        options={"temperature": 0.1},
    )
    content = response["message"]["content"]
    raw = json.loads(content)
    cleaned = _clean_soap_dict(raw)
    validated = SOAPNote(**cleaned)  # raises if the schema doesn't validate
    return validated.model_dump()


def generate_soap(transcript):
    transcript = (transcript or "").strip()
    if not transcript:
        return _rule_based_soap(transcript)

    try:
        return _llm_soap(transcript)
    except Exception as exc:
        warnings.warn(
            f"Ollama SOAP generation unavailable/failed ({exc}); "
            "falling back to rule-based SOAP extraction. Run `ollama pull "
            f"{OLLAMA_MODEL}` and make sure the Ollama server is running to enable LLM synthesis."
        )
        return _rule_based_soap(transcript)


if __name__ == "__main__":
    sample = (
        "Doctor: What brings you in today? Patient: I've had a fever and "
        "sore throat for three days. Doctor: Let's check your temperature."
    )
    print(json.dumps(generate_soap(sample), indent=2))
