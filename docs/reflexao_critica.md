# Reflexão crítica

## Introdução

Nosso projeto é um simulador educacional de verificação de pré-decolagem de uma estação/nave espacial. Os dados são sintéticos, os limites foram definidos pelo grupo e o sistema não é certificado. Então, o objetivo é aplicar os conceitos estudados, e não simular uma operação espacial real.

## Eixo 1: Ética e responsabilidade

Uma decisão de segurança precisa ser explicável. Por isso, a `verificar_pre_decolagem()` não para na primeira falha: ela registra todos os motivos encontrados. Se a temperatura estiver em 31 °C e o máximo for 30 °C, por exemplo, o resultado mostra o valor e o limite. Isso permite que uma pessoa entenda e audite a decisão.

Também não assumimos segurança quando falta informação. Se o resultado energético estiver ausente ou incompleto, a decolagem é abortada. A separação entre `validar_telemetria()` e `verificar_pre_decolagem()` segue a mesma ideia: 150% de energia é um dado impossível, enquanto 45% é possível, mas pode ser insuficiente para a decolagem. O Machine Learning também não toma a decisão final: o GaussianMixture apenas gera as leituras sintéticas.

## Eixo 2: Impacto social

A exploração espacial pode trazer benefícios que vão além da missão em si. 
Segundo a NASA, o programa Technology Transfer existe justamente para que 
tecnologias desenvolvidas em missões de exploração fiquem disponíveis ao 
público, e a publicação Spinoff reúne os casos de cada ano — aplicações em 
medicina, agricultura, manufatura e uso de dados de satélite. Por outro lado, 
a exploração espacial também envolve custos e recursos que poderiam ser 
destinados a outras necessidades. Essa é uma questão de prioridade social, 
e não algo que nosso projeto consiga determinar.

No nosso caso, o principal impacto está na forma como o sistema apresenta seus resultados. Como trabalhamos com dados sintéticos e limites hipotéticos, precisamos deixar isso claro para não passar a impressão de que o simulador representa uma validação real de segurança.

## Eixo 3: Sustentabilidade

O módulo de energia calcula energia inicial, perdas, energia útil e saldo em kWh. Isso aparece no cenário `falha_energia.json`: a carga de 80% é válida, mas o consumo de decolagem de 80 kWh deixa saldo de -4 kWh e impede a missão.

A própria computação também consome recursos, mas não medimos consumo elétrico ou emissão de carbono. Portanto, não temos dados para afirmar qual é o impacto ambiental do nosso sistema.

## Recomendações

Para as próximas versões, manteríamos a separação entre validação e verificação e o registro dos motivos de falha. Também seria interessante aumentar os testes para casos como múltiplas falhas e resultados energéticos incompletos.

## Conclusão

O principal aprendizado foi perceber que uma verificação de segurança não é apenas responder “pode” ou “não pode”. O sistema precisa explicar o motivo e tratar corretamente situações como dados inválidos ou incompletos.

No nosso caso, isso ficou dividido entre `validar()`, `verificar_pre_decolagem()` e o modelo de geração. Ao mesmo tempo, reconhecemos que o projeto é apenas uma simulação educacional, com dados sintéticos e limites hipotéticos, e não uma solução para uma operação real.

## Referências

NASA. *Technology Transfer and Spinoffs*. Disponível em: 
https://www.nasa.gov/space-technology-mission-directorate/technology-transfer-spinoffs/. 
Acesso em: 16 set. 2026.
