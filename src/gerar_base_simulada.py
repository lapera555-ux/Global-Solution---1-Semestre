from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA = BASE_DIR / "data" / "base_agroenso_risk_goias.csv"

if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print("Base de simulação já gerada e disponível em:", DATA)
    print("Linhas:", len(df), "| Municípios:", df['municipio'].nunique(), "| Culturas:", ', '.join(df['cultura'].unique()))
