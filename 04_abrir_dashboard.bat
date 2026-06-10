@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Abrindo dashboard Streamlit...
python -m streamlit run src\dashboard.py
pause
