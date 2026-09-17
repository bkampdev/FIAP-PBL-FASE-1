"""Apresentação textual dos resultados de pré-decolagem.

Este módulo recebe somente o resultado estruturado por ``executar_cenario``.
Ele não lê telemetria, não altera a decisão e não recalcula energia.
"""

from collections.abc import Mapping
import math
from pathlib import Path


def formatar_resultado(resultado):
    """Retorna uma apresentação legível de um resultado de missão.

    A função aceita o contrato retornado por ``src.missao.executar_cenario``:
    ``origem``, ``decisao``, ``motivos`` e ``energia``. Campos energéticos
    ausentes permanecem indisponíveis; nenhum valor é inferido ou recalculado.
    """
    if not isinstance(resultado, Mapping):
        return "ERRO: resultado inválido.\nEnergia: indisponível."

    linhas = [f"Cenário: {_identificar_cenario(resultado.get('origem'))}"]
    motivos = _motivos(resultado.get("motivos"))
    decisao = resultado.get("decisao")

    if decisao is None:
        linhas.append("ERRO: resultado inválido — campo 'decisao' ausente.")
        _adicionar_motivos(linhas, motivos)
        linhas.append("Energia: indisponível.")
        return "\n".join(linhas)

    linhas.append(f"Decisão: {decisao}")
    if decisao == "PRONTO PARA DECOLAR" and not motivos:
        linhas.append("Nenhuma falha operacional identificada.")
    else:
        _adicionar_motivos(linhas, motivos)

    _adicionar_energia(linhas, resultado.get("energia"))
    return "\n".join(linhas)


def _motivos(motivos):
    if isinstance(motivos, (list, tuple)):
        return [str(motivo) for motivo in motivos]
    return []


def _identificar_cenario(origem):
    if not isinstance(origem, str) or not origem:
        return "cenário não identificado"
    if origem.endswith(".json"):
        return Path(origem).name
    return origem


def _adicionar_motivos(linhas, motivos):
    if not motivos:
        return
    linhas.append("Motivos:")
    linhas.extend(f"- {motivo}" for motivo in motivos)


def _adicionar_energia(linhas, energia):
    if not isinstance(energia, Mapping):
        linhas.append("Energia: indisponível.")
        return

    _adicionar_kwh(linhas, "Energia inicial", energia.get("energia_inicial_kwh"))
    _adicionar_kwh(linhas, "Perdas", energia.get("perdas_kwh"))
    _adicionar_kwh(linhas, "Energia útil", energia.get("energia_util_kwh"))
    _adicionar_kwh(linhas, "Saldo após decolagem", energia.get("saldo_kwh"))

    autonomia = energia.get("autonomia_h")
    if _numero(autonomia):
        linhas.append(f"Autonomia estimada: {autonomia:.2f} h")
    else:
        linhas.append("Autonomia temporal não calculada.")


def _adicionar_kwh(linhas, rotulo, valor):
    if _numero(valor):
        linhas.append(f"{rotulo}: {valor:.2f} kWh")


def _numero(valor):
    return (
        isinstance(valor, (int, float))
        and not isinstance(valor, bool)
        and math.isfinite(valor)
    )


def exibir_cenario_gerado(cenario, dados, resultado):
    """Imprime os dados gerados e o resultado real em texto compacto."""
    print(f"\n=== {cenario.replace('_', ' ').capitalize()} ===")
    print(
        f"Temperatura: interna {dados['temperatura_interna_c']} °C | "
        f"externa {dados['temperatura_externa_c']} °C"
    )
    print(
        f"Integridade: {dados['integridade_estrutural']} | "
        f"Energia: {dados['energia_pct']}% | "
        f"Pressão: {dados['pressao_tanque_kpa']} kPa"
    )
    print("Módulos: " + ", ".join(
        f"{nome.replace('_', ' ')}={estado}"
        for nome, estado in dados['modulos'].items()
    ))
    # Reutiliza a apresentação existente, omitindo apenas o título redundante.
    print("\n".join(formatar_resultado(resultado).splitlines()[1:]))
