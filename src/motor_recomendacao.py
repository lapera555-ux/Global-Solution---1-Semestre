def classificar_irea(valor: float) -> str:
    if valor < 31:
        return "Baixo"
    if valor < 56:
        return "Moderado"
    if valor < 76:
        return "Alto"
    return "Crítico"


def gerar_alerta(row) -> str:
    """Gera texto de consultoria para uma linha da base."""
    return (
        f"{row['municipio']} | {row['cultura']} | {row['fase_cultura']}. "
        f"IREA {row['irea_indice_risco_enso_agricola']}, risco produtivo {row['risco_produtivo']} e risco comercial {row['risco_comercial']}. "
        f"Chuva 30d: {row['chuva_30d_mm']} mm, anomalia de temperatura: {row['anomalia_temp_c']} °C, "
        f"umidade do solo: {row['umidade_solo_pct']}%. "
        f"Produtividade esperada: {row['produtividade_esperada_sc_ha']} sc/ha; revisada: {row['produtividade_revisada_sc_ha']} sc/ha. "
        f"Recomendação: {row['recomendacao']}"
    )


def matriz_decisao(risco_produtivo: str, risco_comercial: str) -> str:
    if risco_produtivo in ["Alto", "Crítico"] and risco_comercial in ["Alto", "Crítico"]:
        return "Prioridade máxima: revisar produção e bloquear novas vendas até validação de campo."
    if risco_produtivo in ["Alto", "Crítico"]:
        return "Priorizar vistoria técnica e revisar produtividade antes de avançar comercialmente."
    if risco_comercial in ["Alto", "Crítico"]:
        return "Cautela comercial: exposição elevada mesmo com risco produtivo controlado."
    if risco_produtivo == "Moderado":
        return "Acompanhar semanalmente e vender apenas com margem de segurança."
    return "Manter plano comercial e monitoramento climático."
