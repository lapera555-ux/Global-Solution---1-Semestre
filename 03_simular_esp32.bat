@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Simulando leituras do ESP32...
python src\esp32_simulado.py
pause
