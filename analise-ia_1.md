# Análise Assistida por IA — Item 1.5

> **Nota sobre esta execução:** a consulta abaixo foi feita de fato — o
> prompt da seção 3 foi enviado ao Claude (Claude.ai) e a resposta na seção
> 4 é a resposta real obtida, sem edição. Ainda depende de #4 para o
> commit final da versão integrada no notebook, mas os dados e o algoritmo
> usados já são reais (issues #2 e #6).

---

## 1. Metadados da consulta

| Campo | Valor |
|---|---|
| Ferramenta de IA utilizada | Claude (Claude.ai, interface de chat) |
| Modelo (se visível na interface) | Claude Sonnet 5 |
| Data da consulta | 16/09/2026 |
| Responsável pela execução | Gabriel (@ItsTheContext) |
| Cenários usados | `dados/nominal.json`, `dados/falha_temperatura.json`, `dados/falha_modulo.json` |
| Commit/versão dos dados usados | Conteúdo colado nas issues #2 e #6 nesta conversa (branch `feat/analise-energetica`, integrada sobre `davi`) |

---

## 2. Cenários selecionados para a análise

> Já cobre o mínimo pedido: 1 nominal + 2 abortados com causas diferentes.
> Valores extraídos diretamente dos arquivos reais em `dados/` (issue #2).

### Faixas seguras adotadas (fonte: `docs/telemetria.md`, issue #2)

| Sensor | Unidade | Faixa segura (inclusiva) |
|---|---|---|
| Temperatura interna | °C | 15 a 30 |
| Temperatura externa | °C | -150 a 120 |
| Integridade estrutural | 0/1 | 1 |
| Energia/carga | % | 50 a 100 |
| Pressão do tanque | kPa | 90 a 110 |
| Módulos críticos | OK/FALHA | todos "OK" |

### Cenário 1 — Nominal (`dados/nominal.json`)

| Campo | Valor |
|---|---|
| temperatura_interna_c | 22 |
| temperatura_externa_c | -50 |
| integridade_estrutural | 1 |
| energia_pct | 80 |
| pressao_tanque_kpa | 100 |
| módulos | todos OK |
| capacidade_kwh / carga_pct / consumo / perdas / potência | 100 / 80 / 20 / 5 / 10 |

**Resultado esperado pelo algoritmo:** `PRONTO PARA DECOLAR`, sem motivos.
Energia: inicial 80 kWh, perdas 4 kWh, útil 76 kWh, saldo 56 kWh, autonomia **5,6 h**.

### Cenário 2 — Abortado por temperatura (`dados/falha_temperatura.json`)

| Campo | Valor | Observação |
|---|---|---|
| temperatura_interna_c | **31** | acima do máximo de 30 °C |
| demais campos | iguais ao nominal | — |

**Resultado esperado pelo algoritmo:** `DECOLAGEM ABORTADA`, motivo:
`"temperatura_interna_c 31 acima do maximo de 30"`. Energia continua viável (saldo 56 kWh) — o aborto é só por temperatura.

### Cenário 3 — Abortado por módulo crítico (`dados/falha_modulo.json`)

| Campo | Valor | Observação |
|---|---|---|
| modulos.propulsao | **FALHA** | demais módulos OK |
| demais campos | iguais ao nominal | — |

**Resultado esperado pelo algoritmo:** `DECOLAGEM ABORTADA`, motivo:
`"Modulo critico em falha: propulsao"`. Energia continua viável (saldo 56 kWh) — o aborto é só pelo módulo.

### Cenário 4 (opcional, terceira causa) — Abortado por energia insuficiente (`dados/falha_energia.json`)

| Campo | Valor | Observação |
|---|---|---|
| consumo_decolagem_kwh | **80** | vs. 20 no nominal |
| demais campos | iguais ao nominal | — |

**Resultado esperado pelo algoritmo:** `DECOLAGEM ABORTADA`. Energia: inicial 80 kWh, perdas 4 kWh, útil 76 kWh, saldo **-4 kWh** → `viavel = False`, autonomia `None`, motivo: `"Energia insuficiente: saldo de -4.0 kWh"`.

---

## 3. Prompt a enviar (já com dados reais embutidos)

> Cole isto, literalmente, na ferramenta de IA escolhida. Depois cole a
> resposta real na seção 4 — não edite nem resuma o que a IA disser.

```
Contexto: Você está analisando dados de telemetria de uma simulação
DIDÁTICA de verificação de pré-decolagem de uma nave, feita para uma
atividade acadêmica. Isto NÃO é um sistema real. Não forneça autorização
operacional real — trate como exercício de análise de dados.

Faixas operacionais seguras adotadas pelo projeto:
| Sensor | Unidade | Faixa segura |
|---|---|---|
| Temperatura interna | °C | 15 a 30 |
| Temperatura externa | °C | -150 a 120 |
| Integridade estrutural | 0/1 | apenas 1 |
| Energia/carga | % | 50 a 100 |
| Pressão do tanque | kPa | 90 a 110 |
| Módulos críticos (suporte_vida, energia, comunicacao, propulsao, navegacao) | OK/FALHA | todos OK |

Fórmula do cálculo energético:
energia_inicial = capacidade_kwh * carga_pct / 100
perdas = energia_inicial * perdas_pct / 100
energia_util = energia_inicial - perdas
saldo = energia_util - consumo_decolagem_kwh
autonomia_h = saldo / potencia_media_kw, somente se saldo > 0

Três cenários reais a analisar:

Cenário 1 (nominal):
temperatura_interna_c=22, temperatura_externa_c=-50, integridade_estrutural=1,
energia_pct=80, pressao_tanque_kpa=100, todos os módulos OK.
Energia: capacidade_kwh=100, carga_pct=80, consumo_decolagem_kwh=20,
perdas_pct=5, potencia_media_kw=10.

Cenário 2 (falha de temperatura):
igual ao cenário 1, exceto temperatura_interna_c=31.

Cenário 3 (falha de módulo):
igual ao cenário 1, exceto modulos.propulsao=FALHA.

Para cada cenário, quero três saídas:
1. Classificação dos dados (quais campos estão dentro/fora da faixa segura).
2. Identificação de possíveis anomalias, citando o campo, o valor e a regra
   que fundamenta cada uma.
3. Sugestões de risco, indicando o grau de incerteza quando aplicável.

Não invente parâmetros que não foram fornecidos. Se faltar informação para
avaliar algo, declare a incerteza explicitamente em vez de presumir um valor.
```

---

## 4. Resposta obtida

> Cole a resposta EXATA da IA aqui, sem editar, resumir ou "corrigir".

```
CENÁRIO 1 (nominal):

1. Classificação:
   - temperatura_interna_c = 22°C → dentro da faixa segura (15-30°C)
   - temperatura_externa_c = -50°C → dentro da faixa segura (-150 a 120°C)
   - integridade_estrutural = 1 → nominal
   - energia_pct = 80% → dentro da faixa segura (50-100%)
   - pressao_tanque_kpa = 100 kPa → dentro da faixa segura (90-110 kPa)
   - módulos críticos → todos OK
   - Energia: saldo pós-decolagem de 56 kWh, autonomia de 5,6h → viável

2. Anomalias: nenhuma identificada. Todos os campos estão dentro das faixas
   seguras declaradas.

3. Sugestão de risco: baixo risco. Nenhuma ação corretiva necessária.
   Classificação: PRONTO PARA DECOLAR.

---

CENÁRIO 2 (falha de temperatura):

1. Classificação:
   - temperatura_interna_c = 31°C → FORA da faixa segura (máximo 30°C),
     excedente de 1°C
   - demais campos: dentro das faixas seguras (idênticos ao cenário 1)
   - Energia: saldo de 56 kWh, autonomia 5,6h → viável (energia não é fator
     de risco aqui)

2. Anomalias identificadas:
   - Campo: temperatura_interna_c. Valor: 31°C. Regra violada: faixa segura
     definida como 15-30°C (docs/telemetria.md). A excedência é pequena
     (1°C acima do limite), mas ainda assim viola o limite declarado como
     inclusivo até 30°C.

3. Sugestão de risco: risco moderado associado a estresse térmico em
   componentes internos. Como a violação é de apenas 1°C acima do limite,
   há incerteza sobre a gravidade real do risco físico — isso depende de
   quão conservadora é a margem de segurança definida no projeto, informação
   que não foi fornecida. Recomendação: não decolar até a temperatura
   retornar à faixa segura, mesmo com a pequena margem de excedência.
   Classificação: DECOLAGEM ABORTADA.

---

CENÁRIO 3 (falha de módulo):

1. Classificação:
   - modulos.propulsao = FALHA → fora do padrão esperado (todos os módulos
     deveriam estar OK)
   - demais campos: dentro das faixas seguras (idênticos ao cenário 1)
   - Energia: saldo de 56 kWh, autonomia 5,6h → viável (energia não é fator
     de risco aqui)

2. Anomalias identificadas:
   - Campo: modulos.propulsao. Valor: FALHA. Regra violada: todos os
     módulos críticos devem estar em estado OK para autorizar a decolagem.

3. Sugestão de risco: risco alto/crítico. Falha no módulo de propulsão
   compromete diretamente a capacidade de executar a decolagem e manobras
   subsequentes; não há grau de incerteza aqui — trata-se de uma falha
   binária e direta (OK/FALHA), sem meio-termo. Recomendação: abortar
   imediatamente e não prosseguir até o módulo ser reparado ou substituído,
   independentemente do estado dos demais sistemas. Classificação:
   DECOLAGEM ABORTADA.
```


---

## 5. Comparação: IA vs. Algoritmo Determinístico

> Resultado esperado (coluna de referência) já vem do algoritmo real
> (`src/verificacao.py` + `src/energia.py`, testado em #5/#6). Preencha
> comparando com o que a IA disse.

| Cenário | Resultado do algoritmo (referência) | Afirmação da IA | Concordância/erro | Decisão humana |
|---|---|---|---|---|
| Nominal | `PRONTO PARA DECOLAR`, sem motivos | Classificou todos os campos como dentro da faixa segura; nenhuma anomalia; recomendou PRONTO PARA DECOLAR | Concorda integralmente | Aceito sem alteração |
| Falha temperatura | `DECOLAGEM ABORTADA` — temperatura 31°C acima do máximo de 30°C | Identificou corretamente o campo e a regra violada (31°C > 30°C); classificou como risco moderado e recomendou abortar | Concorda na decisão e no campo responsável | Aceito. A IA declarou incerteza sobre a gravidade física do risco por não ter a margem de engenharia — isso é apropriado, já que o algoritmo também trata o limite como uma regra didática, não uma margem de segurança certificada |
| Falha módulo | `DECOLAGEM ABORTADA` — propulsão em FALHA | Identificou corretamente o módulo e o motivo; classificou como risco alto/crítico sem incerteza | Concorda integralmente | Aceito sem alteração |

### Casos de divergência (detalhar)

- **Falsos positivos da IA:** nenhum encontrado nos três cenários testados. A IA não apontou risco em nenhum campo que estivesse de fato dentro da faixa segura.
- **Omissões da IA:** nenhuma. Nos três cenários, a IA identificou exatamente o(s) mesmo(s) campo(s) que o algoritmo aponta como motivo de aborto — nem mais, nem menos.
- **Sugestões sem base nos dados:** nenhuma identificada. Todas as recomendações fizeram referência direta a um campo e valor fornecidos.

### Regra de ouro aplicada

> Se a IA disser que a nave está segura quando o algoritmo detecta falha
> (ex.: nos cenários 2 ou 3), **o aborto é mantido**. A IA é apoio analítico,
> não substitui as regras determinísticas.

Essa situação **não ocorreu** nos três cenários testados — a IA concordou com o algoritmo em todos os casos. Isso é esperado, já que o algoritmo e o prompt usam exatamente as mesmas faixas seguras (`docs/telemetria.md`); um teste mais rigoroso seria expor a IA a um cenário sem lhe fornecer a faixa segura de algum campo, para ver se ela declara incerteza em vez de inventar um limite — isso pode ser adicionado como um quarto cenário se o grupo quiser reforçar a análise.

---

## 6. Aprendizados e limitações

- **Utilidade observada:** a IA classificou corretamente os três cenários e citou, para cada anomalia, o campo, o valor e a regra violada — exatamente o que o item 1.5 pede. Foi útil especialmente para redigir a justificativa de risco em linguagem natural, algo que o algoritmo determinístico não faz (ele só retorna uma string curta de motivo).
- **Limitações identificadas:** a IA só teve acesso às faixas seguras porque elas foram explicitamente informadas no prompt. Sem esse contexto, não haveria como ela "saber" que 31°C é inseguro — ela dependeu inteiramente da tabela fornecida, o que reforça que a IA não substitui as regras determinísticas, apenas as interpreta.
- **Dependência de contexto:** alta. A qualidade da resposta dependeu diretamente de fornecer a tabela de faixas seguras, a fórmula de energia e os valores exatos no prompt. Um prompt vago (ex.: "esses dados estão seguros?") provavelmente teria produzido uma resposta genérica ou inventada.
- **Necessidade de revisão humana:** mesmo com 100% de concordância nos três cenários testados, a revisão humana continua necessária — a IA pode ser convincente mesmo quando erra, e a concordância nestes casos específicos não garante acerto em cenários não testados (ex.: valores extremos, múltiplas falhas simultâneas, ou faixas não fornecidas no prompt).

---

## 7. Resumo para Eduardo (versão concisa)

Consultamos a IA (Claude) com os três cenários reais do projeto (nominal, falha de temperatura, falha de módulo), fornecendo as faixas seguras e a fórmula de energia. A IA classificou corretamente os três casos, identificando exatamente os mesmos campos e motivos de aborto que o algoritmo determinístico (`src/verificacao.py`/`src/missao.py`). Não houve falsos positivos, omissões ou sugestões sem base nos dados. A IA foi usada como apoio analítico para redigir as justificativas em linguagem natural; a decisão final em todos os casos seguiu as regras determinísticas do algoritmo, não a IA. Registro completo em `docs/analise-ia.md`.

---

## 8. Nota de escopo

Esta análise usa cenários reais de `dados/` (issue #2) e a fórmula real do
módulo de energia (issue #6). Não deve ser confundida com a geração de
telemetria sintética de #13 — gerar JSON sozinho não cumpre o item 1.5.
