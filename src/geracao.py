"""
geracao.py - Issue #13

Dois modelos de estimacao de densidade:
    numeros -> Gaussian Mixture Model (continuo)
    modulos -> frequencia observada no historico (discreto)

Integridade e falhas forcadas sao definidas pelo cenario.
A base de treinamento fica em dados/base_treinamento.json

Fluxo:
    escolher cenario -> gerar -> validar -> verificar seguranca -> exibir
"""

import json
import os

import numpy as np
from sklearn.mixture import GaussianMixture


CENARIOS = ["nominal", "energia_insuficiente", "falha_modulo", "falha_sensor"]

MODULOS = ["suporte_vida", "energia", "comunicacao", "propulsao", "navegacao"]

# caminho da base, relativo a este arquivo (funciona de qualquer pasta)
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BASE = os.path.join(PASTA_ATUAL, "dados", "base_treinamento.json")


# ---------------------------------------------------------------
# LEITURA DA BASE
# ---------------------------------------------------------------

def pega_dados_treinamento(chave, caminho=CAMINHO_BASE):
    """Le a base de treinamento do arquivo JSON.

    chave: "numeros" ou "modulos"
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError("base de treinamento nao encontrada: " + caminho)

    arquivo = open(caminho, encoding="utf-8")
    conteudo = json.load(arquivo)
    arquivo.close()

    if chave not in conteudo:
        raise ValueError("chave nao encontrada no arquivo: " + chave)

    dados = conteudo[chave]

    if len(dados) == 0:
        raise ValueError("base vazia para a chave: " + chave)

    return dados


def treinamento_modelo_numeros(n_components=2, random_state=42):
    """Estima p(x) dos 4 campos numericos com mistura de gaussianas."""
    base_numeros = pega_dados_treinamento("numeros")

    modelo = GaussianMixture(n_components=n_components, random_state=random_state)
    modelo.fit(np.array(base_numeros))
    return modelo


def treinamento_modelo_modulos():
    """Estima p(modulo = OK) pela frequencia observada no historico.

    Os valores sao 0 e 1, entao a media da coluna e a propria proporcao de OK.
    """
    base_modulos = pega_dados_treinamento("modulos")

    return np.array(base_modulos).mean(axis=0)




class Telemetria:
    def __init__(self, temperatura_interna_c, temperatura_externa_c,
                 energia_pct, pressao_tanque_kpa,
                 integridade_estrutural, modulos):
        self.temperatura_interna_c = temperatura_interna_c
        self.temperatura_externa_c = temperatura_externa_c
        self.energia_pct = energia_pct
        self.pressao_tanque_kpa = pressao_tanque_kpa
        self.integridade_estrutural = integridade_estrutural
        self.modulos = modulos

    def __str__(self):
        texto = ""
        texto = texto + "  temperatura interna: " + str(self.temperatura_interna_c) + " C\n"
        texto = texto + "  temperatura externa: " + str(self.temperatura_externa_c) + " C\n"
        texto = texto + "  energia: " + str(self.energia_pct) + " %\n"
        texto = texto + "  pressao do tanque: " + str(self.pressao_tanque_kpa) + " kPa\n"
        texto = texto + "  integridade: " + self.integridade_estrutural + "\n"
        texto = texto + "  modulos: " + str(self.modulos)
        return texto


def gerar_telemetria(cenario, seed=None):
    if cenario not in CENARIOS:
        raise ValueError("cenario invalido: " + str(cenario))

    MODELO_DADOS_NUMEROS = treinamento_modelo_numeros()
    MODELO_DADOS_MODULOS = treinamento_modelo_modulos()

    # --- numeros: sorteia 1 ponto de p(x) ---
    MODELO_DADOS_NUMEROS.random_state = seed
    dados_novos_gerados_numeros = MODELO_DADOS_NUMEROS.sample(1)[0][0]

    dicionario_dados = {
        "temperatura_interna_c": round(float(dados_novos_gerados_numeros[0]), 2),
        "temperatura_externa_c": round(float(dados_novos_gerados_numeros[1]), 2),
        "energia_pct": round(float(dados_novos_gerados_numeros[2]), 2),
        "pressao_tanque_kpa": round(float(dados_novos_gerados_numeros[3]), 2),
        "integridade_estrutural": "NOMINAL",
        "modulos": {},
    }

    # --- modulos: sorteia cada um com a sua probabilidade ---
    objeto_nrg = np.random.default_rng(seed)

    for i in range(len(MODULOS)):
        if objeto_nrg.random() < MODELO_DADOS_MODULOS[i]:
            dicionario_dados["modulos"][MODULOS[i]] = "OK"
        else:
            dicionario_dados["modulos"][MODULOS[i]] = "FALHA"

    # --- cenario altera uma condicao (sobrescreve o sorteio) ---
    if cenario == "nominal":
        pass

    elif cenario == "energia_insuficiente":
        dicionario_dados["energia_pct"] = 45.0
        dicionario_dados["integridade_estrutural"] = "DEGRADADO"

    elif cenario == "falha_modulo":
        dicionario_dados["modulos"]["propulsao"] = "FALHA"
        dicionario_dados["integridade_estrutural"] = "CRITICO"

    elif cenario == "falha_sensor":
        dicionario_dados["temperatura_interna_c"] = 55.0
        dicionario_dados["integridade_estrutural"] = "DEGRADADO"

    # se algum modulo caiu em FALHA no sorteio, a integridade acompanha
    for modulo in dicionario_dados["modulos"]:
        if dicionario_dados["modulos"][modulo] == "FALHA":
            if dicionario_dados["integridade_estrutural"] == "NOMINAL":
                dicionario_dados["integridade_estrutural"] = "CRITICO"

    return dicionario_dados