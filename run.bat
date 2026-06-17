@echo off

call .venv\Scripts\activate

echo Starting FastAPI Server...

python -m uvicorn main:app --reload

pause