# Como a geracao de dados está sendo feita?

No modulo 5 "O Surgimento da Inteligência que Apoia a Tomada de Decisao" temos um modulo que explica nao só sobre o surgimento da intelegicencia artificial mas fala a respeito de fluxos de projetos envolvendo IA e Machine Learning

Como o conteudo teorico foi disponibilizado resolvi construir um modelo de Machine Learning de verdade em vez de chamar uma API pronta. Achei que fazia mais sentido pro que a materia tava pedindo, e de quebra roda sem chave de API e sem internet.

O modelo é o GaussianMixture do scikit-learn. É nao supervisionado e a tarefa dele é estimacao de densidade: ele olha uma base de leituras e tenta reconstruir a funcao p(x) que gerou aquilo. Depois que ele aprende essa funcao, o metodo sample() sorteia pontos novos dela. É assim que a geracao acontece, os numeros que saem nao estavam na base.

Acabou virando dois modelos, porque tenho dois tipos de dado. Os quatro campos numericos (temperatura interna, externa, energia e pressao) vao no GaussianMixture. Os modulos nao dao pra jogar nele, porque gaussiana cospe numero continuo e modulo é OK ou FALHA, nao tem meio termo. Entao pros modulos eu conto a frequencia de falha no historico e uso isso como probabilidade no sorteio. Continua sendo estimacao de densidade, só que na versao discreta.

A base de treino fica em src/dados/base_treinamento.json, fora do codigo. Se depois a gente conseguir dados de verdade é só trocar o arquivo, nao precisa mexer em linha nenhuma.

Pra rodar é necessário a lib do scikit-learn
pip install numpy scikit-learn

E realizar a chamada da funcao telemetria, exemplo após chamada

from src.geracao import gerar_telemetria

print(gerar_telemetria("nominal"))

{'temperatura_interna_c': 20.09, 'temperatura_externa_c': -112.93, 'energia_pct': 88.9, 'pressao_tanque_kpa': 424.71, 'integridade_estrutural': 'NOMINAL', 'modulos': {'suporte_vida': 'OK', 'energia': 'OK', 'comunicacao': 'OK', 'propulsao': 'OK', 'navegacao': 'OK'}}


## Integração validada com a missão

O exemplo anterior é uma amostra bruta do modelo experimental: estados textuais
de integridade e ausência de campos energéticos impedem passá-la diretamente a
`executar_cenario`. A base de treinamento também pode gerar pressão fora da
faixa didática. Essa limitação não deve ser confundida com um cenário nominal seguro.

Use a função de integração:

```python
from src.geracao import gerar_cenario
from src.missao import executar_cenario, LIMITES_PADRAO
from src.apresentacao import formatar_resultado

dados = gerar_cenario("nominal", seed=42)
print(dados["geracao"])
print(formatar_resultado(executar_cenario(dados, LIMITES_PADRAO)))
```

O adaptador converte a integridade para 0/1, informa hipóteses energéticas
(100 kWh, consumo 20 kWh, perdas 5%, potência 10 kW) e sincroniza carga e energia.
Valida e verifica a amostra antes de usá-la. Se ela não for nominal segura,
usa o JSON nominal versionado, sem truncar os valores da amostra, e registra
`origem=arquivo_fallback` e os motivos em `geracao`. O fallback é um arquivo
fixo, não uma nova saída da IA. Depois aplica apenas a falha selecionada:
consumo de 100 kWh, propulsão em FALHA ou temperatura de 55 °C.

Os quatro cenários são nominal, energia_insuficiente, falha_modulo e falha_sensor.
A mesma seed reproduz a saída; seeds diferentes podem cair no mesmo fallback.
Não há API, credenciais ou promessa de que toda amostra do modelo seja segura.
A análise por IA obrigatória continua documentada em `docs/analise-ia.md`.
A integração e os resultados esperados são testados em `tests/test_geracao.py`.
