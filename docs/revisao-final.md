# Revisão independente de integração e usabilidade

## Identificação da versão avaliada

| Campo | Valor |
| --- | --- |
| Código avaliado | `a487de440d1fd0851113ebd7a585fc0522174b86` (merge da PR #27) |
| Branch da revisão | `15-revisar-independentemente-execução-documentação-e-consistência-da-entrega` / PR #26 |
| Data da atualização técnica | 16/09/2026 |
| Responsável pela revisão independente | Gabriel (@ItsTheContext) |
| Atualização técnica | Guilherme, com execução automatizada registrada abaixo |
| Ambiente da execução limpa | macOS, Python 3.14.7; dependências de `requirements.txt` |
| Cópia limpa | árvore temporária criada de `git archive`, sem arquivos locais do revisor |

Esta revisão não equivale ao envio da atividade no FIAP ON. A confirmação
independente de Gabriel sobre a versão e os artefatos finais continua necessária.

## Preparação e execução

O README atual permite criar `.venv`, instalar `requirements.txt`, executar a
suíte e abrir `notebooks/pre_decolagem.ipynb`. A dependência `jupyter` está
declarada em `requirements.txt`.

Na cópia limpa, foram executados:

```sh
python -m unittest discover -s tests -v
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/pre_decolagem.ipynb
```

Resultado: **48 testes executados, 48 aprovados, 0 falhas**. O notebook foi
executado do início ao fim pelo kernel Jupyter e teve as saídas persistidas.

## Resultados reproduzidos do notebook

| Cenário | Entrada observada | Decisão | Saldo | Autonomia | Motivo observado |
| --- | --- | --- | ---: | ---: | --- |
| `dados/nominal.json` | temperatura interna 22 °C; pressão 100 kPa | `PRONTO PARA DECOLAR` | 56,0 kWh | 5,6 h | nenhum |
| `dados/falha_temperatura.json` | temperatura interna 31 °C | `DECOLAGEM ABORTADA` | 56,0 kWh | 5,6 h | acima do máximo de 30 °C |
| `dados/falha_energia.json` | energia 80%; consumo de decolagem 80 kWh | `DECOLAGEM ABORTADA` | -4,0 kWh | não calculada | energia insuficiente |
| `dados/entrada_invalida.json` | pressão do tanque ausente | `DECOLAGEM ABORTADA` | indisponível | indisponível | campo obrigatório ausente |

O notebook mostra a telemetria com unidades, os módulos críticos, a decisão e
o balanço energético. Ele usa `src.missao.executar_cenario` e
`src.apresentacao.formatar_resultado`; a apresentação não recalcula a decisão
nem a energia. Os JSONs fixos mantêm a demonstração reproduzível sem API key
ou internet. A geração de dados por IA permanece uma extensão opcional e não
é acionada por este fluxo determinístico.

## Rastreabilidade de um caso

O caso rastreado foi `dados/falha_temperatura.json`:

1. O notebook mostra `temperatura_interna_c = 31 °C`, acima do limite máximo
   didático de 30 °C; pressão, energia e módulos permanecem válidos.
2. `executar_cenario()` valida a telemetria, calcula a energia e delega a
   decisão a `verificar_pre_decolagem()`.
3. A saída mostra `DECOLAGEM ABORTADA`, o motivo da temperatura e o saldo de
   56,0 kWh com autonomia de 5,6 h.

Não foi observada divergência entre o JSON, a telemetria exibida, o cálculo
energético e a decisão impressa.

## Verificação de artefatos públicos

O repositório contém notebook, README com instruções, documentação de
telemetria, algoritmo, energia, análise assistida por IA e reflexão crítica.
Também contém `src/apresentacao.py` e seus testes. A revisão encontrou duas
ausências objetivas:

- não há imagens de evidência versionadas em `evidencias/` nem prints
  incorporados ao README;
- não há PDF final nem fonte editável em `relatorio/` para conferir os seis
  tópicos, legibilidade, integrantes e link público.

## Achados e reteste

| # | Problema | Como reproduzir | Esperado | Obtido | Responsável | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Evidências visuais ausentes. | Procurar `evidencias/` e imagens no README. | Capturas legíveis de caso nominal, aborto e energia, com legenda e procedimento. | Nenhuma imagem versionada. | Gabriel (#10). | **Bloqueante para entrega, pendente** |
| 2 | PDF final e fonte editável ausentes. | Procurar `relatorio/` e arquivos `.pdf`. | Relatório com os itens exigidos, código, análises, imagens, integrantes e links. | Nenhum PDF ou fonte versionada. | Eduardo (#11). | **Bloqueante para entrega, pendente** |
| 3 | Confirmação independente sobre os artefatos finais pendente. | Após publicar imagens e PDF, Gabriel deve abrir a versão final em cópia limpa. | Reteste documentado da versão e conclusão final. | A execução técnica acima foi atualizada por Guilherme; Gabriel ainda precisa confirmar de forma independente. | Gabriel (#15). | **Pendente** |

Não há bloqueio atual no núcleo de validação, decisão, energia, apresentação,
instruções de execução ou notebook.

## Conclusão e handoff

**Núcleo técnico apto; entrega final bloqueada somente pelos artefatos acima.**
O código, a suíte e o notebook foram reexecutados em cópia limpa com sucesso.
Depois de publicar as imagens e o PDF, Gabriel deve reabrir a versão final,
conferir os artefatos e registrar a conclusão independente nesta PR ou na
Issue #15. A Issue #12 continua responsável pela conferência do grupo e pelo
envio confirmado no FIAP ON.
