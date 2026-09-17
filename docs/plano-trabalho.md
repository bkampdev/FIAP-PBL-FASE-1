# Mapa de requisitos e conferência final

Base auditada: `fc90d6f`, seguida das correções desta branch. A conferência foi
executada pelo Codex a pedido de Guilherme; isso não atribui revisão ou autoria
a colegas que não participaram desta sessão.

| Requisito / issue | Arquivos e evidência | Resultado técnico |
| --- | --- | --- |
| Organização #1 | README, este mapa, contratos em docs/telemetria.md | presente |
| Telemetria #2 / validação #14 | dados/*.json, src/validacao.py, testes de limites/tipos | aprovado |
| Algoritmo #3 | src/verificacao.py, docs/algoritmo.md, pseudocódigo | aprovado; percursos nominal e múltiplas falhas |
| Python #4 | src/missao.py, notebook executado | aprovado |
| Testes #5 | tests/, docs/testes.md | 52 testes, zero falhas |
| Energia #6 | src/energia.py, docs/energia.md | 56 kWh / 5,6 h nominal; -4 kWh aborta |
| Análise por IA #7 | docs/analise-ia.md, PDF seção 6 | prompt, resposta e comparação registrados |
| Reflexão #8 | docs/reflexao_critica.md, PDF seção 7 | três eixos presentes |
| README #9 | README.md | explicação, equipe, execução e três imagens |
| Apresentação #10 | src/apresentacao.py, notebook, evidencias/ | integrada e testada |
| PDF #11 | relatorio/, scripts/gerar_relatorio.py | seis itens e exemplo executável corrigido |
| Geração opcional #13 | src/geracao.py, tests/test_geracao.py, notebook | adaptador validado sem fallback fixo |
| Revisão #15 | docs/revisao-final.md e esta conferência | revisão anterior preservada; reteste após alterações |
| Entrega #12 | docs/entrega.md | depende da confirmação no FIAP ON |

## Limites da conferência

As issues contêm critérios de processo (explicação oral do autor, revisão por
pessoa específica, aviso aos colegas). Testes automáticos não comprovam esses
atos. Os PRs documentam integração; nenhuma confirmação humana foi inventada.
A revisão final anterior declara seu executor real como Codex, não Gabriel.

A geração experimental não equivale a uma API de LLM: o modelo é GaussianMixture.
A amostra bruta permanece experimental; `gerar_cenario` adapta o contrato e
preserva as amostras aleatórias, sem substituir dados inseguros. A análise por IA obrigatória é independente desse gerador.

## Sequência reproduzível

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/pre_decolagem.ipynb
python scripts/gerar_evidencias.py
python scripts/gerar_relatorio.py
```

Nenhum envio ao FIAP ON é comprovado por este documento.
