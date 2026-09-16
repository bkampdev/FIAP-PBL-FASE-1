"""Carregamento e validação dos dados de telemetria.

Issue #14 — validação estrutural dos dados antes das regras de decisão.

A validação deste módulo verifica formato, presença, tipo e domínio possível.
Ela NÃO decide se a nave pode decolar. Por exemplo:
- integridade_estrutural = 0 é um dado válido, mas representa falha operacional;
- um módulo com estado "FALHA" é um dado válido, mas deve ser tratado pelo
  algoritmo de decisão;
- temperatura fora da faixa segura ainda pode ser um número válido.
"""

import json
import math


MODULOS_OBRIGATORIOS = {
    "suporte_vida",
    "energia",
    "comunicacao",
    "propulsao",
    "navegacao",
}

ESTADOS_MODULOS = {"OK", "FALHA"}

CAMPOS_OBRIGATORIOS = {
    "temperatura_interna_c",
    "temperatura_externa_c",
    "integridade_estrutural",
    "energia_pct",
    "pressao_tanque_kpa",
    "modulos",
}

# Entradas do módulo de energia (#6). Elas são validadas quando aparecem
# no cenário, mas não são exigidas do gerador de telemetria até a integração
# entre os módulos ser concluída.
CAMPOS_ENERGIA = {
    "capacidade_kwh",
    "carga_pct",
    "consumo_decolagem_kwh",
    "perdas_pct",
}
CAMPO_ENERGIA_OPCIONAL = "potencia_media_kw"


def _eh_numero_finito(valor):
    """True somente para int/float finito; bool não é aceito como número."""
    return (
        isinstance(valor, (int, float))
        and not isinstance(valor, bool)
        and math.isfinite(valor)
    )


def carregar_json(caminho):
    """Lê um arquivo JSON de forma segura.

    Retorna:
        (dados, erros)

    Em caso de sucesso, ``erros`` é uma lista vazia.
    Em caso de falha, ``dados`` é None e ``erros`` contém mensagem clara.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        return None, [f"arquivo não encontrado: {caminho}"]
    except json.JSONDecodeError as erro:
        return None, [
            f"JSON malformado em {caminho}: linha {erro.lineno}, coluna {erro.colno}"
        ]
    except OSError as erro:
        return None, [f"não foi possível ler {caminho}: {erro}"]

    if not isinstance(dados, dict):
        return None, [f"o conteúdo de {caminho} deve ser um objeto JSON"]

    return dados, []


def validar_telemetria(dados):
    """Valida estrutura, tipos e domínios da telemetria.

    Retorna uma lista de mensagens. Lista vazia significa que os dados são
    estruturalmente válidos. A função não altera o dicionário recebido.
    """
    erros = []

    if not isinstance(dados, dict):
        return ["telemetria deve ser um objeto/dicionário"]

    # Presença dos campos principais
    for campo in sorted(CAMPOS_OBRIGATORIOS):
        if campo not in dados:
            erros.append(f"campo obrigatório ausente: {campo}")

    # Só valida o conteúdo de um campo se ele existir, evitando KeyError.
    _validar_numero(
        dados,
        "temperatura_interna_c",
        erros,
        minimo=-100,
        maximo=150,
    )
    _validar_numero(
        dados,
        "temperatura_externa_c",
        erros,
        minimo=-200,
        maximo=150,
    )
    _validar_numero(
        dados,
        "energia_pct",
        erros,
        minimo=0,
        maximo=100,
        mensagem_intervalo="energia_pct deve estar entre 0 e 100",
    )
    _validar_numero(
        dados,
        "pressao_tanque_kpa",
        erros,
        minimo_exclusivo=0,
        maximo=1000,
    )

    if "integridade_estrutural" in dados:
        valor = dados["integridade_estrutural"]
        if isinstance(valor, bool) or not isinstance(valor, int):
            erros.append("integridade_estrutural deve ser inteiro 0 ou 1")
        elif valor not in (0, 1):
            erros.append("integridade_estrutural deve ser 0 ou 1")

    if "modulos" in dados:
        _validar_modulos(dados["modulos"], erros)

    _validar_entradas_energia(dados, erros)

    return erros


def _validar_numero(
    dados,
    campo,
    erros,
    minimo=None,
    maximo=None,
    minimo_exclusivo=None,
    mensagem_intervalo=None,
):
    if campo not in dados:
        return

    valor = dados[campo]
    if not _eh_numero_finito(valor):
        erros.append(f"{campo} deve ser número finito")
        return

    fora = False
    if minimo is not None and valor < minimo:
        fora = True
    if maximo is not None and valor > maximo:
        fora = True
    if minimo_exclusivo is not None and valor <= minimo_exclusivo:
        fora = True

    if fora:
        if mensagem_intervalo:
            erros.append(mensagem_intervalo)
        elif minimo_exclusivo is not None and maximo is not None:
            erros.append(
                f"{campo} deve ser maior que {minimo_exclusivo} e menor ou igual a {maximo}"
            )
        elif minimo is not None and maximo is not None:
            erros.append(f"{campo} deve estar entre {minimo} e {maximo}")
        else:
            erros.append(f"{campo} está fora do domínio válido")


def _validar_modulos(modulos, erros):
    if not isinstance(modulos, dict):
        erros.append("modulos deve ser um objeto/dicionário")
        return

    faltantes = sorted(MODULOS_OBRIGATORIOS - set(modulos))
    for modulo in faltantes:
        erros.append(f"módulo obrigatório ausente: {modulo}")

    for modulo in sorted(MODULOS_OBRIGATORIOS & set(modulos)):
        estado = modulos[modulo]
        if not isinstance(estado, str):
            erros.append(f"modulos.{modulo} deve ser texto 'OK' ou 'FALHA'")
        elif estado not in ESTADOS_MODULOS:
            erros.append(f"modulos.{modulo} deve ser 'OK' ou 'FALHA'")


def _validar_entradas_energia(dados, erros):
    """Valida campos energéticos quando o cenário os fornece."""
    presentes = CAMPOS_ENERGIA & set(dados)

    # Se nenhum campo energético foi fornecido, não cria um segundo contrato
    # obrigatório para o gerador de telemetria.
    if not presentes and CAMPO_ENERGIA_OPCIONAL not in dados:
        return

    # Se o cenário começou a informar o bloco energético, os campos-base
    # precisam estar completos para o cálculo do módulo #6.
    for campo in sorted(CAMPOS_ENERGIA):
        if campo not in dados:
            erros.append(f"campo energético obrigatório ausente: {campo}")

    _validar_numero(
        dados,
        "capacidade_kwh",
        erros,
        minimo_exclusivo=0,
    )
    _validar_numero(
        dados,
        "carga_pct",
        erros,
        minimo=0,
        maximo=100,
    )
    _validar_numero(
        dados,
        "consumo_decolagem_kwh",
        erros,
        minimo=0,
    )
    _validar_numero(
        dados,
        "perdas_pct",
        erros,
        minimo=0,
        maximo=100,
    )

    if CAMPO_ENERGIA_OPCIONAL in dados:
        _validar_numero(
            dados,
            CAMPO_ENERGIA_OPCIONAL,
            erros,
            minimo_exclusivo=0,
        )

    # ``energia_pct`` é a telemetria da carga atual e ``carga_pct`` é o
    # mesmo valor consumido pelo cálculo energético. Dois números diferentes
    # fariam o verificador e a análise energética decidirem sobre cenários
    # distintos.
    if (
        "energia_pct" in dados
        and "carga_pct" in dados
        and _eh_numero_finito(dados["energia_pct"])
        and _eh_numero_finito(dados["carga_pct"])
        and dados["energia_pct"] != dados["carga_pct"]
    ):
        erros.append("carga_pct deve ser igual a energia_pct")
