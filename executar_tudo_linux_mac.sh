#!/bin/bash
set -e
cd "$(dirname "$0")"
echo "AgroENSO Risk IA - Execução completa"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 src/validar_entrega.py
python3 src/modelo_risco.py
python3 src/gerar_relatorio_html.py
python3 -m streamlit run src/dashboard.py
