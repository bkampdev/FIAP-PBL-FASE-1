"""
Módulo de apresentação textual dos resultados da verificação de pré-decolagem.

Autoria: Gabriel (@ItsTheContext)

Este módulo NÃO lê sensores nem decide se a nave pode decolar.
Ele recebe um dicionário de resultado já calculado (decisão de Lorenzo,
números de energia de Eduardo) e retorna um texto legível para exibição
no notebook, README e PDF.
"""


def formatar_resultado(resultado: dict) -> str:
    """
    Formata o resultado da verificação de pré-decolagem em texto legível.

    Parâmetros
    ----------
    resultado : dict
        Dicionário esperado com as chaves:
        - "cenario" (str): identificação do cenário testado.
        - "decisao" (str): "PRONTO PARA DECOLAR" ou "DECOLAGEM ABORTADA".
        - "motivos" (list[str]): lista de motivos de aborto (pode ser vazia).
        - "energia" (dict): capacidade_kwh, carga_percentual, autonomia_horas
          (autonomia_horas pode ser None se não calculada).

    Retorna
    -------
    str
        Texto formatado, pronto para impressão. Não modifica o dicionário
        recebido.
    """
    # Validação: decisão é obrigatória. Sem ela, não aprovamos por padrão.
    if "decisao" not in resultado:
        return "ERRO: resultado inválido — campo 'decisao' ausente."

    cenario = resultado.get("cenario", "cenário não identificado")
    decisao = resultado["decisao"]
    motivos = resultado.get("motivos", [])
    energia = resultado.get("energia", {})

    linhas = []
    linhas.append(f"Cenário: {cenario}")
    linhas.append(f"Decisão: {decisao}")

    # Motivos de aborto (ou confirmação de que não há falhas)
    if decisao == "PRONTO PARA DECOLAR" and not motivos:
        linhas.append("Nenhuma falha operacional identificada.")
    else:
        for motivo in motivos:
            linhas.append(f"- Motivo: {motivo}")

    # Bloco de energia
    capacidade = energia.get("capacidade_kwh")
    carga = energia.get("carga_percentual")
    autonomia = energia.get("autonomia_horas")

    if capacidade is not None:
        linhas.append(f"Capacidade: {capacidade:.2f} kWh")
    if carga is not None:
        linhas.append(f"Carga atual: {carga:.2f}%")

    if autonomia is None:
        linhas.append("Autonomia temporal não calculada")
    else:
        linhas.append(f"Autonomia estimada: {autonomia:.2f} h")

    return "\n".join(linhas)


if __name__ == "__main__":
    # Exemplo manual de uso — útil para conferir a formatação visualmente.
    resultado_exemplo = {
        "cenario": "nominal_01",
        "decisao": "PRONTO PARA DECOLAR",
        "motivos": [],
        "energia": {
            "autonomia_horas": 4.25,
            "capacidade_kwh": 120.0,
            "carga_percentual": 87.5,
        },
    }
    print(formatar_resultado(resultado_exemplo))
