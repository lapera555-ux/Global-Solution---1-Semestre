@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AgroENSO Risk IA - Menu Profissional
color 0A

:menu
cls
echo ============================================================
echo                 AGROENSO RISK IA
echo       MENU PROFISSIONAL DE EXECUCAO DA POC
echo ============================================================
echo.
echo Aluno: Pedro Vinicius Gomes dos Santos ^| RM 571446
echo Turma: 1TIAOB-2026 ^| Global Solution 2026.1
echo.
echo  [1] Executar tudo recomendado: instalar, validar, treinar, relatorio e dashboard
echo  [2] Instalar dependencias Python
echo  [3] Validar entrega e ambiente
echo  [4] Treinar modelo de Machine Learning
echo  [5] Gerar relatorio executivo HTML
echo  [6] Simular ESP32 no terminal
echo  [7] Abrir dashboard Streamlit
echo  [8] Abrir PDF do projeto
echo  [9] Abrir relatorio executivo HTML
echo  [10] Abrir guia de apresentacao
echo  [0] Sair
echo.
set /p opcao=Escolha uma opcao e pressione ENTER: 

if "%opcao%"=="1" call 05_executar_tudo.bat
if "%opcao%"=="2" call 00_instalar_dependencias.bat
if "%opcao%"=="3" call 01_checar_ambiente.bat
if "%opcao%"=="4" call 02_treinar_modelo.bat
if "%opcao%"=="5" call 06_gerar_relatorio_html.bat
if "%opcao%"=="6" call 03_simular_esp32.bat
if "%opcao%"=="7" call 04_abrir_dashboard.bat
if "%opcao%"=="8" start "" "docs\projeto_agroenso_risk_ia.pdf"
if "%opcao%"=="9" start "" "reports\relatorio_executivo_agroenso.html"
if "%opcao%"=="10" start "" "docs\GUIA_DE_APRESENTACAO.md"
if "%opcao%"=="0" exit

echo.
echo Voltando ao menu principal...
pause
goto menu
