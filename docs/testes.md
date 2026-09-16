# Matriz de testes — pré-decolagem

Esta matriz complementa `tests/test_pre_decolagem.py` e os testes unitários já existentes dos módulos de decisão e energia.

## Comando reproduzível

```bash
python -m unittest discover -s tests -v
```

O resultado obtido e a contagem final foram registrados após executar a suíte na branch integrada.

## Casos cobertos

| Grupo | Entrada alterada | Resultado esperado | Evidência executável |
|---|---|---|---|
| Nominal | nenhuma | `PRONTO PARA DECOLAR`, sem motivos | `test_nominal_pronto_e_sem_motivos` |
| Fronteiras | abaixo/mínimo/máximo/acima para cada faixa numérica | limites inclusivos passam; fora aborta com motivo do campo | `test_fronteiras_numericas` |
| Integridade | 1 e 0 | 1 aprova; 0 aborta com motivo | testes `test_integridade_*` |
| Módulos | cada módulo crítico em `FALHA` isoladamente | aborto e motivo correspondente | `test_cada_modulo_critico_em_falha` |
| Múltiplas falhas | temperatura alta + propulsão em falha + energia zero | aborto com todos os motivos necessários | `test_multiplas_falhas_acumulam_motivos` |
| Campo ausente | remove `energia_pct` | erro de validação citando o campo | `test_validador_rejeita_campo_ausente` |
| `null` | `energia_pct = None` | erro de tipo/número finito | `test_validador_rejeita_null_em_numero` |
| Texto por número | temperatura `"22"` | erro de tipo/número finito | `test_validador_rejeita_texto_no_lugar_de_numero` |
| Energia inválida | -1 e 101% | erro de domínio | `test_validador_rejeita_energia_fora_do_dominio` |
| Carga divergente | `energia_pct` diferente de `carga_pct` | erro de entrada; verificação e cálculo usam a mesma carga | `test_validador_rejeita_carga_energetica_divergente` |
| Estado de módulo desconhecido | `DESCONHECIDO` | erro de validação | `test_validador_rejeita_estado_desconhecido_de_modulo` |
| Módulos incompletos | remove `navegacao` | erro citando módulo ausente | `test_validador_rejeita_modulos_incompletos` |
| Não finitos | NaN, +inf, -inf | erro de número finito | `test_validador_rejeita_numeros_nao_finitos` |
| Falha operacional válida | integridade 0 + módulo `FALHA` | validador aceita formato; decisão operacional deve abortar | `test_falha_operacional_continua_sendo_dado_valido` |
| Conta manual | 100 kWh, 80%, 20 kWh, perdas 5%, potência 10 kW | autonomia 5,6 h | `test_energia_exemplo_manual_100_kwh` |
| Saldo energético | positivo / zero / negativo | positivo gera autonomia; zero/negativo não liberam missão | testes `test_energia_saldo_*` |
| Potência | zero / negativa | não ocorre aprovação indevida; zero não divide por zero | testes `test_potencia_*` |

## Conta manual independente

Para `capacidade=100 kWh`, `carga=80%`, `perdas=5%`, `consumo=20 kWh` e `potência=10 kW`:

1. energia inicial = 100 × 0,80 = 80 kWh;
2. perdas = 80 × 0,05 = 4 kWh;
3. energia útil = 80 - 4 = 76 kWh;
4. saldo após decolagem = 76 - 20 = 56 kWh;
5. autonomia = 56 / 10 = **5,6 h**.

A base de incidência das perdas é, portanto, a energia inicialmente disponível após aplicar a carga, e não a capacidade nominal total.

## Resultado obtido

Execução realizada em **15/09/2026**, na branch `feat/analise-energetica`, integrada sobre a branch `davi`.

Comando utilizado:

```bash
python -m unittest discover -s tests -v
```

Resultado da execução:

- **31 testes executados**
- **31 testes aprovados**
- **0 testes com falha**
- Tempo de execução: **0.008s**
- Status final: **OK**

A suíte foi executada após a integração dos módulos de validação, decisão e energia disponíveis na branch atual.

Não foram identificadas falhas nos casos testados.

## Observação de responsabilidade

`src/verificacao.py` e `tests/test_verificacao.py` pertencem à implementação de decisão de Lorenzo. Esta matriz apenas amplia a cobertura conforme a issue #5 e não modifica as regras daquele módulo.
