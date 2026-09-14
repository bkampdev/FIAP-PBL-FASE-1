"""
verificacao.py - Issue #3

"""

MODULOS_CRITICOS = ["suporte_vida", "energia", "comunicacao", "propulsao", "navegacao"]


def verificar_pre_decolagem(dados, energia, limites):
    """Aplica as regras de seguranca e devolve a decisao.

    dados   -> telemetria (#13)
    energia -> autonomia em horas retornada pelo calculo energetico (#6)
    limites -> faixas operacionais (#2)

    Retorna {"decisao": str, "motivos": list}
    """
    motivos = []

    for campo in limites:
        if campo not in dados:
            motivos.append("Campo ausente na telemetria: " + campo)
            continue

        valor = dados[campo]
        minimo = limites[campo][0]
        maximo = limites[campo][1]

        if valor < minimo:
            motivos.append(
                campo + " " + str(valor) + " abaixo do minimo de " + str(minimo)
            )

        if valor > maximo:
            motivos.append(
                campo + " " + str(valor) + " acima do maximo de " + str(maximo)
            )

    if "integridade_estrutural" not in dados:
        motivos.append("Campo ausente na telemetria: integridade_estrutural")
    else:
        if dados["integridade_estrutural"] not in ("NOMINAL", 1):
            motivos.append(
                "Integridade estrutural " + str(dados["integridade_estrutural"])
                + ", esperado NOMINAL ou 1"
            )

    if "modulos" not in dados:
        motivos.append("Campo ausente na telemetria: modulos")
    else:
        for modulo in MODULOS_CRITICOS:
            if modulo not in dados["modulos"]:
                motivos.append("Modulo ausente na telemetria: " + modulo)
            elif dados["modulos"][modulo] == "FALHA":
                motivos.append("Modulo critico em falha: " + modulo)

    if energia is None:
        motivos.append("Resultado energetico ausente")
    elif energia <= 0:
        motivos.append("Energia insuficiente: autonomia de " + str(energia) + " h")

    if len(motivos) == 0:
        return {"decisao": "PRONTO PARA DECOLAR", "motivos": []}

    return {"decisao": "DECOLAGEM ABORTADA", "motivos": motivos}
