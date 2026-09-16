# Revisão Final Independente — Item de Integração e Usabilidade

> ⚠️ **O QUE AINDA FALTA (remover este bloco antes da entrega final)**
>
> Nesta sessão, os módulos `src/validacao.py` (#14), `src/energia.py` (#6) e
> `src/missao.py` (#4) foram efetivamente reconstruídos e **testados de
> verdade** (13/13 testes passando, 0 falhas). Um achado real e bloqueante
> foi confirmado por execução (seção 8, item 1).
>
> Porém, isto **não é uma revisão completa** ainda:
> - `src/verificacao.py` (Lorenzo) nunca foi compartilhado por inteiro — só
>   em trechos de diff. 26 testes da suíte dependem dele e não foram
>   confirmados por execução real, só por reconstrução baseada nos testes.
> - **#9 e #11** — citados como dependências explícitas da própria #15 —
>   ainda não foram enviados. Não sabemos o que são nem se afetam a decisão.
> - O notebook integrado, o README.md e o PDF final não foram
>   compartilhados — sem eles as seções 3, 6 e 7 deste checklist não podem
>   ser marcadas.
>
> Por isso a conclusão da seção 12 permanece **bloqueada**, não "apta".

---

## 1. Identificação da versão avaliada

| Campo | Valor |
|---|---|
| Commit avaliado | `[PREENCHER: hash do commit/PR de src/missao.py — confirmar com Guilherme]` |
| Branch/PR | `[PREENCHER: PR contendo src/missao.py e tests/test_missao.py — confirmar com Guilherme]` |
| Data da revisão | `[PREENCHER: DD/MM/AAAA]` |
| Revisor | Gabriel (@ItsTheContext) |
| Python usado | `[PREENCHER: confirmar versão usada por Guilherme/Davi]` |
| Ambiente | `[PREENCHER: SO, venv/conda, dependências — README do repositório ainda vai precisar listar isso]` |
| Pasta/local de execução | Cópia limpa em pasta nova (não reaproveitar checkout de outro integrante) |

---

## 2. Preparação do ambiente (seguindo APENAS o README)

- [ ] Cópia limpa do repositório obtida em pasta nova
- [ ] Dependências instaladas seguindo só as instruções do README
- [ ] Notebook aberto com sucesso

**Passos faltantes, caminhos quebrados ou dúvidas que precisaram ser tiradas com o autor:**

`[PREENCHER: listar qualquer lacuna encontrada no README — depende de #4/README ainda não disponíveis]`

---

## 3. Execução do notebook

- [ ] Kernel reiniciado antes da execução
- [ ] Todas as células executadas em modo padrão (sem API key)
- [ ] Caso nominal testado (`dados/nominal.json` → esperado `PRONTO PARA DECOLAR`)
- [ ] Caso(s) abortado(s) testado(s) — sugestão: `falha_temperatura.json` e `falha_modulo.json`, que têm causas diferentes
- [ ] Saídas conferidas como resultado da execução atual (não valores salvos de execução anterior)

**Resultados esperados (referência, calculados a partir dos módulos reais em #6/#14):**

| Cenário | Decisão esperada | Motivo esperado |
|---|---|---|
| `nominal.json` | PRONTO PARA DECOLAR | — |
| `falha_temperatura.json` | DECOLAGEM ABORTADA | temperatura_interna_c 31 acima do maximo de 30 |
| `falha_modulo.json` | DECOLAGEM ABORTADA | Modulo critico em falha: propulsao |
| `falha_energia.json` | DECOLAGEM ABORTADA | Energia insuficiente: saldo de -4.0 kWh |

**Observações:**

`[PREENCHER]`

---

## 4. Testes automatizados (#5/#6/#14)

| Item | Resultado |
|---|---|
| Comando executado | `python -m unittest discover -s tests -v` |
| Resultado **confirmado por execução real** nesta sessão (apenas `test_energia.py` + `test_missao.py`, que têm arquivo-fonte completo disponível) | **13 testes executados, 13 aprovados, 0 falhas** |
| `test_pre_decolagem.py` e `test_verificacao.py` (26 testes, dependem de `src/verificacao.py` completo, ainda não recebido — só diffs) | **NÃO confirmado por execução real** — `src/verificacao.py` foi apenas reconstruído a partir das mensagens de erro exigidas pelos testes, não é o arquivo oficial de Lorenzo |
| Resultado obtido na cópia limpa do repositório real | `[PREENCHER: só é possível com o repositório completo/clonado, não com diffs colados]` |
| Suíte roda no pacote recebido (não só na máquina de Davi/Eduardo) | `[PREENCHER: sim/não]` |

**Log resumido:**
```
[PREENCHER: colar saída real da execução na cópia limpa]
```

---

## 5. Rastreabilidade de um caso (JSON → notebook → PDF)

> Sugestão de caso para rastrear: `falha_modulo.json` — é uma causa isolada
> e fácil de conferir ponta a ponta. `src/missao.py::executar_cenario` já tem
> um teste próprio confirmando esse resultado
> (`test_falha_operacional_preserva_motivo_do_modulo`), útil como referência
> cruzada.

| Etapa | Valor esperado (referência) | Valor observado | Consistente? |
|---|---|---|---|
| JSON de entrada (`dados/falha_modulo.json`) | `modulos.propulsao = "FALHA"`, demais OK | `[PREENCHER]` | — |
| `executar_cenario()` (#4) | `decisao="DECOLAGEM ABORTADA"`, `energia["viavel"]=True`, motivo `"Modulo critico em falha: propulsao"` | `[PREENCHER]` | `[PREENCHER]` |
| Tabela no notebook | mesmos valores do JSON | `[PREENCHER]` | `[PREENCHER]` |
| Cálculo de energia | saldo 56 kWh, autonomia 5,6h (energia não é a causa do aborto aqui) | `[PREENCHER]` | `[PREENCHER]` |
| Decisão final exibida | `DECOLAGEM ABORTADA` — "Modulo critico em falha: propulsao" | `[PREENCHER]` | `[PREENCHER]` |
| Print/evidência (#10) | mesmo texto e valores | `[PREENCHER]` | `[PREENCHER]` |
| PDF final | mesmo texto e valores | `[PREENCHER]` | `[PREENCHER]` |

**Atenção:** ao rodar `executar_cenario`, confirmar qual dicionário de
limites está sendo passado. Se for `LIMITES_PADRAO` (definido em
`src/missao.py`), veja o achado #1 na seção 8 — os limites padrão de
`energia_pct` e `pressao_tanque_kpa` não correspondem às faixas acordadas
em #2, o que pode aprovar cenários que deveriam ser abortados.

**Divergências encontradas (mesmo que a decisão final seja igual):**

`[PREENCHER]`

**Atenção especial (regra de #6/#14):** `energia_pct` (telemetria) e `carga_pct`
(cálculo energético) precisam ser iguais — se algum cenário do notebook usar
valores diferentes para os dois, isso é erro de entrada, não um caso válido.
Conferir isso ao rastrear.

---

## 6. Verificação do PDF final

- [ ] Item 1.1 presente (organização/descrição da telemetria)
- [ ] Item 1.2 presente (algoritmo — fluxograma/pseudocódigo)
- [ ] Item 1.3 presente (script Python)
- [ ] Item 1.4 presente (análise energética — conferir fórmulas batem com `src/energia.py`)
- [ ] Item 1.5 presente (análise assistida por IA — ver `docs/analise-ia.md`)
- [ ] Item 1.6 presente (reflexão crítica)
- [ ] Código/algoritmo legível (não cortado, fonte adequada)
- [ ] Link do repositório GitHub presente e correto
- [ ] Nomes dos integrantes conferem com o README (nenhum dado inventado)

**Observações:**

`[PREENCHER]`

---

## 7. Verificação do GitHub (README e acesso público)

- [ ] Repositório é público
- [ ] README explica o projeto
- [ ] README contém prints da execução
- [ ] README contém instruções de execução do código
- [ ] Nenhuma instrução exige conta/API paga para rodar o núcleo obrigatório
- [ ] Imagens (`evidencias/`) abrem corretamente no GitHub

**Observações:**

`[PREENCHER]`

---

## 8. Tabela de achados

| # | Problema | Como reproduzir | Esperado | Obtido | Responsável | Estado |
|---|---|---|---|---|---|---|
| 1 | `LIMITES_PADRAO` em `src/missao.py` usa `energia_pct: (20, 100)` e `pressao_tanque_kpa: (1, 1000)`, divergindo das faixas seguras acordadas em `docs/telemetria.md` (#2): `energia_pct: 50-100` e `pressao_tanque_kpa: 90-110`. **Reproduzido de fato nesta sessão** (ver comando abaixo). | `executar_cenario({..., "energia_pct": 30, "carga_pct": 30, ...}, LIMITES_PADRAO)` | `DECOLAGEM ABORTADA` (fora da faixa segura de #2) | `PRONTO PARA DECOLAR` — confirmado por execução real: `energia_pct=30` foi aprovado | Guilherme (#4, `src/missao.py`) | **Bloqueante, confirmado** — aprova cenários operacionalmente inseguros por padrão |
| 2 | `src/verificacao.py` (autoria de Lorenzo) nunca foi compartilhado por completo nesta revisão — só como trechos de diff. 26 dos 39 testes da suíte dependem dele e não puderam ser executados de verdade; foram apenas inferidos por reconstrução. | Solicitar o arquivo completo (ou acesso ao repositório) e rodar `python -m unittest discover -s tests -v` numa cópia limpa. | Suíte completa executando e confirmando os 39 testes | Só 13/39 confirmados por execução real nesta sessão | Lorenzo (arquivo) / Gabriel (execução final) | **Bloqueante para fechar a #15** — falta evidência real, não just diff |
| 3 | `[PREENCHER: outros achados após obter #9, #11, notebook, README e PDF reais]` | `[PREENCHER]` | `[PREENCHER]` | `[PREENCHER]` | `[PREENCHER]` | `[PREENCHER]` |

> **Nota:** o achado #1 já havia sido sinalizado por um bot de revisão
> automática (chatgpt-codex-connector) no PR de #4, mas segue sem correção
> até o momento desta revisão. Um segundo apontamento do mesmo bot — risco
> de `KeyError` quando faltam campos de energia — **já está corrigido** no
> código atual: há checagem explícita de `campos_energia_ausentes` antes do
> cálculo, confirmada pelo teste
> `test_cenario_sem_campos_de_energia_aborta_sem_lancar_key_error`. Não
> precisa reabrir esse segundo ponto.

> **Critério de bloqueio:** problemas que impedem execução, alteram resultado
> ou omitem requisito → **bloqueiam a entrega**. Detalhes cosméticos devem ser
> listados separadamente e não bloqueiam.

---

## 9. Revisão independente do módulo de apresentação (#10, autoria de Gabriel)

> Gabriel é autor de #10 e não pode ser o único aprovador dessa parte.

| Revisor | Escopo |
|---|---|
| Davi | `src/apresentacao.py` e seus testes |
| Guilherme | Integração visual no notebook |
| Gabriel | Módulos dos colegas e fluxo geral de execução (não a própria parte) |

**Status da revisão cruzada de #10:** `[PREENCHER: aprovado / pendências]`

---

## 10. Verificação de uso efetivo dos módulos

> Um arquivo nunca importado não demonstra participação funcional.

| Integrante | Módulo | Importado/usado no notebook? | PR/arquivo examinado |
|---|---|---|---|
| Gabriel | `src/apresentacao.py` | `[PREENCHER]` | `[link do PR]` |
| Guilherme | `src/missao.py` (orquestrador, #4) + integração no notebook | `[PREENCHER]` | `[link do PR]` |
| Davi | `src/validacao.py`, matriz de testes (#5/#14) | `[PREENCHER]` | `[link do PR]` |
| Lorenzo | `src/verificacao.py` (decisão) | `[PREENCHER]` | `[link do PR]` |
| Eduardo | `src/energia.py` (#6) | `[PREENCHER]` | `[link do PR]` |

---

## 11. Correções solicitadas

| Solicitado a | Item | Retestado? | Resultado do reteste |
|---|---|---|---|
| `[PREENCHER]` | `[PREENCHER]` | `[sim/não]` | `[PREENCHER]` |

---

## 12. Conclusão

- [ ] **Apto para conferência de entrega** (encaminhar a Guilherme em #12)
- [x] **Bloqueado** pelos itens listados na seção 8

**Justificativa final:**

Bloqueado por dois motivos confirmados nesta sessão: (1) achado real e
reproduzido — `LIMITES_PADRAO` em `src/missao.py` aprova cenários fora das
faixas seguras acordadas em #2; (2) falta de evidência real de execução para
26 dos 39 testes da suíte, por ausência do arquivo completo
`src/verificacao.py`. Além disso, #9, #11, o notebook integrado, o README e
o PDF final ainda não foram disponibilizados — sem eles, esta revisão não
pode ser considerada completa nem o status pode ser marcado como concluído.

> ⚠️ Esta revisão não equivale ao envio no portal FIAP ON. O envio final é
> responsabilidade de Guilherme via #12.
