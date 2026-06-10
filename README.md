# AGROENSO RISK IA

## Satélites, Clima e Inteligência Artificial para Antecipação de Riscos Produtivos e Comerciais em Soja e Milho Safrinha

**Aluno:** Pedro Vinicius Gomes dos Santos  
**RM:** 571446  
**Turma:** 1TIAOB-2026  
**Curso:** Inteligência Artificial  
**Global Solution 2026.1**  
**QUERO CONCORRER**

---

## 1. O que é o projeto

O AgroENSO Risk IA é uma prova de conceito executável que monitora o ENSO, com foco na fase El Niño, e transforma esse cenário climático em risco produtivo e comercial para soja e milho safrinha em Goiás.

O sistema não tenta prever o El Niño do zero. Ele organiza sinais climáticos, agrícolas e comerciais para apoiar decisão de vistoria, revisão de produtividade, venda futura e gestão de risco de entrega.

Fluxo lógico:

```txt
ENSO -> probabilidade de El Niño -> chuva e temperatura -> fase da cultura -> risco produtivo -> risco comercial -> recomendação
```

---

## 2. Como executar no Windows

A forma mais profissional é abrir o menu:

```txt
00_MENU_PROFISSIONAL.bat
```

Depois escolha:

```txt
1 - Executar projeto completo recomendado
```

Essa opção instala dependências, valida o projeto, treina o modelo, gera relatório executivo e abre o dashboard.

Também é possível executar direto:

```txt
05_executar_tudo.bat
```

---

## 3. Como executar manualmente

```bash
python -m pip install -r requirements.txt
python src/validar_entrega.py
python src/modelo_risco.py
python src/gerar_relatorio_html.py
python -m streamlit run src/dashboard.py
```

---

## 4. Recorte da POC

```txt
Estado: Goiás
Foco operacional: sudoeste goiano
Culturas: soja e milho safrinha
Municípios: 10
Horizonte: junho de 2026 a fevereiro de 2027
Sensor: ESP32 simulado
Modelo: Random Forest Classifier
Dashboard: Streamlit
```

---

## 5. Dados oficiais e premissas

### Referências usadas no projeto

- IRI Columbia: ENSO, Niño 3.4 e probabilidades de El Niño, Neutralidade e La Niña.
- NOAA/CPC: ENSO Diagnostic Discussion.
- WMO: contexto global sobre El Niño e alerta antecipado.
- CPTEC/INPE: referência brasileira para ENOS.
- CONAB: referência de safra e produtividade.
- ECMWF e CFSv2: referência de chuva acumulada e anomalia de temperatura.
- Rural Clima: referência aplicada de previsão para Goiás.
- Royal Rural: oferta e demanda de milho por estado.

### Premissas de simulação

```txt
Soja: 60 sc/ha
Milho safrinha: 115 sc/ha
Percentual vendido: 30%, 50% e 70%
Preço soja: R$ 120/sc
Preço milho: R$ 60/sc
Umidade do solo: simulada via ESP32
```

---

## 6. Estrutura do projeto

```txt
AgroENSO-Risk-IA-Executavel-Premium/
  00_MENU_PROFISSIONAL.bat
  05_executar_tudo.bat
  README.md
  requirements.txt
  data/
  src/
  docs/
  esp32/
  assets/
  reports/
  outputs/
```

---

## 7. O que demonstrar no vídeo

1. Abrir a pasta do projeto.
2. Mostrar o PDF em `docs/projeto_agroenso_risk_ia.pdf`.
3. Rodar `00_MENU_PROFISSIONAL.bat`.
4. Escolher a opção 1.
5. Mostrar a validação, treinamento do modelo e abertura do dashboard.
6. Explicar as abas: Resumo, ENSO, Goiás, Agrícola, Comercial e Alertas IA.
7. Mostrar um município com risco alto e a recomendação gerada.

---

## 8. Links finais da entrega

- Repositório GitHub: https://github.com/lapera555-ux/Global-Solution---1-Semestre.git
- Vídeo demonstrativo não listado: https://youtu.be/_QISHjaNjZc?si=8stXluBzlJo_yhMA

---

## 9. Documento principal

O PDF principal de entrega está em:

```txt
docs/projeto_agroenso_risk_ia.pdf
```

Ele contém capa, contextualização ENSO/El Niño, problema, solução, metodologia, arquitetura, Machine Learning, ESP32 simulado, dashboard, resultados esperados, limitações, conclusão e referências.


---

## 10. Execução profissional

Para a banca, a forma mais simples é abrir:

```txt
INICIAR_PROJETO.bat
```

ou diretamente:

```txt
00_MENU_PROFISSIONAL.bat
```

A opção recomendada é a opção 1 do menu. Ela executa o fluxo completo:

```txt
instalação de dependências
↓
validação da entrega
↓
treinamento do modelo
↓
geração do relatório HTML
↓
abertura do dashboard Streamlit
```

---

## 11. Diferencial técnico

O projeto não é apenas um dashboard climático. Ele organiza o problema em quatro camadas:

```txt
1. ENSO e El Niño
2. Clima regional em Goiás
3. Risco agrícola em soja e milho safrinha
4. Risco comercial e recomendação de consultoria
```

Isso deixa a solução mais próxima de uma aplicação real para produtores e consultorias agrícolas.
