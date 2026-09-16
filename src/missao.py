"""Orquestra os módulos da simulação de pré-decolagem.

Este módulo é a fronteira de integração da issue #4: recebe uma telemetria
fixa ou o caminho de um JSON, valida a entrada, calcula a energia e aplica as
regras determinísticas de decisão. Ele não reimplementa os módulos de
validação, energia ou verificação.
"""

from collections.abc import Mapping
from copy import deepcopy
import math
from os import PathLike

from src.energia import calcular_energia
from src.validacao import carregar_json, validar_telemetria
from src.verificacao import verificar_pre_decolagem


# Faixas didáticas acordadas em docs/telemetria.md. Não representam parâmetros
# certificados de uma nave real.
LIMITES_PADRAO = {
    "temperatura_interna_c": (15, 30),
    "temperatura_externa_c": (-150, 120),
    "energia_pct": (50, 100),
    "pressao_tanque_kpa": (90, 110),
}

CAMPOS_ENERGIA_CENARIO = (
    "capacidade_kwh",
    "carga_pct",
    "consumo_decolagem_kwh",
    "perdas_pct",
)


def executar_cenario(caminho_ou_dados, limites):
    """Executa um cenário completo sem alterar os dados recebidos.

    Args:
        caminho_ou_dados: caminho para um JSON de telemetria ou dicionário
            equivalente já carregado.
        limites: dicionário ``campo -> (mínimo, máximo)`` usado pelo módulo de
            verificação.

    Returns:
        Um dicionário com ``origem``, ``dados``, ``erros_entrada``, ``energia``,
        ``decisao`` e ``motivos``. Uma falha de leitura, validação ou cálculo
        sempre retorna ``DECOLAGEM ABORTADA``; nenhum cenário nominal oculto é
        usado como fallback.
    """
    dados, origem, erros = _obter_dados(caminho_ou_dados)
    resultado = {
        "origem": origem,
        "dados": dados,
        "erros_entrada": erros,
        "energia": None,
        "decisao": "DECOLAGEM ABORTADA",
        "motivos": [],
    }

    if erros:
        resultado["motivos"] = _motivos_de_entrada(erros)
        return resultado

    erros_validacao = validar_telemetria(dados)
    if erros_validacao:
        resultado["erros_entrada"] = erros_validacao
        resultado["motivos"] = _motivos_de_entrada(erros_validacao)
        return resultado

    erros_limites = _validar_limites(limites)
    if erros_limites:
        resultado["erros_entrada"] = erros_limites
        resultado["motivos"] = _motivos_de_entrada(erros_limites)
        return resultado

    campos_energia_ausentes = [
        campo for campo in CAMPOS_ENERGIA_CENARIO if campo not in dados
    ]
    if campos_energia_ausentes:
        resultado["erros_entrada"] = [
            f"campo energético obrigatório ausente: {campo}"
            for campo in campos_energia_ausentes
        ]
        resultado["motivos"] = _motivos_de_entrada(resultado["erros_entrada"])
        return resultado

    try:
        energia = calcular_energia(
            dados["capacidade_kwh"],
            dados["carga_pct"],
            dados["consumo_decolagem_kwh"],
            dados["perdas_pct"],
            dados.get("potencia_media_kw"),
        )
    except ValueError as erro:
        resultado["erros_entrada"] = [str(erro)]
        resultado["motivos"] = _motivos_de_entrada(resultado["erros_entrada"])
        return resultado

    decisao = verificar_pre_decolagem(dados, energia, limites)
    resultado["energia"] = energia
    resultado["decisao"] = decisao["decisao"]
    resultado["motivos"] = decisao["motivos"]
    return resultado


def _obter_dados(caminho_ou_dados):
    if isinstance(caminho_ou_dados, Mapping):
        return deepcopy(dict(caminho_ou_dados)), "dados em memória", []

    if isinstance(caminho_ou_dados, (str, PathLike)):
        caminho = str(caminho_ou_dados)
        dados, erros = carregar_json(caminho)
        return dados, caminho, erros

    return (
        None,
        "fonte inválida",
        ["cenário deve ser um caminho de JSON ou um dicionário de telemetria"],
    )


def _validar_limites(limites):
    if not isinstance(limites, Mapping) or not limites:
        return ["limites deve ser um dicionário não vazio"]

    erros = []
    for campo, faixa in limites.items():
        if not isinstance(faixa, (tuple, list)) or len(faixa) != 2:
            erros.append(f"limite inválido para {campo}: use (mínimo, máximo)")
            continue

        minimo, maximo = faixa
        if (
            isinstance(minimo, bool)
            or isinstance(maximo, bool)
            or not isinstance(minimo, (int, float))
            or not isinstance(maximo, (int, float))
            or not math.isfinite(minimo)
            or not math.isfinite(maximo)
            or minimo > maximo
        ):
            erros.append(f"limite inválido para {campo}")
    return erros


def _motivos_de_entrada(erros):
    return [f"Entrada inválida: {erro}" for erro in erros]
