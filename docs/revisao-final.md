# Revisão independente de integração e usabilidade

## Conclusão

**APTA PARA SUBMISSÃO NO FIAP ON.**

A versão final foi executada em cópia limpa, os artefatos foram comparados
com as entradas e ficaram publicamente acessíveis após o merge. Não foram
encontrados bloqueadores no código, notebook, README, evidências ou PDF.

Esta conclusão encerra a revisão técnica da issue #15, mas não equivale ao
envio da atividade. A issue #12 continua responsável pela submissão e pela
confirmação do status no portal.

## Responsabilidade e transparência

A revisão estava originalmente atribuída a Gabriel. A execução final descrita
neste documento foi realizada pelo Codex, como revisor técnico independente,
sob coordenação e autorização de Guilherme. Nenhuma ação ou confirmação é
atribuída falsamente a Gabriel.

## Versão avaliada

| Campo | Valor |
| --- | --- |
| Commit da branch candidata | `43529ea` |
| Commit de merge na `main` | `9c3205f82d9bbc468cd8f202119ff408cf8b24bd` |
| Equivalência | os dois commits possuem a mesma árvore Git (`5c9daeb3`) |
| Data da revisão | 16/09/2026 |
| Ambiente limpo | arquivo criado por `git archive`, venv nova e Python 3.14.7 |
| Instalação | `python -m pip install -r requirements.txt` |

## Procedimento reproduzido

A revisão partiu de uma árvore exportada do commit candidato, sem arquivos
não versionados. Em seguida, foi criado um ambiente virtual novo e executado:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/pre_decolagem.ipynb
python scripts/gerar_evidencias.py
python scripts/gerar_relatorio.py
```

Resultados:

- **48 testes aprovados, 0 falhas**;
- notebook executado integralmente, sem outputs de erro;
- três imagens regeneradas em PNG 1600 x 900;
- PDF regenerado com 13 páginas;
- link `https://github.com/bkampdev/FIAP-PBL-FASE-1` clicável nas páginas 1, 2 e 13;
- CodeQL aprovado na PR #29.

## Resultados reproduzidos

| Cenário | Entrada determinante | Decisão | Saldo | Autonomia |
| --- | --- | --- | ---: | ---: |
| `nominal.json` | temperatura interna 22 °C; pressão 100 kPa | `PRONTO PARA DECOLAR` | 56 kWh | 5,6 h |
| `falha_temperatura.json` | temperatura interna 31 °C | `DECOLAGEM ABORTADA` | 56 kWh | 5,6 h |
| `falha_energia.json` | consumo de decolagem 80 kWh | `DECOLAGEM ABORTADA` | -4 kWh | não calculada |
| `entrada_invalida.json` | pressão do tanque ausente | `DECOLAGEM ABORTADA` | indisponível | indisponível |

## Rastreabilidade de um cenário

O cenário `falha_temperatura.json` foi acompanhado de ponta a ponta:

1. o JSON altera somente a temperatura interna para 31 °C;
2. o validador preserva o dado como estruturalmente válido;
3. o módulo energético calcula saldo de 56 kWh e autonomia de 5,6 h;
4. o verificador compara 31 °C com o máximo didático de 30 °C;
5. a apresentação mostra `DECOLAGEM ABORTADA` e o motivo da temperatura;
6. o notebook, `evidencias/02-aborto.png` e o PDF exibem os mesmos valores.

Não foi observada divergência entre JSON, cálculo, decisão, imagem e PDF.

## Verificação dos entregáveis

| Requisito | Resultado da revisão |
| --- | --- |
| 1.1 Telemetria | campos, unidades, domínios, faixas e cenários documentados |
| 1.2 Algoritmo | pseudocódigo, regras, fronteiras e decisões presentes |
| 1.3 Python | leitura, validação, energia, decisão e apresentação integradas |
| 1.4 Energia | fórmulas, substituição numérica, saldo e autonomia coerentes |
| 1.5 IA | prompt, resposta, anomalias, riscos e revisão humana registrados |
| 1.6 Reflexão | ética, impacto social e sustentabilidade contemplados |
| README | explicação, execução, equipe, arquitetura, prints e links |
| Notebook | versionado, executado e sem dependência de API key |
| PDF | 13 páginas, legível, com os seis tópicos e GitHub clicável |

## Acesso público após o merge

Foram consultados sem autenticação os arquivos na branch `main`:

- README: HTTP 200;
- notebook: HTTP 200;
- PDF: HTTP 200;
- três PNGs de evidência: HTTP 200.

## Achados da revisão e resolução

1. A URL do GitHub existia no PDF, mas foi promovida para a capa com texto completo e link clicável.
2. O exemplo energético divergente foi alinhado para perdas de 5%, saldo de 56 kWh e autonomia de 5,6 h.
3. A reflexão foi alinhada ao cenário versionado `falha_energia.json`.
4. `Pillow` e `reportlab`, responsáveis pelos artefatos, tiveram versões fixadas no `requirements.txt`.
5. A documentação passou a distinguir a versão textual editável da fonte executável que produz o PDF.
6. O rascunho duplicado `analise-ia_1.md` foi removido.

## Handoff para a entrega

O repositório está tecnicamente apto. Para concluir a atividade acadêmica,
Guilherme deve anexar `relatorio/relatorio-pre-decolagem.pdf`, informar o link
público do repositório e confirmar que o FIAP ON deixou de mostrar “Entrega
pendente”. O comprovante deve permanecer privado.
