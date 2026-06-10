from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "base_agroenso_risk_goias.csv"

RISCO_ORDEM = {"Baixo": 1, "Moderado": 2, "Alto": 3, "Crítico": 4}


def carregar_base() -> pd.DataFrame:
    """Carrega a base estruturada da POC e prepara campos para análise."""
    df = pd.read_csv(DATA_PATH)
    df["data_referencia"] = pd.to_datetime(df["data_referencia"])
    df["percentual_vendido_pct"] = df["percentual_vendido"] * 100
    df["risco_produtivo_nivel"] = df["risco_produtivo"].map(RISCO_ORDEM)
    df["risco_comercial_nivel"] = df["risco_comercial"].map(RISCO_ORDEM)
    df["quebra_estimativa_sc_ha"] = df["produtividade_esperada_sc_ha"] - df["produtividade_revisada_sc_ha"]
    return df


def resumo_executivo(df: pd.DataFrame) -> dict:
    return {
        "linhas": len(df),
        "municipios": df["municipio"].nunique(),
        "culturas": df["cultura"].nunique(),
        "irea_medio": round(df["irea_indice_risco_enso_agricola"].mean(), 1),
        "producao_esperada_sc": round(df["producao_esperada_sc"].sum(), 0),
        "producao_revisada_sc": round(df["producao_revisada_sc"].sum(), 0),
        "risco_entrega_sc": round(df["risco_entrega_sc"].sum(), 0),
    }


if __name__ == "__main__":
    base = carregar_base()
    print(base.head())
    print(resumo_executivo(base))
