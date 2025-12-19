@echo off
echo Starting AI Influencer Factory...

cd /d %~dp0

call venv\Scripts\activate

echo Launching Content Engine...
python main.py

pause
