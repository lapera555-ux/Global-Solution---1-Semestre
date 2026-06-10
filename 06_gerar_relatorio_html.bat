@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Gerando relatorio executivo HTML...
python src\gerar_relatorio_html.py
start "" "reports\relatorio_executivo_agroenso.html"
pause
