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
- Hipótese do grupo sobre reserva energética: ...
- Todas as falhas são acumuladas; o algoritmo não para na primeira.

## 3. Pseudocódigo
Presente no arquivo: pseudocodigo_verificacao.md

## 4. Saída
- Sem motivos: `{"decisao": "PRONTO PARA DECOLAR", "motivos": []}`
- Com motivos: `{"decisao": "DECOLAGEM ABORTADA", "motivos": [...]}`

## 5. Percursos demonstrados
### 5.1 Caso nominal
(entradas, passo a passo, saída)

### 5.2 Caso com múltiplas falhas
(entradas, passo a passo com motivos acumulados, saída)