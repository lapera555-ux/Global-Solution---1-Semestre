from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

GITHUB_URL = 'https://github.com/lapera555-ux/Global-Solution---1-Semestre.git'
YOUTUBE_URL = 'https://youtu.be/_QISHjaNjZc?si=8stXluBzlJo_yhMA'
import plotly.graph_objects as go
from tratamento_dados import carregar_base
from motor_recomendacao import gerar_alerta, matriz_decisao

BASE_DIR = Path(__file__).resolve().parents[1]
ENSO_PATH = BASE_DIR / "data" / "dados_enso_referencia.csv"
PDF_PATH = BASE_DIR / "docs" / "projeto_agroenso_risk_ia.pdf"
REPORT_PATH = BASE_DIR / "reports" / "relatorio_executivo_agroenso.html"

st.set_page_config(page_title="AgroENSO Risk IA", page_icon="🌎", layout="wide")

st.markdown("""
<style>
.main {background-color:#FAFCFA;}
.hero {padding: 1.4rem 1.6rem; border-radius: 1.2rem; background: linear-gradient(135deg,#0F3D27,#1E6B3A); color: white; margin-bottom: 1rem;}
.hero h1 {font-size: 2.3rem; margin:0; color:white;}
.hero p {font-size: 1.02rem; opacity:.96; margin:.4rem 0 0 0;}
.card {padding: 1rem; border-radius: 1rem; border: 1px solid #DDE7DD; background: white; box-shadow: 0 1px 4px rgba(0,0,0,.04);}
.kpi {font-size: .82rem; color:#596B61; margin-bottom:.2rem;}
.kpivalue {font-size:1.6rem; font-weight:800; color:#123B22;}
.callout {padding: 1rem; border-radius: .9rem; border-left: 5px solid #D98C00; background:#FFF8E8; color:#2E2E2E;}
.successbox {padding: 1rem; border-radius: .9rem; border-left: 5px solid #1F7A43; background:#EEF8EF;}
.small {color:#667085; font-size:.92rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    df = carregar_base()
    enso = pd.read_csv(ENSO_PATH)
    return df, enso

def fmt_int(x):
    return f"{x:,.0f}".replace(',', '.')

def risco_cor(r):
    if r == "Crítico": return "🔴"
    if r == "Alto": return "🟠"
    if r == "Moderado": return "🟡"
    return "🟢"

df, enso = load()

st.markdown("""
<div class="hero">
  <h1>AgroENSO Risk IA</h1>
  <p>Satélites, clima e inteligência artificial para antecipação de riscos produtivos e comerciais em soja e milho safrinha em Goiás.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("Leitura correta do projeto", expanded=True):
    st.markdown("""
Este sistema não tenta prever o El Niño do zero. A proposta é monitorar o ENSO, interpretar a fase El Niño e cruzar esse sinal climático com Goiás, cultura, fase da lavoura, produtividade esperada, percentual vendido e sensor de solo simulado.

Fluxo lógico: ENSO → probabilidade de El Niño → chuva e temperatura → risco em soja/milho → produtividade revisada → risco comercial → recomendação para produtor e consultoria.
""")

st.sidebar.title("Filtros da análise")
municipios = st.sidebar.multiselect("Municípios", sorted(df["municipio"].unique()), default=sorted(df["municipio"].unique()))
culturas = st.sidebar.multiselect("Culturas", sorted(df["cultura"].unique()), default=sorted(df["cultura"].unique()))
meses = st.sidebar.multiselect("Meses", sorted(df["mes"].unique()), default=sorted(df["mes"].unique()))
riscos = st.sidebar.multiselect("Risco produtivo", ["Baixo", "Moderado", "Alto", "Crítico"], default=["Baixo", "Moderado", "Alto", "Crítico"])
st.sidebar.divider()
st.sidebar.markdown("Aluno: Pedro Vinicius Gomes dos Santos  \nRM: 571446  \nTurma: 1TIAOB-2026")

f = df[df["municipio"].isin(municipios) & df["cultura"].isin(culturas) & df["mes"].isin(meses) & df["risco_produtivo"].isin(riscos)]
if f.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

tabs = st.tabs(["Resumo", "ENSO", "Goiás", "Agrícola", "Comercial", "Alertas IA", "Execução", "Base"])

with tabs[0]:
    st.subheader("Visão executiva")
    k1,k2,k3,k4,k5 = st.columns(5)
    metrics = [
        (k1, "IREA médio", f"{f['irea_indice_risco_enso_agricola'].mean():.1f}"),
        (k2, "Produção esperada", fmt_int(f['producao_esperada_sc'].sum()) + " sc"),
        (k3, "Produção revisada", fmt_int(f['producao_revisada_sc'].sum()) + " sc"),
        (k4, "Risco entrega potencial", fmt_int(f['risco_entrega_sc'].sum()) + " sc"),
        (k5, "Média vendida", f"{f['percentual_vendido'].mean()*100:.0f}%"),
    ]
    for col, label, value in metrics:
        with col:
            st.markdown(f"<div class='card'><div class='kpi'>{label}</div><div class='kpivalue'>{value}</div></div>", unsafe_allow_html=True)
    st.write("")
    c1,c2 = st.columns([1.25, .85])
    with c1:
        rank = f.groupby("municipio", as_index=False).agg(
            irea=("irea_indice_risco_enso_agricola", "mean"),
            risco_entrega_sc=("risco_entrega_sc", "sum"),
            prod_rev=("producao_revisada_sc", "sum"),
        ).sort_values("irea", ascending=False)
        st.plotly_chart(px.bar(rank, x="municipio", y="irea", text_auto='.1f', hover_data=["risco_entrega_sc", "prod_rev"], title="Ranking de risco por município"), use_container_width=True)
    with c2:
        dist = f["risco_produtivo"].value_counts().rename_axis("risco").reset_index(name="qtde")
        st.plotly_chart(px.pie(dist, names="risco", values="qtde", hole=.48, title="Distribuição do risco produtivo"), use_container_width=True)
    pior = f.sort_values(["risco_comercial_score","irea_indice_risco_enso_agricola"], ascending=False).iloc[0]
    st.markdown(f"<div class='callout'><b>Principal alerta:</b> {pior.municipio}, {pior.cultura}, {pior.mes}. IREA {pior.irea_indice_risco_enso_agricola:.1f}, risco produtivo {pior.risco_produtivo} e risco comercial {pior.risco_comercial}. Recomendação: {pior.recomendacao}</div>", unsafe_allow_html=True)

with tabs[1]:
    st.subheader("Painel ENSO")
    st.markdown("ENSO é o sistema climático completo. El Niño é a fase quente. O projeto monitora o sinal climático e o traduz para risco agrícola regional.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=enso["mes"], y=enso["prob_el_nino"]*100, mode="lines+markers", name="Probabilidade El Niño (%)"))
    fig.add_trace(go.Scatter(x=enso["mes"], y=enso["prob_neutro"]*100, mode="lines+markers", name="Probabilidade Neutro (%)"))
    fig.add_trace(go.Scatter(x=enso["mes"], y=enso["prob_la_nina"]*100, mode="lines+markers", name="Probabilidade La Niña (%)"))
    fig.update_layout(title="Probabilidades ENSO usadas na POC", yaxis_title="Probabilidade (%)")
    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.line(enso, x="mes", y=["nino34","oni"], markers=True, title="Niño 3.4 e ONI")
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(enso, use_container_width=True)

with tabs[2]:
    st.subheader("Goiás e sudoeste goiano")
    mapa = f.groupby(["municipio","latitude","longitude","regiao_operacional"], as_index=False).agg(
        irea=("irea_indice_risco_enso_agricola", "mean"),
        risco_entrega_sc=("risco_entrega_sc", "sum"),
    )
    st.map(mapa.rename(columns={"latitude":"lat", "longitude":"lon"}), latitude="lat", longitude="lon", size="irea")
    st.markdown("<div class='successbox'>O recorte usa Goiás inteiro, mas a leitura prática prioriza municípios relevantes para soja e milho safrinha, principalmente no sudoeste goiano.</div>", unsafe_allow_html=True)
    st.dataframe(mapa.sort_values("irea", ascending=False), use_container_width=True)

with tabs[3]:
    st.subheader("Risco agrícola")
    prod = f.groupby(["municipio","cultura"], as_index=False).agg(
        produtividade_esperada=("produtividade_esperada_sc_ha","mean"),
        produtividade_revisada=("produtividade_revisada_sc_ha","mean"),
        chuva_30d=("chuva_30d_mm","mean"),
        anomalia_temp=("anomalia_temp_c","mean"),
    )
    st.plotly_chart(px.bar(prod, x="municipio", y=["produtividade_esperada","produtividade_revisada"], color="cultura", barmode="group", title="Produtividade esperada x revisada"), use_container_width=True)
    c1,c2 = st.columns(2)
    with c1:
        clim = f.groupby("mes", as_index=False).agg(chuva_30d_mm=("chuva_30d_mm","mean"), dias_sem_chuva=("dias_sem_chuva","mean"))
        st.plotly_chart(px.line(clim, x="mes", y=["chuva_30d_mm","dias_sem_chuva"], markers=True, title="Chuva acumulada e dias sem chuva"), use_container_width=True)
    with c2:
        temp = f.groupby("mes", as_index=False).agg(anomalia_temp_c=("anomalia_temp_c","mean"), umidade_solo_pct=("umidade_solo_pct","mean"))
        st.plotly_chart(px.line(temp, x="mes", y=["anomalia_temp_c","umidade_solo_pct"], markers=True, title="Anomalia de temperatura e solo simulado"), use_container_width=True)

with tabs[4]:
    st.subheader("Risco comercial")
    comercial = f.groupby(["municipio","cultura"], as_index=False).agg(
        volume_vendido_sc=("volume_vendido_sc","sum"),
        producao_revisada_sc=("producao_revisada_sc","sum"),
        risco_entrega_sc=("risco_entrega_sc","sum"),
        percentual_vendido=("percentual_vendido","mean"),
        valor_producao_revisada_rs=("valor_producao_revisada_rs","sum"),
    )
    st.plotly_chart(px.scatter(comercial, x="percentual_vendido", y="risco_entrega_sc", size="producao_revisada_sc", color="cultura", hover_name="municipio", title="Percentual vendido x risco de entrega potencial"), use_container_width=True)
    st.dataframe(comercial, use_container_width=True)
    st.markdown("<p class='small'>Risco de entrega potencial representa o volume afetado pela revisão de produtividade, não uma inadimplência real.</p>", unsafe_allow_html=True)

with tabs[5]:
    st.subheader("Alertas automáticos em linguagem de consultoria")
    top = f.sort_values(["risco_comercial_score","irea_indice_risco_enso_agricola"], ascending=False).head(12)
    for _, row in top.iterrows():
        st.info(f"{risco_cor(row.risco_produtivo)} " + gerar_alerta(row) + "\n\nDecisão sugerida: " + matriz_decisao(row['risco_produtivo'], row['risco_comercial']))

with tabs[6]:
    st.subheader("Execução e entrega")
    st.markdown("""
Para demonstrar o projeto no vídeo, rode o arquivo `00_MENU_PROFISSIONAL.bat` e use a opção 1. O sistema valida a estrutura, treina o modelo, gera relatório executivo e abre este dashboard.
""")
    c1,c2,c3 = st.columns(3)
    with c1:
        if PDF_PATH.exists():
            st.download_button("Baixar PDF do projeto", data=PDF_PATH.read_bytes(), file_name="projeto_agroenso_risk_ia.pdf", mime="application/pdf")
    with c2:
        if REPORT_PATH.exists():
            st.download_button("Baixar relatório HTML", data=REPORT_PATH.read_bytes(), file_name="relatorio_executivo_agroenso.html", mime="text/html")
    with c3:
        st.download_button("Baixar base completa", data=df.to_csv(index=False).encode("utf-8"), file_name="base_agroenso_risk_goias.csv", mime="text/csv")
    st.code("00_MENU_PROFISSIONAL.bat\n05_executar_tudo.bat\npython -m streamlit run src/dashboard.py", language="bash")

with tabs[7]:
    st.subheader("Base estruturada")
    st.dataframe(f, use_container_width=True)
    st.download_button("Baixar CSV filtrado", f.to_csv(index=False).encode("utf-8"), "agroenso_risk_filtrado.csv", "text/csv")
