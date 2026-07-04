@echo off

echo =====================================
echo Setting up Ambient Clinical Scribe
echo =====================================
echo.

REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

echo.
echo =====================================
echo Setup Complete!
echo Run run.bat to start the application.
echo =====================================
pause