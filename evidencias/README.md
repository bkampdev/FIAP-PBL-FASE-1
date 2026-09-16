# Evidências de execução

As três imagens desta pasta são representações legíveis das **saídas reais**
persistidas em `notebooks/pre_decolagem.ipynb`. O notebook foi reiniciado e
executado integralmente em 16/09/2026 sobre a base `a487de4` e as alterações
desta PR. O script `scripts/gerar_evidencias.py` extrai o texto das células e o
diagrama em PNG; ele não inventa valores nem altera decisões.

| Imagem | Entrada | Evidência |
| --- | --- | --- |
| `01-nominal.png` | `dados/nominal.json` | sensores dentro das faixas, saldo de 56 kWh, autonomia de 5,6 h e `PRONTO PARA DECOLAR` |
| `02-aborto.png` | `dados/falha_temperatura.json` | temperatura interna de 31 °C, acima do máximo de 30 °C, e `DECOLAGEM ABORTADA` |
| `03-energia.png` | `dados/falha_energia.json` | saldo de -4 kWh, autonomia não calculada e `DECOLAGEM ABORTADA` |

## Como reproduzir

Na raiz do repositório, após instalar `requirements.txt`:

```sh
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/pre_decolagem.ipynb
python scripts/gerar_evidencias.py
```

Depois, abra as imagens em tamanho natural e compare os valores com as saídas
do notebook. Nenhuma imagem contém credenciais, e-mails ou dados pessoais.
