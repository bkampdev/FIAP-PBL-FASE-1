"""Cálculos da energia disponível para a decisão de pré-decolagem."""

import math


def _validar_numero(nome, valor, minimo=None, maximo=None, estritamente_positivo=False):
    """Rejeita tipos e números que não podem participar de um cálculo físico."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{nome} deve ser um número finito")
    if not math.isfinite(valor):
        raise ValueError(f"{nome} deve ser um número finito")
    if estritamente_positivo and valor <= 0:
        raise ValueError(f"{nome} deve ser maior que zero")
    if minimo is not None and valor < minimo:
        raise ValueError(f"{nome} deve ser maior ou igual a {minimo}")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{nome} deve ser menor ou igual a {maximo}")


def calcular_energia(
    capacidade_kwh,
    carga_pct,
    consumo_decolagem_kwh,
    perdas_pct,
    potencia_media_kw=None,
):
    """Calcula energia, saldo e autonomia após a decolagem.

    Retorna um dicionário estruturado para que o verificador possa decidir pela
    chave ``viavel`` e a apresentação possa exibir os valores intermediários.
    Uma missão só é viável quando sobra energia positiva após a decolagem.
    """
    _validar_numero("capacidade_kwh", capacidade_kwh, estritamente_positivo=True)
    _validar_numero("carga_pct", carga_pct, minimo=0, maximo=100)
    _validar_numero("consumo_decolagem_kwh", consumo_decolagem_kwh, minimo=0)
    _validar_numero("perdas_pct", perdas_pct, minimo=0, maximo=100)
    if potencia_media_kw is not None:
        _validar_numero(
            "potencia_media_kw", potencia_media_kw, estritamente_positivo=True
        )

    energia_inicial_kwh = capacidade_kwh * (carga_pct / 100.0)
    perdas_kwh = energia_inicial_kwh * (perdas_pct / 100.0)
    energia_util_kwh = energia_inicial_kwh - perdas_kwh
    energia_saldo_kwh = energia_util_kwh - consumo_decolagem_kwh

    viavel = energia_saldo_kwh > 0
    autonomia_h = (
        energia_saldo_kwh / potencia_media_kw
        if viavel and potencia_media_kw is not None
        else None
    )

    return {
        "energia_inicial_kwh": energia_inicial_kwh,
        "perdas_kwh": perdas_kwh,
        "energia_util_kwh": energia_util_kwh,
        "saldo_kwh": energia_saldo_kwh,
        "viavel": viavel,
        "autonomia_h": autonomia_h
    }
