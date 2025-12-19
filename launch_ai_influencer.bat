@echo off
echo Starting AI Influencer Factory...

cd /d %~dp0

REM Ensure Python is available
where python >nul 2>&1
if errorlevel 1 (
  echo Python is not on PATH. Install Python 3.10+ and re-run.
  pause
  exit /b 1
)

REM Create venv if missing
if not exist venv\Scripts\activate (
  echo Virtual environment not found. Creating one...
  python -m venv venv
)

call venv\Scripts\activate

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
  echo Installing dependencies from requirements.txt...
  pip install -r requirements.txt >nul
)

:menu
cls
echo === AI Influencer Factory Launcher ===
echo [1] Generate content (main.py)
echo [2] Open influencers folder for editing
echo [3] Regenerate prompts after edits
echo [4] Exit
set /p choice=Select option: 

if "%choice%"=="1" (
  echo Running content engine...
  python main.py
  if errorlevel 1 (
    echo Content engine failed. Check the console output above for details.
    pause
    goto menu
  )
  if exist outputs (
    echo Opening generated outputs folder...
    start "" "%cd%\outputs"
  )
  pause
  goto menu
)
if "%choice%"=="2" (
  start "" "%cd%\influencers"
  goto menu
)
if "%choice%"=="3" (
  echo Regenerating prompts...
  python main.py
  pause
  goto menu
)
if "%choice%"=="4" (
  exit /b 0
)

echo Invalid choice.
pause
goto menu
