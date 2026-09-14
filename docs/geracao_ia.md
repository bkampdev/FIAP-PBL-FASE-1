# Como a geracao de dados está sendo feita?

No modulo 5 "O Surgimento da Inteligência que Apoia a Tomada de Decisao" temos um modulo que explica nao só sobre o surgimento da intelegicencia artificial mas fala a respeito de fluxos de projetos envolvendo IA e Machine Learning

Como o conteudo teorico foi disponibilizado resolvi construir um modelo de Machine Learning de verdade em vez de chamar uma API pronta. Achei que fazia mais sentido pro que a materia tava pedindo, e de quebra roda sem chave de API e sem internet.

O modelo é o GaussianMixture do scikit-learn. É nao supervisionado e a tarefa dele é estimacao de densidade: ele olha uma base de leituras e tenta reconstruir a funcao p(x) que gerou aquilo. Depois que ele aprende essa funcao, o metodo sample() sorteia pontos novos dela. É assim que a geracao acontece, os numeros que saem nao estavam na base.

Acabou virando dois modelos, porque tenho dois tipos de dado. Os quatro campos numericos (temperatura interna, externa, energia e pressao) vao no GaussianMixture. Os modulos nao dao pra jogar nele, porque gaussiana cospe numero continuo e modulo é OK ou FALHA, nao tem meio termo. Entao pros modulos eu conto a frequencia de falha no historico e uso isso como probabilidade no sorteio. Continua sendo estimacao de densidade, só que na versao discreta.

A base de treino fica em dados/base_treinamento.json, fora do codigo. Se depois a gente conseguir dados de verdade é só trocar o arquivo, nao precisa mexer em linha nenhuma.

Pra rodar é necessário a lib do scikit-learn
pip install numpy scikit-learn

E realizar a chamada da funcao telemetria, exemplo após chamada

import geracao

print(geracao.gerar_telemetria("nominal"))

{'temperatura_interna_c': 20.09, 'temperatura_externa_c': -112.93, 'energia_pct': 88.9, 'pressao_tanque_kpa': 424.71, 'integridade_estrutural': 'NOMINAL', 'modulos': {'suporte_vida': 'OK', 'energia': 'OK', 'comunicacao': 'OK', 'propulsao': 'OK', 'navegacao': 'OK'}}
