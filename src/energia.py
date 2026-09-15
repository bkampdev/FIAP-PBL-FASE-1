def calcular_energia(capacidade_kwh, carga_pct, consumo_decolagem_kwh, perdas_pct, potencia_media_kw=None):
    # 1. Validação de domínio dos parâmetros de entrada
    if (capacidade_kwh <= 0 or 
        not (0 <= carga_pct <= 100) or 
        not (0 <= perdas_pct <= 100) or 
        consumo_decolagem_kwh < 0):
        return {
            "energia_inicial_kwh": 0.0,
            "perdas_kwh": 0.0,
            "energia_util_kwh": 0.0,
            "saldo_kwh": 0.0,
            "viavel": False,
            "autonomia_h": None
        }

    # 2. Cálculos energéticos
    energia_inicial_kwh = capacidade_kwh * (carga_pct / 100.0)
    perdas_kwh = energia_inicial_kwh * (perdas_pct / 100.0)
    energia_util_kwh = energia_inicial_kwh - perdas_kwh
    energia_saldo_kwh = energia_util_kwh - consumo_decolagem_kwh

    # 3. Determina a viabilidade e autonomia temporal
    if energia_saldo_kwh < 0:
        viavel = False
        autonomia_h = None
    elif potencia_media_kw is None or potencia_media_kw <= 0:
        viavel = True  # O saldo de energia é positivo, mas a autonomia temporal não é calculável
        autonomia_h = None
    else:
        viavel = True
        autonomia_h = energia_saldo_kwh / potencia_media_kw

    return {
        "energia_inicial_kwh": energia_inicial_kwh,
        "perdas_kwh": perdas_kwh,
        "energia_util_kwh": energia_util_kwh,
        "saldo_kwh": energia_saldo_kwh,
        "viavel": viavel,
        "autonomia_h": autonomia_h
    }