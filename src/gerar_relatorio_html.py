from pathlib import Path
import pandas as pd
from tratamento_dados import carregar_base

BASE_DIR = Path(__file__).resolve().parents[1]
OUT = BASE_DIR / "reports" / "relatorio_executivo_agroenso.html"

def fmt_int(x): return f"{x:,.0f}".replace(",", ".")
def fmt_money(x): return "R$ " + f"{x:,.0f}".replace(",", ".")

def main():
    df = carregar_base()
    ens = pd.read_csv(BASE_DIR / "data" / "dados_enso_referencia.csv")
    top = df.sort_values(["risco_comercial_score", "irea_indice_risco_enso_agricola"], ascending=False).head(15)
    mun = df.groupby("municipio", as_index=False).agg(
        irea=("irea_indice_risco_enso_agricola", "mean"),
        risco_entrega_sc=("risco_entrega_sc", "sum"),
        producao_revisada_sc=("producao_revisada_sc", "sum"),
    ).sort_values("irea", ascending=False)
    cards = {
        "IREA médio": f"{df['irea_indice_risco_enso_agricola'].mean():.1f}",
        "Municípios": str(df['municipio'].nunique()),
        "Produção esperada": fmt_int(df['producao_esperada_sc'].sum()) + " sc",
        "Produção revisada": fmt_int(df['producao_revisada_sc'].sum()) + " sc",
        "Risco entrega potencial": fmt_int(df['risco_entrega_sc'].sum()) + " sc",
        "Prob. El Niño média": f"{ens['prob_el_nino'].mean()*100:.0f}%",
    }
    card_html = "".join(f"<div class='card'><span>{k}</span><strong>{v}</strong></div>" for k,v in cards.items())
    rows = "".join(
        f"<tr><td>{r.municipio}</td><td>{r.cultura}</td><td>{r.mes}</td><td>{r.fase_cultura}</td><td>{r.irea_indice_risco_enso_agricola:.1f}</td><td>{r.risco_produtivo}</td><td>{r.risco_comercial}</td><td>{fmt_int(r.risco_entrega_sc)}</td><td>{r.recomendacao}</td></tr>"
        for _, r in top.iterrows()
    )
    mun_rows = "".join(
        f"<tr><td>{r.municipio}</td><td>{r.irea:.1f}</td><td>{fmt_int(r.producao_revisada_sc)}</td><td>{fmt_int(r.risco_entrega_sc)}</td></tr>"
        for _, r in mun.iterrows()
    )
    html = f"""
<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'>
<title>Relatório Executivo AgroENSO Risk IA</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 0; color: #17202A; background: #F6FAF6; }}
.header {{ background: linear-gradient(135deg,#0F3D27,#1E6B3A); color:white; padding: 34px 42px; }}
.header h1 {{ margin:0; font-size:34px; }} .header p {{ margin:8px 0 0 0; opacity:.95; }}
.wrap {{ padding: 28px 42px; }}
h2 {{ color: #123B22; border-bottom: 2px solid #D9E8D9; padding-bottom: 7px; margin-top: 28px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 22px 0; }}
.card {{ background:white; border:1px solid #DDE7DD; border-radius:14px; padding:16px; box-shadow:0 1px 5px rgba(0,0,0,.05); }}
.card span {{ display:block; color:#60706A; font-size:13px; }} .card strong {{ display:block; font-size:24px; margin-top:8px; color:#123B22; }}
table {{ width:100%; border-collapse:collapse; background:white; margin-top:12px; }}
th,td {{ border:1px solid #E1E7E1; padding:8px; font-size:12px; vertical-align:top; }} th {{ background:#EAF5EA; color:#123B22; }}
.note {{ background:#FFF7E6; border-left:5px solid #D98C00; padding:13px; border-radius:8px; }}
.good {{ background:#ECF8EE; border-left:5px solid #1F7A43; padding:13px; border-radius:8px; }}
code {{ background:#EDF2EE; padding:2px 5px; border-radius:4px; }}
</style></head><body>
<div class='header'><h1>AgroENSO Risk IA</h1><p>Relatório executivo automático da POC executável</p><p>Pedro Vinicius Gomes dos Santos | RM 571446 | 1TIAOB-2026</p></div>
<div class='wrap'>
<p>O projeto monitora o ENSO, com foco na fase El Niño, e traduz esse sinal climático em risco produtivo e comercial para soja e milho safrinha em Goiás.</p>
<div class='grid'>{card_html}</div>
<h2>Leitura central</h2>
<div class='note'>O sistema não promete prever El Niño do zero. A proposta é organizar sinais climáticos, agrícolas e comerciais para apoiar decisão de vistoria, revisão de produtividade, venda futura e gestão de risco de entrega.</div>
<h2>Fluxo da solução</h2>
<p><code>ENSO</code> → <code>probabilidade de El Niño</code> → <code>chuva e temperatura em Goiás</code> → <code>fase da cultura</code> → <code>risco produtivo</code> → <code>risco comercial</code> → <code>recomendação da IA</code></p>
<h2>Ranking municipal</h2>
<table><thead><tr><th>Município</th><th>IREA médio</th><th>Produção revisada sc</th><th>Risco entrega potencial sc</th></tr></thead><tbody>{mun_rows}</tbody></table>
<h2>Top alertas gerados pela IA</h2>
<table><thead><tr><th>Município</th><th>Cultura</th><th>Mês</th><th>Fase</th><th>IREA</th><th>Risco produtivo</th><th>Risco comercial</th><th>Risco entrega sc</th><th>Recomendação</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Como demonstrar para a banca</h2>
<div class='good'><ol><li>Executar <b>INICIAR_PROJETO.bat</b> ou <b>00_MENU_PROFISSIONAL.bat</b>.</li><li>Escolher a opção 1 para rodar tudo.</li><li>Mostrar validação, treinamento, relatório HTML e dashboard.</li><li>No dashboard, explicar as abas Resumo, ENSO, Goiás, Agrícola, Comercial e Alertas IA.</li></ol></div>
</div></body></html>
"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Relatório HTML gerado: {OUT}")

if __name__ == "__main__": main()
