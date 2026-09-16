"""Gera as imagens de evidência a partir das saídas persistidas no notebook.

As imagens não simulam uma interface: o texto é extraído diretamente dos
outputs do notebook executado e apenas diagramado para leitura no README/PDF.
"""

from pathlib import Path
import textwrap

import nbformat
from PIL import Image, ImageDraw, ImageFont


RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ / "notebooks" / "pre_decolagem.ipynb"
DESTINO = RAIZ / "evidencias"

LARGURA, ALTURA = 1600, 900
FUNDO = "#0B1020"
PAINEL = "#121A31"
BORDA = "#2B3B64"
TEXTO = "#EDF2FF"
SUAVE = "#AAB7D4"
ROXO = "#8B5CF6"
VERDE = "#34D399"
VERMELHO = "#FB7185"


def fonte(tamanho: int, negrito: bool = False):
    candidatos = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if negrito else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if negrito else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for caminho in candidatos:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    return ImageFont.load_default()


def saidas_do_notebook() -> dict[str, str]:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    saidas = {}
    for celula in notebook.cells:
        if celula.cell_type != "code":
            continue
        texto = "".join(
            output.get("text", "")
            for output in celula.get("outputs", [])
            if output.get("output_type") == "stream"
        ).strip()
        if texto.startswith("Entrada: nominal.json"):
            saidas["nominal"] = texto
        elif texto.startswith("Entrada: falha_temperatura.json"):
            saidas["aborto"] = texto
        elif texto.startswith("Entrada: falha_energia.json"):
            saidas["energia"] = texto
    ausentes = {"nominal", "aborto", "energia"} - saidas.keys()
    if ausentes:
        raise RuntimeError(f"Saídas ausentes no notebook executado: {sorted(ausentes)}")
    return saidas


def quebrar_linha(linha: str, limite: int = 92) -> list[str]:
    if len(linha) <= limite:
        return [linha]
    prefixo = "  " if linha.startswith("-") else ""
    return textwrap.wrap(linha, width=limite, subsequent_indent=prefixo)


def gerar_imagem(nome: str, titulo: str, subtitulo: str, texto: str, destaque: str):
    imagem = Image.new("RGB", (LARGURA, ALTURA), FUNDO)
    desenho = ImageDraw.Draw(imagem)

    desenho.rounded_rectangle((70, 55, 1530, 845), radius=28, fill=PAINEL, outline=BORDA, width=2)
    desenho.rounded_rectangle((105, 92, 485, 142), radius=18, fill="#1C2745")
    desenho.text((130, 103), "EXECUÇÃO REAL · JUPYTER", font=fonte(22, True), fill=ROXO)
    desenho.text((105, 178), titulo, font=fonte(46, True), fill=TEXTO)
    desenho.text((105, 240), subtitulo, font=fonte(25), fill=SUAVE)
    desenho.line((105, 292, 1495, 292), fill=BORDA, width=2)

    y = 330
    for linha_original in texto.splitlines():
        for linha in quebrar_linha(linha_original):
            cor = TEXTO
            negrito = False
            if linha.startswith("Decisão:"):
                cor = destaque
                negrito = True
            elif linha.startswith("Motivos:") or linha.startswith("Nenhuma falha"):
                cor = destaque
                negrito = True
            elif linha.startswith("Entrada:") or linha.startswith("Cenário:"):
                cor = "#93C5FD"
                negrito = True
            desenho.text((120, y), linha, font=fonte(22, negrito), fill=cor)
            y += 30

    desenho.text(
        (105, 818),
        "Fonte: notebooks/pre_decolagem.ipynb · execução integral em 16/09/2026 · base a487de4",
        font=fonte(18),
        fill=SUAVE,
    )
    imagem.save(DESTINO / nome, optimize=True)


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    saidas = saidas_do_notebook()
    gerar_imagem(
        "01-nominal.png",
        "Cenário nominal",
        "Telemetria segura, energia viável e decisão positiva",
        saidas["nominal"],
        VERDE,
    )
    gerar_imagem(
        "02-aborto.png",
        "Aborto por temperatura",
        "A falha operacional é preservada e explicada pelo verificador",
        saidas["aborto"],
        VERMELHO,
    )
    gerar_imagem(
        "03-energia.png",
        "Aborto por energia",
        "Saldo negativo impede a decolagem e a autonomia não é calculada",
        saidas["energia"],
        VERMELHO,
    )
    print("Evidências geradas a partir dos outputs persistidos do notebook.")


if __name__ == "__main__":
    main()
