@echo off
echo Starting AI Influencer Factory...

cd /d %~dp0

if not exist venv\Scripts\activate (
  echo Virtual environment not found. Create one with: python -m venv venv
  pause
  exit /b 1
)

call venv\Scripts\activate

echo Launching Content Engine...
python main.py

pause
