# Informações no site:

## ATIVIDADE INTEGRADORA – RELATÓRIO OPERACIONAL DE PRÉ-DECOLAGEM


## Introdução

**1.1 Organização e descrição da telemetria**
Interpretar dados referentes a:
-   Temperatura interna e externa;
-   Integridade estrutural (0/1);
-   Níveis de energia (%);
-   Pressão dos tanques;
-   Status dos módulos críticos.

**1.2 Algoritmo de verificação**
Construir um algoritmo (fluxograma/pseudocódigo) capaz de decidir: “PRONTO PARA DECOLAR” ou “DECOLAGEM ABORTADA” com base em faixas seguras predefinidas.

**1.3 Script em Python**
Implementar a lógica do algoritmo em Python, simulando:
-   Leitura dos dados;
-   Execução das verificações;
-   Resultado final impresso.

**1.4 Análise energética**
Calcular autonomia inicial considerando:
-   Capacidade total (kwh);
-   Carga atual (%);
-   Consumo estimado na decolagem;
-   Perdas energéticas.

**1.5 Análise assistida por IA**
Solicitar à IA:
-   Classificação dos dados;
-   Identificação de possíveis anomalias;
-   Sugestões de risco.

**1.6 Reflexão crítica**
Texto sobre:
-   Ética e responsabilidade;
-   Impacto social da exploração espacial;
-   Sustentabilidade tecnológica.

## 2 ENTREGÁVEIS

**Em relação aos entregáveis, é necessário:**

-   Um relatório em PDF contendo todos os dados pedidos na atividade integradora (códigos, análises, algoritmos etc.);
-   Link do repositório  **público**  no GitHub contendo:
    -   Notebook Python (.ipynb);
-   Arquivo README.md contendo:
    -   Explicação do projeto;
    -   Prints da execução;
    -   Instruções de execução do código.

**3 Critérios de avaliação (10 pontos totais)**
|Criterio|Pontos  |
|--|--|
|Organização da telemetria e clareza na apresentação dos dados| 2 |
|Algoritmo de verificação bem estruturado (fluxograma ou pseudocódigo)|2|
|Script Python funcional realizando todas as verificações da missão|2|
|Análise energética correta com cálculos apresentados|2|
|Documentação clara no PDF + repositório GitHub público com README completo|2|
|||
|TOTAL|10|

## Membros do grupo:
Davi: rm572772
Guilherme: rm574229
Lorenzo: rm575361
Gabriel: rm574746

## Organização do trabalho — equipe de 5

Planejamento revisado em **09/09/2026** a partir do capítulo 1 (páginas 13–15) e do [enunciado no FIAP ON](https://on.fiap.com.br/mod/assign/view.php?id=616742). Este é um plano de execução: as tarefas abaixo não estão sendo declaradas concluídas.

Eduardo Backes Klauck (@BackesEdu) integra a divisão de trabalho como quinto membro; seu RM deve ser confirmado pelo próprio integrante. O convite de acesso ao GitHub ainda estava pendente na revisão.

| Integrante | Responsabilidades | Issues detalhadas |
| --- | --- | --- |
| Guilherme — @bkampdev | Estrutura e contratos; integração do notebook; regularização da equipe e entrega | [#1](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/1), [#4](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/4), [#12](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/12) |
| Davi — @daviconinck | Dicionário e cenários de telemetria; validação dos dados; testes das regras | [#2](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/2), [#14](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/14), [#5](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/5) |
| Lorenzo — @Rocha0306 | Algoritmo de decisão; cálculos energéticos; geração de dados com IA | [#3](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/3), [#6](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/6), [#13](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/13) |
| Gabriel — @ItsTheContext | Análise assistida por IA; prints/evidências; revisão independente da entrega | [#7](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/7), [#10](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/10), [#15](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/15) |
| Eduardo — @BackesEdu | Reflexão crítica; documentação do README; consolidação do relatório PDF | [#8](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/8), [#9](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/9), [#11](https://github.com/bkampdev/FIAP-PBL-FASE-1/issues/11) |

Cada issue contém objetivo, pré-requisitos, arquivos sugeridos, passo a passo, exemplo, critérios de aceite e orientação de entrega ao próximo responsável. São três tarefas por integrante, com estimativas ajustáveis; cada autor deve produzir sua parte e ajudar quem integra o resultado.

**Atribuição pendente:** as issues #8, #9 e #11 são de Eduardo no planejamento. O campo Assignees será preenchido após o aceite do convite, conforme checklist de #12. O nome no texto não equivale a uma atribuição formal do GitHub.

### Sequência e metas internas

| Meta sugerida | Resultado esperado |
| --- | --- |
| 10/09 | Contratos, dicionário dos dados e cenários definidos (#1, #2) |
| 11/09 | Algoritmo, energia e validação prontos para integrar (#3, #6, #14) |
| 12/09 | Notebook funcionando e extensão de geração integrada se disponível (#4, #13) |
| 13/09 | Testes, análise por IA e reflexão revisados (#5, #7, #8) |
| 14/09 | README e evidências de execução (#9, #10) |
| 15/09 | PDF, revisão independente e conferência/envio com margem (#11, #15, #12) |

Essas metas são propostas do grupo, não prazos adicionais da FIAP. **Prazo oficial exibido no portal: 16/09/2026 às 23h59.** Em 09/09 a atividade estava com entrega pendente.

### Como usar o Project

O acompanhamento fica no [Roadmap PBL](https://github.com/users/bkampdev/projects/5). Fluxo: **Backlog → Ready → In progress → In review → Done**. Mover para In progress quando começar; pedir revisão de outro integrante antes de concluir; comentar bloqueios na issue mencionando a dependência. Evitar editar o mesmo notebook simultaneamente: combinar alterações por branch/PR com Guilherme.

### Cuidados para a entrega

- O núcleo obrigatório é: telemetria, algoritmo, Python, energia, análise assistida por IA e reflexão; PDF com o conteúdo pedido; repositório público com notebook `.ipynb`; README com explicação, prints e execução.
- A geração de dados por IA (#13) é uma extensão solicitada pelo grupo e permanece com Lorenzo. Não substitui a análise assistida por IA de #7. Manter execução local sem credenciais para o núcleo obrigatório.
- Dados e faixas de segurança são hipóteses didáticas, não parâmetros certificados de uma nave real. A IA não substitui as verificações determinísticas nem a revisão humana.
- Na consulta de 09/09, o grupo da atividade no FIAP ON mostrava apenas Guilherme e Davi. Confirmar e regularizar os cinco integrantes antes da entrega (#12); participar do GitHub não inclui automaticamente alguém no grupo da FIAP.
- O capítulo local menciona 15 pontos, enquanto o portal atual e o enunciado acima indicam 10. Os entregáveis centrais coincidem; usar o portal como referência atual e esclarecer a divergência com a tutoria se necessário.
- Não publicar o PDF didático exclusivo do aluno, senhas ou API keys. O PDF a entregar é o relatório produzido pelo grupo.

As instruções finais de execução, prints e link do relatório serão acrescentados em #9 após os artefatos existirem e serem testados. Não considerar a atividade enviada até o portal confirmar o envio (#12).
