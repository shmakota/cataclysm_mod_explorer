@echo off

REM Check if venv exists
IF NOT EXIST "venv" (
    python -m venv venv
)

REM Activate virtual environment
CALL venv\Scripts\activate.bat

REM Install requirements
pip install -r requirements.txt

REM Run the script
python mod_viewer.py

