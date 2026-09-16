# Algoritmo de verificação pré-decolagem

## 1. Entradas
- `dados`: telemetria (#13) com temperaturas, pressão, carga, `integridade_estrutural` e `modulos`.
- `energia`: resultado do cálculo energético (#6), dicionário com `viavel` e `saldo_kwh`.
- `limites`: faixas operacionais [mínimo, máximo] definidas em #2.

## 2. Regras
- Cada campo de `limites` deve existir em `dados` e estar dentro da faixa.
- `integridade_estrutural` deve ser "NOMINAL" ou 1.
- Todos os módulos críticos devem existir e não estar em "FALHA".
- `energia["viavel"]` deve ser verdadeiro; a fórmula não é recalculada aqui.
- Política de reserva energética: não há reserva adicional fixa. A missão é viável
  somente quando `saldo_kwh > 0`; saldo igual a zero ou negativo interrompe a
  decolagem. Essa é a mesma regra aplicada por `calcular_energia` ao preencher
  `energia["viavel"]`.
- Todas as falhas são acumuladas; o algoritmo não para na primeira.

## 3. Pseudocódigo
Presente no arquivo: pseudocodigo_verificacao.md

## 4. Saída
- Sem motivos: `{"decisao": "PRONTO PARA DECOLAR", "motivos": []}`
- Com motivos: `{"decisao": "DECOLAGEM ABORTADA", "motivos": [...]}`

## 5. Percursos demonstrados
### 5.1 Caso nominal

Entradas:

```text
dados = {
  temperatura_interna_c: 22,
  temperatura_externa_c: -50,
  energia_pct: 80,
  pressao_tanque_kpa: 100,
  integridade_estrutural: 1,
  modulos: todos os cinco módulos críticos em "OK"
}
limites = {
  temperatura_interna_c: [15, 30],
  temperatura_externa_c: [-150, 120],
  energia_pct: [50, 100],
  pressao_tanque_kpa: [90, 110]
}
energia = calcular_energia(100, 80, 20, 5, 10)
```

Passo a passo:

1. Todos os valores de telemetria estão dentro das faixas.
2. A integridade `1` é aceita como nominal e os módulos críticos estão em `"OK"`.
3. O cálculo energético resulta em `energia_inicial_kwh = 80`, `perdas_kwh = 4`,
   `energia_util_kwh = 76`, `saldo_kwh = 56` e `viavel = verdadeiro`.
4. Não há motivos de aborto.

Saída:

```json
{"decisao": "PRONTO PARA DECOLAR", "motivos": []}
```

### 5.2 Caso com múltiplas falhas

Entradas: usar o mesmo caso nominal, alterando
`temperatura_interna_c` para `31`, o módulo `propulsao` para `"FALHA"` e a
energia para `calcular_energia(100, 80, 101, 0, 10)`.

Passo a passo:

1. `temperatura_interna_c = 31` excede o máximo de `30`.
2. O módulo crítico `propulsao` está em `"FALHA"`.
3. O cálculo energético resulta em `energia_inicial_kwh = 80`, `perdas_kwh = 0`,
   `energia_util_kwh = 80`, `saldo_kwh = -21` e `viavel = falso`.
4. As três falhas são acumuladas antes da decisão.

Saída:

```json
{
  "decisao": "DECOLAGEM ABORTADA",
  "motivos": [
    "temperatura_interna_c 31 acima do maximo de 30",
    "Modulo critico em falha: propulsao",
    "Energia insuficiente: saldo de -21.0 kWh"
  ]
}
```
