@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Checando ambiente e validando estrutura do projeto...
python src\validar_entrega.py
pause
