@echo off

echo =====================================
echo Setting up Ambient Clinical Scribe
echo =====================================

python -m venv .venv

call .venv\Scripts\activate

pip install -r requirements.txt

echo.
echo Setup Complete!
pause