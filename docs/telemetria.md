# Dicionário de telemetria

Este documento define o contrato de entrada adotado pelo grupo para a simulação de pré-decolagem.

As faixas operacionais são **hipóteses didáticas do projeto**. Elas não representam parâmetros certificados de uma nave real. Nesta versão, os limites foram alinhados com os valores já usados pelo módulo `src/verificacao.py` e seus testes na `main`.

## Campos

| Campo | Significado | Tipo | Unidade | Exemplo | Domínio válido | Faixa operacional segura | Justificativa didática |
|---|---|---|---|---:|---|---|---|
| `temperatura_interna_c` | Temperatura interna | número | °C | 22 | -100 a 150 | **15 a 30, inclusive** | permite testar conforto/segurança com fronteiras claras |
| `temperatura_externa_c` | Temperatura externa | número | °C | -50 | -200 a 150 | **-150 a 120, inclusive** | faixa ampla e didática para a simulação |
| `integridade_estrutural` | Indica integridade da estrutura | inteiro | 0 ou 1 | 1 | somente 0 ou 1 | **1** | `0` é falha operacional válida e deve chegar ao verificador |
| `energia_pct` | Percentual de energia/carga disponível | número | % | 80 | 0 a 100 | **50 a 100, inclusive** | separa domínio percentual de uma condição operacional segura |
| `pressao_tanque_kpa` | Pressão do tanque | número | kPa | 100 | maior que 0 e até 1000 | **90 a 110, inclusive** | faixa hipotética simples para testes de limite |
| `modulos` | Estados dos módulos críticos | objeto | estado textual | ver abaixo | todos os módulos obrigatórios | todos em `OK` | qualquer `FALHA` deve impedir a decolagem |

## Módulos críticos e estados aceitos

A seleção dos módulos é uma hipótese didática do grupo e foi alinhada ao módulo de decisão existente:

- `suporte_vida`
- `energia`
- `comunicacao`
- `propulsao`
- `navegacao`

Estados aceitos:
- `OK`
- `FALHA`

## Entradas do cálculo energético

| Campo | Significado | Tipo | Unidade | Exemplo | Domínio válido |
|---|---|---|---|---:|---|
| `capacidade_kwh` | Capacidade total | número | kWh | 100 | maior que 0 |
| `carga_pct` | Carga atual | número | % | 80 | 0 a 100 |
| `consumo_decolagem_kwh` | Consumo previsto da decolagem | número | kWh | 20 | maior ou igual a 0 |
| `perdas_pct` | Perdas aplicadas à energia inicial | número | % | 5 | 0 a 100 |
| `potencia_media_kw` | Potência média para estimar autonomia | número | kW | 10 | maior que 0 quando usada |

A conta adotada pelo módulo de energia é:

`energia_inicial = capacidade_kwh * carga_pct / 100`

`perdas = energia_inicial * perdas_pct / 100`

`energia_util = energia_inicial - perdas`

`saldo = energia_util - consumo_decolagem_kwh`

`autonomia_h = saldo / potencia_media_kw`, quando há saldo não negativo e potência utilizável.

Exemplo nominal: 100 kWh × 80% = 80 kWh; perdas de 5% sobre 80 kWh = 4 kWh; energia útil = 76 kWh; após consumo de 20 kWh sobram 56 kWh; a 10 kW, autonomia = **5,6 h**.

## Domínio válido x segurança operacional

Validação de dados e decisão operacional são etapas diferentes.

- `energia_pct = 45` é **válido** no domínio 0–100, porém está abaixo da faixa segura de 50%.
- `energia_pct = 150` é **inválido**.
- `integridade_estrutural = 0` é um dado **válido**, porém exige aborto.
- `modulos.propulsao = "FALHA"` é um dado **válido**, porém exige aborto.
- `temperatura_interna_c = 31` é um número válido no domínio geral, porém está acima do máximo operacional de 30 °C.

## Cenários versionados

Cada cenário de falha parte do nominal e altera uma única condição para isolar a causa.

| Arquivo | Única alteração em relação ao nominal | Resultado operacional esperado |
|---|---|---|
| `dados/nominal.json` | nenhuma | `PRONTO PARA DECOLAR` |
| `dados/falha_temperatura.json` | `temperatura_interna_c`: 22 → 31 | `DECOLAGEM ABORTADA`, motivo de temperatura interna |
| `dados/falha_modulo.json` | `modulos.propulsao`: `OK` → `FALHA` | `DECOLAGEM ABORTADA`, motivo de módulo crítico |
| `dados/falha_energia.json` | `consumo_decolagem_kwh`: 20 → 80 | autonomia não positiva e `DECOLAGEM ABORTADA` |

Os JSONs são dados sintéticos produzidos para fins didáticos.
