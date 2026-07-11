import re


def _first_sentences(text, count=2):
    parts = [s.strip() for s in re.split(r'[.?!]\s*', text) if s.strip()]
    return ' '.join(parts[:count]) if parts else text.strip()


def generate_soap(transcript):
    transcript = transcript.strip() or 'No transcript available.'
    subjective = _first_sentences(transcript, 2)

    if re.search(r'\b(fevers?|fever|cough|sore throat|headache|fatigue|pain|chest|shortness of breath|dyspnea|nausea|vomiting|diarrhea|weakness)\b', transcript, re.I):
        assessment = 'Symptoms are consistent with an acute infection; follow-up and supportive care are recommended.'
    elif re.search(r'\b(diabetes|hypertension|asthma|COPD|arthritis|depression|anxiety)\b', transcript, re.I):
        assessment = 'Chronic disease management with current symptoms noted; optimize therapy and monitor closely.'
    else:
        assessment = 'Clinical impression is non-specific; further evaluation is recommended.'

    objective = 'Objective exam findings are unavailable in the transcript; obtain vitals and physical exam data as needed.'
    plan = 'Recommend follow-up, symptomatic relief, and diagnostics as clinically indicated.'

    return {
        'subjective': subjective,
        'objective': objective,
        'assessment': assessment,
        'plan': plan,
    }
