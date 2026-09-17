# ATIVIDADE INTEGRADORA — RELATÓRIO OPERACIONAL DE PRÉ-DECOLAGEM

**FIAP — Fase 1: Decolagem da Missão**

**16 de setembro de 2026**

## Equipe

| Integrante | RM | Contribuição principal |
| --- | --- | --- |
| Davi Coninck Cassaro | RM572772 | telemetria, validação e testes |
| Guilherme Cardoso Bremenkamp | RM574229 | integração dos cenários e notebook |
| Lorenzo Mendes Rocha | RM575361 | verificação, geração sintética e reflexão |
| Gabriel Gonzales | RM574746 | análise por IA, apresentação e revisão |
| Eduardo Backes Klauck | RM575889 | energia, documentação e relatório |

Repositório público:
https://github.com/bkampdev/FIAP-PBL-FASE-1

Notebook:
https://github.com/bkampdev/FIAP-PBL-FASE-1/blob/main/notebooks/pre_decolagem.ipynb

## Resumo

Este trabalho implementa uma simulação educacional de pré-decolagem. O sistema
lê dados sintéticos, valida o contrato de entrada, calcula o balanço energético,
verifica as faixas seguras e apresenta uma decisão explicável. O fluxo autoriza
a missão somente quando todos os critérios são satisfeitos e o saldo energético
é positivo. A análise por IA apoia a interpretação, mas não substitui as regras
determinísticas nem a revisão humana.

Os limites são hipóteses didáticas do grupo e não parâmetros certificados de
uma nave real.

## 1. Objetivo e arquitetura

O objetivo é responder “PRONTO PARA DECOLAR” ou “DECOLAGEM ABORTADA” a partir
da telemetria e do cálculo energético, acumulando todos os motivos encontrados.

Fluxo:

1. `carregar_json` lê o cenário e trata arquivo ausente ou malformado.
2. `validar_telemetria` verifica presença, tipos e domínios válidos.
3. `calcular_energia` calcula energia inicial, perdas, energia útil, saldo e autonomia.
4. `verificar_pre_decolagem` avalia as faixas operacionais e módulos críticos.
5. `executar_cenario` integra as etapas.
6. `formatar_resultado` apresenta o resultado sem recalcular valores.

## 2. Organização e descrição da telemetria — requisito 1.1

| Campo | Unidade/tipo | Domínio válido | Faixa segura |
| --- | --- | --- | --- |
| `temperatura_interna_c` | °C, número | -100 a 150 | 15 a 30, inclusive |
| `temperatura_externa_c` | °C, número | -200 a 150 | -150 a 120, inclusive |
| `integridade_estrutural` | inteiro 0/1 | 0 ou 1 | 1 |
| `energia_pct` | %, número | 0 a 100 | 50 a 100, inclusive |
| `pressao_tanque_kpa` | kPa, número | > 0 e <= 1000 | 90 a 110, inclusive |
| `modulos` | objeto | todos os módulos | todos em `OK` |

Módulos críticos: suporte de vida, energia, comunicação, propulsão e navegação.
Os estados aceitos são `OK` e `FALHA`.

Validade estrutural e segurança operacional são etapas diferentes. Por exemplo,
`integridade_estrutural = 0` e `propulsao = FALHA` são dados válidos, mas
obrigam o aborto. Já `energia_pct = 150` é uma entrada inválida.

### Cenários versionados

| Arquivo | Alteração principal | Resultado esperado |
| --- | --- | --- |
| `dados/nominal.json` | nenhuma | PRONTO PARA DECOLAR |
| `dados/falha_temperatura.json` | temperatura interna = 31 °C | aborto por temperatura |
| `dados/falha_modulo.json` | propulsão em FALHA | aborto por módulo |
| `dados/falha_energia.json` | consumo de decolagem = 80 kWh | aborto por energia |
| `dados/entrada_invalida.json` | pressão ausente | aborto por erro de entrada |

## 3. Algoritmo de verificação — requisito 1.2

Pseudocódigo resumido:

```text
INÍCIO
  carregar cenário
  validar estrutura, tipos e domínios
  SE houver erros:
      retornar DECOLAGEM ABORTADA e todos os erros
  calcular energia inicial, perdas, energia útil, saldo e autonomia
  motivos <- lista vazia
  PARA cada faixa segura:
      registrar valores abaixo ou acima dos limites
  verificar integridade estrutural
  PARA cada módulo crítico:
      registrar módulo em falha
  SE saldo energético <= 0:
      registrar energia insuficiente
  SE motivos estiver vazia:
      retornar PRONTO PARA DECOLAR
  SENÃO:
      retornar DECOLAGEM ABORTADA e todos os motivos
FIM
```

As fronteiras são inclusivas. O verificador não encerra na primeira falha:
isso mantém a decisão auditável e permite corrigir todos os problemas detectados.

## 4. Script em Python — requisito 1.3

Os módulos possuem responsabilidades separadas:

- `src/validacao.py`: leitura segura e validação de campos.
- `src/energia.py`: fórmulas energéticas e validação numérica.
- `src/verificacao.py`: regras operacionais e decisão.
- `src/missao.py`: orquestração do fluxo completo.
- `src/apresentacao.py`: saída textual legível.
- `notebooks/pre_decolagem.ipynb`: demonstração executável.

Trecho central de integração:

```python
from src.missao import executar_cenario, LIMITES_PADRAO
from src.apresentacao import formatar_resultado

# Executar a partir da raiz do repositório.
resultado = executar_cenario("dados/nominal.json", LIMITES_PADRAO)
print(formatar_resultado(resultado))
```

A suíte automatizada cobre cenários nominais, limites, falhas de cada módulo,
múltiplas falhas, entradas inválidas, erros de energia, integração e apresentação.

## 5. Análise energética — requisito 1.4

Entradas:

- capacidade total (`capacidade_kwh`);
- carga atual (`carga_pct`);
- consumo estimado na decolagem (`consumo_decolagem_kwh`);
- perdas (`perdas_pct`);
- potência média opcional para autonomia (`potencia_media_kw`).

Fórmulas:

```text
energia_inicial = capacidade_kwh × carga_pct / 100
perdas          = energia_inicial × perdas_pct / 100
energia_util    = energia_inicial − perdas
saldo           = energia_util − consumo_decolagem_kwh
autonomia_h     = saldo / potencia_media_kw, somente se saldo > 0
```

Exemplo nominal executado:

```text
capacidade = 100 kWh
carga = 80%  → energia inicial = 80 kWh
perdas = 5% de 80 kWh = 4 kWh
energia útil = 76 kWh
consumo da decolagem = 20 kWh
saldo = 56 kWh
potência média = 10 kW
autonomia = 5,6 h
```

No cenário de falha energética, o consumo é 80 kWh. O saldo passa a -4 kWh,
a missão não é viável e a autonomia não é calculada.

## 6. Análise assistida por IA — requisito 1.5

A consulta ao Codex/GPT-5 solicitou classificação dos dados, identificação de
anomalias e sugestões de risco para os cenários nominal, falha de temperatura
e falha de propulsão. O prompt forneceu explicitamente as faixas, as fórmulas e
a orientação de não autorizar uma operação real.

Resultados representativos:

- nominal: leituras dentro das faixas, saldo de 56 kWh e autonomia de 5,6 h;
- temperatura: 31 °C excede o máximo interno de 30 °C;
- propulsão: `propulsao = FALHA` impede a missão mesmo com energia adequada;
- limitação declarada: os dados não permitem diagnosticar a causa interna da falha.

A revisão humana comparou cada afirmação com os JSONs, `LIMITES_PADRAO`,
`calcular_energia` e `verificar_pre_decolagem`. Em caso de divergência,
prevalece a implementação determinística.

O projeto também contém uma extensão opcional em `src/geracao.py`, que usa
`GaussianMixture` para gerar dados sintéticos. Essa extensão não é usada para
a decisão autoritativa nem é requisito para executar o notebook principal.

## 7. Reflexão crítica — requisito 1.6

### Ética e responsabilidade

Decisões de segurança precisam ser explicáveis. O sistema acumula motivos,
informa valores e limites e aborta quando faltam dados indispensáveis. A IA
serve como apoio interpretativo; não recebe autoridade para aprovar a missão.

### Impacto social

Tecnologias espaciais podem gerar aplicações em medicina, agricultura,
manufatura e observação terrestre. Ao mesmo tempo, o investimento espacial
disputa recursos com outras prioridades sociais. O simulador não resolve essa
decisão política, mas evita apresentar dados sintéticos como segurança real.

### Sustentabilidade tecnológica

O balanço energético torna perdas e consumo explícitos e evita declarar
autonomia quando o saldo é nulo ou negativo. O projeto não mediu emissões ou
consumo computacional; portanto, não faz alegações ambientais sem dados.

## 8. Evidências de execução

As imagens em `evidencias/` são capturas reais da janela do VS Code, obtidas
após executar o notebook e a suíte de testes pela interface:

1. `01-nominal.png`: decisão positiva, saldo de 56 kWh e autonomia de 5,6 h.
2. `02-aborto.png`: temperatura interna de 31 °C e aborto explicado.
3. `03-energia.png`: saldo de -4 kWh, aborto e autonomia indisponível.
4. `04-testes.png`: terminal integrado com 52 testes aprovados e resultado OK.

O procedimento reproduzível está em `evidencias/README.md`.

## 9. Validação e resultados

Em 16/09/2026 foram executados:

```sh
python -m unittest discover -s tests -v
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/pre_decolagem.ipynb
```

Resultado: **52 testes aprovados, 0 falhas**, e notebook executado integralmente.

| Cenário | Decisão | Saldo | Autonomia |
| --- | --- | ---: | ---: |
| nominal | PRONTO PARA DECOLAR | 56 kWh | 5,6 h |
| falha de temperatura | DECOLAGEM ABORTADA | 56 kWh | 5,6 h |
| falha de energia | DECOLAGEM ABORTADA | -4 kWh | não calculada |
| entrada inválida | DECOLAGEM ABORTADA | indisponível | indisponível |

## 10. Conclusão

O projeto atende aos seis itens técnicos solicitados: telemetria organizada,
algoritmo, script Python, análise energética, análise assistida por IA e
reflexão crítica. O repositório inclui notebook executável, README com
instruções e prints, esta versão textual editável e o PDF. A fonte executável
da diagramação está em `scripts/gerar_relatorio.py`.

A separação entre validação, energia, decisão e apresentação reduz ambiguidades
e permite rastrear cada resultado. O uso de dados sintéticos e limites
hipotéticos permanece explicitamente identificado.

## Referências

- FIAP ON. Atividade Integradora — Relatório Operacional de Pré-Decolagem.
  Consultada em 16 set. 2026.
- NASA. Technology Transfer and Spinoffs.
  https://www.nasa.gov/space-technology-mission-directorate/technology-transfer-spinoffs/
- Documentação e código do projeto:
  https://github.com/bkampdev/FIAP-PBL-FASE-1

## Controle da versão

- Base integrada: `a487de4` (merge da PR #27).
- Notebook reexecutado e artefatos consolidados em 16/09/2026.
- A confirmação do envio no FIAP ON deve ser registrada separadamente; a
  presença deste arquivo no GitHub não equivale à submissão no portal.


## Atualização do gerador integrado

O notebook importa os módulos de geração, missão e apresentação e exibe saída textual compacta. A base sintética de pressão foi corrigida de aproximadamente 420 kPa para 94–104 kPa, compatível com os limites didáticos de 90–110 kPa; não houve conversão de unidades nem alteração dos limites. Os dados continuam aleatórios, sem seed fixa na chamada e sem substituição de amostras para aprovar. O nominal pode abortar por falhas sorteadas; os três cenários de falha abortam deliberadamente.

Uma verificação com 100 sorteios nominais produziu 87 aprovações e 13 abortos, contagem observada e não garantida. Os 52 testes passaram e o notebook executou integralmente. As capturas reais já incluídas correspondem aos cenários JSON determinísticos, não à amostragem do gerador.
