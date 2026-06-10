"""Treinamento do modelo introdutório de Machine Learning para a POC.

O modelo usa Random Forest para classificar risco produtivo a partir de variáveis ENSO,
climáticas, sensoriamento simulado, fase da lavoura e exposição comercial.
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "base_agroenso_risk_goias.csv"
MODEL_PATH = BASE_DIR / "assets" / "modelo_risco_produtivo.joblib"
REPORT_PATH = BASE_DIR / "outputs" / "metricas_modelo.txt"

FEATURES = [
    "nino34", "oni", "prob_el_nino", "chuva_7d_mm", "chuva_15d_mm", "chuva_30d_mm",
    "anomalia_temp_c", "temperatura_media_c", "dias_sem_chuva", "umidade_solo_pct",
    "ndvi_atual", "variacao_ndvi_pct", "percentual_vendido"
]


def treinar_modelo():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df["risco_produtivo"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    counts = pd.Series(y).value_counts()
    usar_stratify = pd.Series(y_encoded).value_counts().min() >= 2
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.25, random_state=42,
        stratify=y_encoded if usar_stratify else None
    )

    modelo = RandomForestClassifier(
        n_estimators=300, random_state=42, max_depth=8, class_weight="balanced"
    )
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)

    acc = accuracy_score(y_test, pred)
    labels_presentes = sorted(set(y_test) | set(pred))
    nomes_presentes = [le.classes_[i] for i in labels_presentes]

    relatorio = []
    relatorio.append("AGROENSO RISK IA - MÉTRICAS DO MODELO\n")
    relatorio.append("Modelo: Random Forest Classifier\n")
    relatorio.append(f"Acurácia na amostra de teste: {acc:.3f}\n\n")
    relatorio.append("Distribuição de classes na base completa:\n")
    relatorio.append(counts.to_string())
    relatorio.append("\n\nRelatório de classificação na amostra de teste:\n")
    relatorio.append(classification_report(y_test, pred, labels=labels_presentes, target_names=nomes_presentes, zero_division=0))
    relatorio.append("\nMatriz de confusão da amostra de teste:\n")
    relatorio.append(str(confusion_matrix(y_test, pred, labels=labels_presentes)))
    relatorio.append("\n\nObservação metodológica:\n")
    relatorio.append("Como a base é uma POC simulada, algumas classes extremas podem ter baixa frequência. A função do modelo é demonstrar o fluxo de IA e a classificação de risco, não substituir validação agronômica real.\n")
    relatorio.append("\nImportância das variáveis:\n")
    importancias = pd.DataFrame({"variavel": FEATURES, "importancia": modelo.feature_importances_}).sort_values("importancia", ascending=False)
    relatorio.append(importancias.to_string(index=False))

    MODEL_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    joblib.dump({"modelo": modelo, "label_encoder": le, "features": FEATURES}, MODEL_PATH)
    REPORT_PATH.write_text("".join(relatorio), encoding="utf-8")

    print("Modelo treinado com sucesso.")
    print(f"Acurácia: {acc:.3f}")
    print(f"Modelo salvo em: {MODEL_PATH}")
    print(f"Relatório salvo em: {REPORT_PATH}")


if __name__ == "__main__":
    treinar_modelo()
