@echo off
setlocal enabledelayedexpansion

echo =====================================
echo   Ambient Clinical Scribe - Setup
echo =====================================
echo.

REM --- Check Python version -----------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found on PATH. Install Python 3.11 from
    echo         https://www.python.org/downloads/ and re-run this script.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo Detected Python %PYVER%
echo %PYVER% | findstr /b "3.11." >nul
if errorlevel 1 (
    echo [WARNING] This project targets Python 3.11. Python 3.13 does NOT
    echo           yet have prebuilt wheels for several ML packages here
    echo           ^(torch, whisper^) and the install below may fail to build.
    echo           If install fails, install Python 3.11 side-by-side and
    echo           re-run this script with that interpreter.
    echo.
)

REM --- Check FFmpeg (required by openai-whisper) --------------------------
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ffmpeg was not found on PATH. openai-whisper needs it to
    echo           decode audio. Install it from https://ffmpeg.org/download.html
    echo           or set FFMPEG_PATH in your .env file, then re-run setup.
    echo.
)

REM --- Check for Ollama (optional, enables LLM SOAP synthesis) ------------
where ollama >nul 2>&1
if errorlevel 1 (
    echo [INFO] Ollama was not found on PATH. The app will still run and
    echo        fall back to rule-based SOAP notes. For full LLM-generated
    echo        SOAP notes, install Ollama from https://ollama.com and run:
    echo            ollama pull llama3.2
    echo.
)

REM --- Create virtual environment -----------------------------------------
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists, reusing .venv
)

call .venv\Scripts\activate
if errorlevel 1 (
    echo [ERROR] Could not activate the virtual environment.
    pause
    exit /b 1
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing backend dependencies (this can take several minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed. See the error above.
    echo         Common fixes:
    echo           - Use Python 3.11 ^(not 3.13^)
    echo           - Re-run this script from an "x64 Native Tools" prompt
    echo             if a package needs to compile from source
    pause
    exit /b 1
)

REM --- Set up .env ----------------------------------------------------------
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
)

REM --- Build the ICD-10 RAG vector database --------------------------------
if not exist "icd_db" (
    echo.
    echo Building the ICD-10 vector database for RAG search ^(one-time, may
    echo take a few minutes to download the embedding model^)...
    python prepare_icd.py
    python build_icd_db.py
) else (
    echo ICD-10 vector database already exists, skipping build.
)

REM --- Optional: set up the React dashboard (frontend-react) ---------------
where npm >nul 2>&1
if not errorlevel 1 (
    if exist "frontend-react\package.json" (
        echo.
        echo Installing frontend-react dependencies...
        pushd frontend-react
        call npm install
        popd
    )
) else (
    echo [INFO] npm not found; skipping frontend-react ^(optional, WIP^) setup.
)

echo.
echo =====================================
echo   Setup Complete!
echo   Run run.bat to start the application.
echo   Then open http://localhost:8000
echo =====================================
pause
