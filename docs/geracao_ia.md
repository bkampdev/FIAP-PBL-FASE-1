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

{'temperatura_interna_c': 20.09, 'temperatura_externa_c': -112.93, 'energia_pct': 88.9, 'pressao_tanque_kpa': 104.71, 'integridade_estrutural': 'NOMINAL', 'modulos': {'suporte_vida': 'OK', 'energia': 'OK', 'comunicacao': 'OK', 'propulsao': 'OK', 'navegacao': 'OK'}}


## Integração com a missão

Use `gerar_cenario("nominal")` para novos sorteios a cada chamada. A função
preserva os valores do modelo, converte integridade para 0/1 e acrescenta
hipóteses energéticas explícitas: capacidade 100 kWh, consumo 20 kWh, perdas
5% e potência 10 kW. A carga acompanha energia_pct. Energia insuficiente usa
consumo de 100 kWh; as outras falhas são aplicadas pelo gerador original.

Não há fallback para JSON fixo. O cenário nominal significa ausência de falha
forçada, não garantia de aprovação: a amostra pode conter pressão fora da
faixa ou módulos em falha. O fluxo da missão valida os dados e decide.
A mesma decisão em duas execuções não significa que os dados são iguais.

O notebook mostra os dados sorteados, origem e decisão. Para depuração ou
testes apenas, `gerar_cenario("nominal", seed=42)` repete a amostra.
O random_state fixo do treinamento estabiliza o ajuste do modelo; o sorteio
usa a seed recebida, que por padrão é None.

## Faixa de pressão da base sintética

A base didática foi ajustada de 414–424 kPa para aproximadamente 94–104 kPa,
compatível com os limites de 90–110 kPa definidos no projeto. Esta é uma
correção da base sintética, não uma conversão de unidades nem uma alteração
dos limites de segurança. Os sorteios continuam aleatórios e não são
recortados ou substituídos para aprovar. O cenário nominal ainda pode abortar
por falhas sorteadas nos módulos; os outros três cenários forçam falhas.
