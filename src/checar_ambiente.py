import sys
from pathlib import Path

print("Python:", sys.version)
print("Pasta do projeto:", Path(__file__).resolve().parents[1])
print("OK: ambiente básico carregado.")
try:
    import pandas, sklearn, streamlit, plotly
    print("OK: dependências principais disponíveis.")
except Exception as e:
    print("ATENÇÃO: alguma dependência não está instalada:", e)
    print("Execute: python -m pip install -r requirements.txt")
