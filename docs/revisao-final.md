# Revisão técnica da versão candidata

## Identificação

| Campo | Valor |
| --- | --- |
| Base integrada | `a487de440d1fd0851113ebd7a585fc0522174b86` |
| Branch candidata | `entrega-final-master` |
| Data | 16/09/2026 |
| Execução técnica | Guilherme, durante a consolidação da entrega |
| Revisão independente final | pendente de confirmação por Gabriel (#15) |
| Ambiente | macOS, Python 3.14.7 e dependências de `requirements.txt` |

Esta revisão técnica não equivale ao envio no FIAP ON nem substitui a
confirmação independente de Gabriel.

## Execução reproduzida

```sh
python -m unittest discover -s tests -v
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/pre_decolagem.ipynb
```

Resultado: **48 testes aprovados, 0 falhas**. O notebook foi executado do
início ao fim e teve as saídas persistidas.

| Cenário | Entrada observada | Decisão | Saldo | Autonomia |
| --- | --- | --- | ---: | ---: |
| nominal | temperatura interna 22 °C; pressão 100 kPa | PRONTO PARA DECOLAR | 56 kWh | 5,6 h |
| temperatura | temperatura interna 31 °C | DECOLAGEM ABORTADA | 56 kWh | 5,6 h |
| energia | consumo de decolagem 80 kWh | DECOLAGEM ABORTADA | -4 kWh | não calculada |
| entrada inválida | pressão ausente | DECOLAGEM ABORTADA | indisponível | indisponível |

## Rastreabilidade

O caso `falha_temperatura.json` foi acompanhado do JSON até a apresentação:

1. o JSON altera somente a temperatura interna para 31 °C;
2. o validador mantém o dado como operacionalmente válido;
3. o cálculo energético preserva saldo de 56 kWh;
4. o verificador compara 31 °C com o máximo didático de 30 °C;
5. o notebook apresenta `DECOLAGEM ABORTADA` e o motivo correspondente;
6. `evidencias/02-aborto.png` e o PDF exibem os mesmos valores.

Não foi observada divergência entre entrada, cálculo, decisão, imagem e
relatório.

## Artefatos finais conferidos

- `README.md`: explicação, equipe, execução, arquitetura, prints e links.
- `notebooks/pre_decolagem.ipynb`: executado e com quatro demonstrações.
- `evidencias/01-nominal.png`: saída nominal legível.
- `evidencias/02-aborto.png`: aborto por temperatura legível.
- `evidencias/03-energia.png`: aborto energético legível.
- `relatorio/relatorio-pre-decolagem.md`: versão textual editável.
- `scripts/gerar_relatorio.py`: fonte executável da diagramação do PDF.
- `relatorio/relatorio-pre-decolagem.pdf`: 13 páginas revisadas visualmente,
  com os seis tópicos, código, fórmulas, imagens, integrantes e links.
- `docs/entrega.md`: separa conferência local de submissão no portal.

## Correções feitas durante a consolidação

1. O exemplo em `docs/energia.md` usava perdas de 10% e saldo de 52 kWh,
   diferente do cenário versionado. Foi alinhado para 5%, saldo de 56 kWh e
   autonomia de 5,6 h.
2. A reflexão citava um cenário inexistente de 45% de energia. Foi alinhada ao
   `falha_energia.json`, que produz saldo de -4 kWh.
3. O README ainda apresentava tarefas concluídas como planejamento e dizia que
   parte da equipe estava pendente. Foi atualizado com o estado confirmado no
   FIAP ON em 16/09/2026.
4. O rascunho duplicado `analise-ia_1.md` foi removido; a versão canônica
   permanece em `docs/analise-ia.md`.

## Conclusão

**Versão tecnicamente pronta para revisão independente e submissão.** Não há
bloqueador conhecido no código, notebook, README, evidências ou PDF. Antes do
envio, Gabriel deve confirmar os artefatos finais e Guilherme deve realizar a
conferência pública e a submissão descritas em `docs/entrega.md`.
