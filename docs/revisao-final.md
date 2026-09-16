# Revisão independente de integração e usabilidade

## Identificação da versão avaliada

| Campo | Valor |
| --- | --- |
| Commit avaliado | `89a0fbd542aee0e1d9c250fbdf6bea5e7cc2feeb` |
| Branch/PR | `15-revisar-independentemente-execução-documentação-e-consistência-da-entrega` / PR #26 |
| Data da revisão | 16/09/2026 |
| Revisor | Gabriel (@ItsTheContext) |
| Ambiente | macOS, Python 3.14.7 global; `requirements.txt` declara `numpy` e `scikit-learn` |
| Cópia limpa | clone local em diretório temporário independente |

Esta revisão confere a versão integrada com a `main` atual. Ela não equivale ao
envio da atividade no FIAP ON.

## Preparação e execução

A cópia limpa foi obtida e a suíte foi executada com:

```sh
python3 -m unittest discover -s tests -v
```

Resultado: **40 testes executados, 40 aprovados, 0 falhas**.

O README ainda não tem instruções de instalação/execução, portanto não foi
possível preparar o ambiente seguindo apenas esse arquivo, como pede a issue.
Também não há Jupyter instalado nem declarado em `requirements.txt`. Para
validar a lógica do notebook sem alegar uma execução por kernel Jupyter, as
células de código foram executadas em ordem com Python 3.14.7 na cópia limpa.
Essa limitação é registrada como bloqueio abaixo.

## Resultados reproduzidos do notebook

| Cenário | Decisão observada | Saldo | Autonomia | Motivo observado |
| --- | --- | ---: | ---: | --- |
| `dados/nominal.json` | `PRONTO PARA DECOLAR` | 56,0 kWh | 5,6 h | nenhum |
| `dados/falha_modulo.json` | `DECOLAGEM ABORTADA` | 56,0 kWh | 5,6 h | `Modulo critico em falha: propulsao` |
| `dados/falha_energia.json` | `DECOLAGEM ABORTADA` | -4,0 kWh | `None` | `Energia insuficiente: saldo de -4.0 kWh` |

O notebook usa os limites atuais de `src.missao.LIMITES_PADRAO`: energia de
50–100% e pressão de 90–110 kPa. A divergência de limites apontada no rascunho
anterior foi corrigida na `main` e **não é um bloqueio nesta versão**.

## Rastreabilidade de um caso

O caso rastreado foi `dados/falha_modulo.json`.

| Etapa | Evidência | Resultado |
| --- | --- | --- |
| JSON | `modulos.propulsao` é `FALHA`; os demais módulos são `OK` | entrada consistente |
| Energia | 100 kWh × 80%; perdas de 5%; consumo de 20 kWh | saldo de 56,0 kWh; autonomia de 5,6 h |
| Decisão | `executar_cenario()` | `DECOLAGEM ABORTADA` por falha de propulsão |
| Notebook | célula de cenário de falha operacional | mesmo resultado impresso |
| Prints e PDF | não existem artefatos versionados | não verificável, bloqueio |

`energia_pct` e `carga_pct` permanecem ambos em 80, portanto não há divergência
entre telemetria e cálculo energético nesse caso.

## Verificação de artefatos públicos

O repositório é público. Os documentos de telemetria, algoritmo, energia,
análise por IA e reflexão crítica existem no repositório. Porém, a revisão
encontrou as pendências abaixo:

- não há PDF final versionado para conferir os seis tópicos, legibilidade,
  nomes e link do repositório;
- não há imagens/prints versionados;
- o README explica o escopo, mas não contém instruções reproduzíveis de
  instalação, execução dos testes ou abertura do notebook;
- `src/apresentacao.py` não existe e o notebook declara explicitamente que
  `exibir_cenario` é temporária; logo, ainda não há prova de uso do módulo de
  apresentação da issue #10.

## Achados e reteste

| # | Problema | Como reproduzir | Esperado | Obtido | Responsável | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | README sem instruções de instalação e execução, inclusive da dependência Jupyter. | Abrir `README.md` e `requirements.txt` em clone limpo. | Preparar e abrir o notebook só pelo README. | Não há passos de execução e Jupyter não é declarado. | Eduardo (#9), com apoio de Guilherme para integração. | **Bloqueante, pendente** |
| 2 | Não há PDF final nem prints/imagens versionados. | Procurar arquivos `.pdf`, `.png`, `.jpg`, `.jpeg` e `.gif`. | Conferir os seis tópicos, legibilidade e consistência visual. | Nenhum desses arquivos está no repositório. | Eduardo (#11) e Gabriel (#10). | **Bloqueante, pendente** |
| 3 | O módulo oficial de apresentação não está integrado. | Verificar `src/apresentacao.py` e os imports do notebook. | Notebook usa a função oficial de #10. | O arquivo não existe; o notebook usa `exibir_cenario` temporária. | Gabriel (#10), integração por Guilherme (#4). | **Bloqueante, pendente** |
| 4 | Execução por kernel Jupyter não é reproduzível pelo projeto. | Seguir README e `requirements.txt` em clone limpo. | Reiniciar kernel e executar todas as células. | Jupyter não está instalado nem documentado; as células foram validadas apenas por execução sequencial em Python. | Eduardo (#9), com apoio de Guilherme. | **Bloqueante, pendente** |

Não foi encontrado bloqueio no núcleo de validação, energia ou decisão: a suíte
completa e os três cenários acima foram retestados na cópia limpa.

## Conclusão e handoff

**Bloqueado para conferência de entrega.** O núcleo Python está funcional e
reproduzível no ambiente testado, mas os quatro achados de empacotamento e
integração impedem validar a entrega completa solicitada pela FIAP. Após as
correções, o responsável deve executar o notebook por Jupyter em cópia limpa,
conferir PDF e imagens e repetir a suíte antes de mudar esta conclusão para
apta.

Esta conclusão deve ser encaminhada a Guilherme na issue #12; ela não fecha a
issue #15 nem autoriza o envio no portal.
