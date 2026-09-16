# Análise Energética do Módulo de Decolagem e Autonomia

## 1. Variáveis e Unidades
* `capacidade_kwh` (kWh): Capacidade total do banco de baterias.
* `carga_pct` (%): Porcentagem atual da carga disponível (0 a 100%).
* `consumo_decolagem_kwh` (kWh): Energia consumida durante a fase de decolagem.
* `perdas_pct` (%): Taxa de perdas estimada sobre a energia inicialmente armazenada.
* `potencia_media_kw` (kW): Potência média exigida para o voo de cruzeiro após a decolagem.

## 2. Hipóteses e Fórmulas
1. Energia Inicial Storeada ($E_{inicial}$):
   $$E_{inicial} = \text{capacidade\_kwh} \times \left(\frac{\text{carga\_pct}}{100}\right)$$

2. Perdas de Bateria ($E_{perdas}$):
   A base das perdas é aplicada sobre a energia inicial armazenada:
   $$E_{perdas} = E_{inicial} \times \left(\frac{\text{perdas\_pct}}{100}\right)$$

3. Energia Útil ($E_{util}$):
   $$E_{util} = E_{inicial} - E_{perdas}$$

4. Saldo Energético Pós-Decolagem ($E_{saldo}$):
   $$E_{saldo} = E_{util} - \text{consumo\_decolagem\_kwh}$$

5. Autonomia Temporal ($A_h$) e Viabilidade:
   * Se $E_{saldo} > 0$: $\text{viavel} = \text{True}$. Quando $\text{potencia\_media\_kw}$ é informada e positiva, $A_h = \frac{E_{saldo}}{\text{potencia\_media\_kw}}$; sem potência, $A_h = \text{None}$.
   * Se $E_{saldo} \le 0$: $\text{viavel} = \text{False}$ e $A_h = \text{None}$.
   * Capacidade, consumo, percentuais e potência informada devem ser números finitos nos domínios indicados. Valores inválidos, inclusive potência zero/negativa, geram `ValueError`.

## 3. Exemplo Calculado Manualmente
* Dados: Capacidade = 100 kWh | Carga = 80% | Perdas = 10% | Decolagem = 20 kWh | Potência = 10 kW
* Cálculo:
  * $E_{inicial} = 100 \times 0.80 = 80\text{ kWh}$
  * $E_{perdas} = 80 \times 0.10 = 8\text{ kWh}$
  * $E_{util} = 80 - 8 = 72\text{ kWh}$
  * $E_{saldo} = 72 - 20 = 52\text{ kWh}$
  * $A_h = \frac{52}{10} = 5,2\text{ horas}$ ($\text{Viável} = \text{True}$)
