# Análise assistida por IA: pré-decolagem

## Registro da consulta

Esta é uma análise didática de dados sintéticos. A IA foi usada como apoio para
classificar leituras, apontar anomalias e sugerir riscos; ela **não** autoriza
uma decolagem nem substitui as regras determinísticas do projeto.

- Ferramenta: Codex.
- Modelo identificado nesta sessão: GPT-5.
- Data da consulta: 16/09/2026.
- Dados usados: `dados/nominal.json`, `dados/falha_temperatura.json` e
  `dados/falha_modulo.json` no commit `1113a83ebef4f588320432097197d359a252600b`.
- Referência executável para a decisão: `src/missao.py`, que valida a entrada,
  chama `src/energia.py` e delega as regras de pré-decolagem a
  `src/verificacao.py`.

As faixas usadas na consulta são as hipóteses didáticas versionadas em
`docs/telemetria.md`: temperatura interna de 15 a 30 °C, temperatura externa
de -150 a 120 °C, energia de 50 a 100% e pressão de 90 a 110 kPa. Todos os
módulos críticos devem estar em `OK`, a integridade estrutural deve ser `1` e a
energia após a decolagem deve ter saldo positivo.

## Prompt efetivamente enviado

> Analise os três cenários sintéticos abaixo usando **apenas** as faixas e
> regras informadas. Para cada cenário, classifique os campos, indique
> anomalias com o campo, valor e regra correspondente e descreva riscos ou
> sugestões. Se faltar uma informação, declare a incerteza e não invente
> parâmetros. Esta é uma simulação didática: não dê autorização operacional
> real para uma nave.
>
> Regras: temperatura interna 15–30 °C; externa -150–120 °C; energia 50–100%;
> pressão 90–110 kPa; integridade estrutural igual a 1; todos os módulos em
> `OK`. O cálculo energético é: energia inicial = capacidade × carga/100;
> perdas = energia inicial × perdas/100; saldo = energia inicial − perdas −
> consumo. A decolagem só é viável com saldo positivo; a autonomia é
> saldo/potência somente nesse caso.
>
> Cenário nominal: temperatura interna 22 °C, externa -50 °C, energia 80%,
> pressão 100 kPa, integridade 1, todos os módulos `OK`, capacidade 100 kWh,
> carga 80%, perdas 5%, consumo 20 kWh e potência 10 kW.
>
> Cenário de temperatura: igual ao nominal, exceto temperatura interna 31 °C.
>
> Cenário de propulsão: igual ao nominal, exceto
> `modulos.propulsao = FALHA`.

## Resposta obtida

> **Nominal.** Todas as leituras informadas estão dentro das faixas: 22 °C
> interna, -50 °C externa, 80% de energia e 100 kPa. Integridade 1 e módulos
> em `OK` não apontam falha. O saldo calculado é 56 kWh
> (100 × 0,80 − 4 − 20), positivo; com 10 kW, a autonomia estimada é 5,6 h.
> Pela informação fornecida, não há anomalia operacional a apontar.
>
> **Temperatura.** A temperatura interna de 31 °C está 1 °C acima do máximo
> de 30 °C. Os demais valores apresentados são nominais e o saldo continua em
> 56 kWh, mas a leitura interna indica condição fora da faixa de segurança.
> O risco é operar fora da condição térmica didática definida; a sugestão é
> investigar e normalizar o sistema térmico antes de prosseguir.
>
> **Propulsão.** `modulos.propulsao = FALHA` viola a regra de que todos os
> módulos críticos devem estar em `OK`. Mesmo com temperatura, pressão,
> energia e saldo nominalmente adequados, há risco de indisponibilidade de um
> sistema crítico. A sugestão é diagnosticar e corrigir o módulo de propulsão
> antes de uma nova avaliação. Não há dados suficientes para diagnosticar a
> causa interna da falha.

## Revisão humana contra a implementação

| Afirmação da IA | Evidência nos dados e no código | Concordância e decisão humana |
|---|---|---|
| O cenário nominal não tem anomalias e tem saldo de 56 kWh com autonomia de 5,6 h. | `dados/nominal.json` fornece 100 kWh, 80%, 5%, 20 kWh e 10 kW. `calcular_energia` retorna saldo `56.0`, autonomia `5.6` e `viavel=True`. | Concordamos. `executar_cenario` deve retornar `PRONTO PARA DECOLAR`. |
| 31 °C excede a faixa interna de 15–30 °C, mesmo com energia suficiente. | `dados/falha_temperatura.json` altera somente `temperatura_interna_c` para `31`; `LIMITES_PADRAO` aplica máximo `30`. | Concordamos. O algoritmo deve abortar por temperatura interna; o saldo não elimina essa falha. |
| Falha em propulsão impede a decolagem, ainda que os demais valores sejam nominais. | `dados/falha_modulo.json` define `propulsao` como `FALHA`; `verificar_pre_decolagem` registra `Modulo critico em falha: propulsao`. | Concordamos. O algoritmo deve abortar por falha de módulo crítico. |
| Não é possível identificar a causa interna da falha de propulsão. | Os dados só informam o estado do módulo; não há diagnóstico, histórico ou telemetria do componente. | Concordamos. Essa limitação deve ser declarada, não preenchida com suposições. |

Como verificação adicional do cálculo, `dados/falha_energia.json` usa consumo
de 80 kWh: o saldo é -4 kWh, `viavel` é falso e a autonomia é `None`. A IA não
foi usada para substituir essa regra; o resultado correto continua sendo
`DECOLAGEM ABORTADA`.

## Conclusão

A consulta foi útil para transformar as leituras em explicações compreensíveis
e para explicitar riscos e lacunas de informação. Sua resposta só é aceita
depois da comparação com os JSONs versionados, as faixas documentadas e a
execução determinística. Em caso de divergência, prevalecem os módulos de
validação, energia e verificação do projeto.
