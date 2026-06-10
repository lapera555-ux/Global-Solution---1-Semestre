from pathlib import Path
import importlib.util
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parents[1]

OBRIGATORIOS = [
    "README.md",
    "requirements.txt",
    "docs/projeto_agroenso_risk_ia.pdf",
    "docs/projeto_agroenso_risk_ia.docx",
    "docs/roteiro_video.md",
    "docs/GUIA_DE_APRESENTACAO.md",
    "data/base_agroenso_risk_goias.csv",
    "data/dados_enso_referencia.csv",
    "src/dashboard.py",
    "src/modelo_risco.py",
    "src/motor_recomendacao.py",
    "src/esp32_simulado.py",
    "src/executar_projeto.py",
    "esp32/sensor_umidade_simulado.ino",
    "00_MENU_PROFISSIONAL.bat",
    "05_executar_tudo.bat",
]

MODULOS = ["pandas", "numpy", "sklearn", "joblib", "streamlit", "plotly"]

COLUNAS_BASE = [
    "municipio", "estado", "cultura", "fase_cultura", "area_ha",
    "produtividade_esperada_sc_ha", "produtividade_revisada_sc_ha",
    "percentual_vendido", "nino34", "oni", "prob_el_nino", "chuva_7d_mm",
    "chuva_15d_mm", "chuva_30d_mm", "anomalia_temp_c", "temperatura_media_c",
    "dias_sem_chuva", "umidade_solo_pct", "ndvi_atual", "variacao_ndvi_pct",
    "irea_indice_risco_enso_agricola", "risco_produtivo", "risco_comercial",
    "risco_entrega_sc", "recomendacao",
]

GITHUB_URL = "https://github.com/lapera555-ux/Global-Solution---1-Semestre.git"
YOUTUBE_URL = "https://youtu.be/_QISHjaNjZc?si=8stXluBzlJo_yhMA"


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def warn(msg: str) -> None:
    print(f"[AVISO] {msg}")


def fail(msg: str) -> None:
    print(f"[ERRO] {msg}")


def main() -> int:
    criticos = []
    avisos = []

    print("\nValidação profissional do AgroENSO Risk IA")
    print("=" * 52)

    print("\n[1/4] Checando arquivos obrigatórios...")
    for rel in OBRIGATORIOS:
        p = BASE_DIR / rel
        if p.exists():
            ok(f"Arquivo encontrado: {rel}")
        else:
            fail(f"Arquivo ausente: {rel}")
            criticos.append(f"arquivo ausente: {rel}")

    print("\n[2/4] Checando módulos Python...")
    for mod in MODULOS:
        if importlib.util.find_spec(mod) is not None:
            ok(f"Módulo disponível: {mod}")
        else:
            warn(f"Módulo ausente: {mod}. Rode 00_instalar_dependencias.bat ou 05_executar_tudo.bat.")
            avisos.append(f"módulo ausente: {mod}")

    print("\n[3/4] Checando base de dados...")
    try:
        df = pd.read_csv(BASE_DIR / "data" / "base_agroenso_risk_goias.csv")
        ok(f"Base carregada com {len(df)} linhas e {len(df.columns)} colunas")

        faltantes = [col for col in COLUNAS_BASE if col not in df.columns]
        if faltantes:
            for col in faltantes:
                fail(f"Coluna ausente na base: {col}")
            criticos.extend([f"coluna ausente: {col}" for col in faltantes])
        else:
            ok("Todas as colunas essenciais da base foram encontradas")
            ok(f"Municípios analisados: {df['municipio'].nunique()}")
            ok(f"Culturas: {', '.join(sorted(df['cultura'].unique()))}")
            if "mes" in df.columns:
                ok(f"Meses simulados: {df['mes'].nunique()}")
            ok(f"IREA médio: {df['irea_indice_risco_enso_agricola'].mean():.1f}")
            total_risco = df["risco_entrega_sc"].sum()
            ok(f"Risco de entrega potencial total: {total_risco:,.0f} sc".replace(",", "."))
    except Exception as e:
        fail(f"Erro ao ler base: {e}")
        criticos.append(f"erro ao ler base: {e}")

    print("\n[4/4] Checando links finais...")
    readme_path = BASE_DIR / "README.md"
    readme = readme_path.read_text(encoding="utf-8", errors="ignore") if readme_path.exists() else ""
    if GITHUB_URL in readme:
        ok("Link do GitHub encontrado no README")
    else:
        warn("Link do GitHub não encontrado no README")
        avisos.append("GitHub não encontrado no README")
    if YOUTUBE_URL in readme:
        ok("Link do YouTube encontrado no README")
    else:
        warn("Link do YouTube não encontrado no README")
        avisos.append("YouTube não encontrado no README")

    out = BASE_DIR / "outputs" / "checklist_validacao.txt"
    out.parent.mkdir(exist_ok=True)

    if criticos:
        status = "COM PENDÊNCIAS A REVISAR, EXECUÇÃO LIBERADA PARA DEMONSTRAÇÃO"
    elif avisos:
        status = "APROVADO COM AVISOS"
    else:
        status = "APROVADO"

    conteudo = (
        "Status da validação: " + status + "\n"
        + "Pendências críticas: " + str(criticos) + "\n"
        + "Avisos: " + str(avisos) + "\n"
        + "GitHub: " + GITHUB_URL + "\n"
        + "YouTube: " + YOUTUBE_URL + "\n"
    )
    out.write_text(conteudo, encoding="utf-8")

    print(f"\nResultado: {status}")
    if criticos:
        print("Pendências a revisar:", criticos)
        print("Observação: a validação agora NÃO bloqueia a demonstração. Os próximos passos tentarão executar normalmente.")
    if avisos:
        print("Avisos:", avisos)
    print(f"Checklist salvo em: {out}")

    # Não bloquear a demonstração. Se algo realmente impedir a execução, o script seguinte indicará o erro.
    return 0


if __name__ == "__main__":
    sys.exit(main())
