import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_soap(transcript):

    prompt = f"""
You are a medical AI assistant.

Convert the following doctor-patient transcript into a complete SOAP note.

IMPORTANT:
- Always fill all four sections.
- Never leave objective empty.
- Never leave assessment empty.
- Infer a reasonable clinical assessment from the symptoms.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations.

Transcript:
{transcript}

Return this exact JSON format:

{{
  "subjective": "",
  "objective": "",
  "assessment": "",
  "plan": ""
}}
"""

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    if response_text.startswith("```json"):
        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    return json.loads(response_text)