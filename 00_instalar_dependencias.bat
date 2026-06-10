@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Instalando dependencias do AgroENSO Risk IA...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Erro na instalacao. Verifique se o Python esta instalado e no PATH.
  pause
  exit /b 1
)
echo Dependencias instaladas com sucesso.
pause
