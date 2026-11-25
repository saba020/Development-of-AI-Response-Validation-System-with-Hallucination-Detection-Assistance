@echo off
echo ========================================================
echo   Starting AI Response Quality Evaluator FastAPI Backend
echo ========================================================
cd /d "%~dp0"
python -m uvicorn api:app --reload --port 8000
pause
