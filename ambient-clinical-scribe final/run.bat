@echo off
if not exist ".venv\Scripts\activate" (
    echo [ERROR] Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate

echo Starting FastAPI Server on http://localhost:8000 ...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
