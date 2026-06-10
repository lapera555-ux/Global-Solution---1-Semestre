@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AgroENSO Risk IA - Execucao Completa
color 0A

echo ============================================================
echo        AGROENSO RISK IA - EXECUCAO COMPLETA RECOMENDADA
echo ============================================================
echo.
echo Esta rotina prepara e demonstra a POC para a banca.
echo.

echo [0/5] Verificando Python...
python --version
if errorlevel 1 goto erro_python

echo.
echo [1/5] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto erro

echo.
echo [2/5] Validando entrega, arquivos, links e base de dados...
python src\validar_entrega.py
echo.
echo Validacao concluida. Esta etapa e informativa e nao bloqueia a demonstracao.

echo.
echo [3/5] Treinando modelo de Machine Learning...
python src\modelo_risco.py
if errorlevel 1 goto erro

echo.
echo [4/5] Gerando relatorio executivo HTML...
python src\gerar_relatorio_html.py
if errorlevel 1 goto erro

echo.
echo [5/5] Abrindo dashboard Streamlit...
echo O navegador deve abrir automaticamente. Se nao abrir, copie o link exibido no terminal.
python -m streamlit run src\dashboard.py
exit /b 0

:erro_python
echo.
echo ERRO: Python nao encontrado no PATH.
echo Instale Python 3.10+ e marque a opcao "Add Python to PATH".
pause
exit /b 1

:erro
echo.
echo ERRO: a execucao foi interrompida em uma etapa operacional.
echo Veja a mensagem acima. Se for dependencia, rode 00_instalar_dependencias.bat e tente novamente.
pause
exit /b 1
