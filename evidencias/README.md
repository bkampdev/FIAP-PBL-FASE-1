# Capturas reais de execução no VS Code

Estas quatro imagens foram capturadas diretamente da janela do Visual Studio
Code pelo Computer Use. Não foram redesenhadas, recortadas ou alteradas.
A base do código é `777c27f`, com a remoção local de Grupo 16 do relatório.
O manifesto `capturas-vscode.json` registra hashes SHA-256 dos arquivos originais.

| Arquivo | Execução visível |
| --- | --- |
| 01-nominal.png | célula [16], PRONTO PARA DECOLAR, saldo 56 kWh e autonomia 5,6 h |
| 02-aborto.png | célula [17], 31 °C, DECOLAGEM ABORTADA |
| 03-energia.png | célula [18], saldo -4 kWh, DECOLAGEM ABORTADA |
| 04-testes.png | terminal integrado, 52 testes, OK |

## Como reproduzir

1. Abra a raiz do projeto no VS Code e o notebook pre_decolagem.ipynb.
2. Selecione o kernel `.venv/bin/python` e clique em Run All.
3. Aguarde o fim, salve o notebook e capture a janela nos três cenários.
4. No terminal integrado execute `.venv/bin/python -m unittest discover -s tests -v`.
5. Capture o resumo final dos testes, preservando a interface e os resultados.
6. Salve as capturas com os nomes acima e execute `python scripts/gerar_relatorio.py`.

O zoom foi ampliado para legibilidade durante as capturas e restaurado depois.
`gerar_evidencias.py` produz apenas representações opcionais dos outputs em
`evidencias/diagramadas/`; elas não substituem estes prints nem entram no PDF.
