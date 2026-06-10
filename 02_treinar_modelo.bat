@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Treinando modelo de Machine Learning...
python src\modelo_risco.py
pause
