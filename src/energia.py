def calcular_energia(capacidade_kwh, carga_pct, consumo_decolagem_kwh, perdas_pct, potencia_media_kw=None):
    energia_inicial_kwh = capacidade_kwh*(carga_pct / 100)
    perdas_kwh = (energia_inicial_kwh/100)*perdas_pct
    energia_util_kwh = energia_inicial_kwh - perdas_kwh
    energia_saldo_kwh = energia_util_kwh-consumo_decolagem_kwh

    if energia_saldo_kwh >= 0 and potencia_media_kw:
        autonomia_h = energia_saldo_kwh/potencia_media_kw
    else:
        autonomia_h = 0

    return autonomia_h