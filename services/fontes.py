# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : fontes.py
Autor      : Emerson
Data       : Sun Jul 26 17:29:57 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Serviço criado para resolver o problema com as fontes do app quando este esta online,
agora posso carregar a minhas próprias fontes e não ficar dependente das fontes instaladas no sevidor
      
Histórico:
       26/07/20226 - Inicio 
===============================================================================
"""
from pathlib import Path
from PIL import ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FONTS_DIR = PROJECT_ROOT / "assets" / "fonts"

FONT_REGULAR = FONTS_DIR / "NotoSans-Regular.ttf"
FONT_BOLD = FONTS_DIR / "NotoSans-Bold.ttf"

FONT_SYMBOL_REGULAR = FONTS_DIR / "DejaVuSans.ttf"
FONT_SYMBOL_BOLD = FONTS_DIR / "DejaVuSans-Bold.ttf"

FONT_SYMBOL_EMOJI = FONTS_DIR / "NotoEmoji-Regular.ttf"


def fonte_regular(tamanho: int):
    return ImageFont.truetype(str(FONTS_DIR / "NotoSans-Regular.ttf"),tamanho)

def fonte_bold(tamanho: int):
    return ImageFont.truetype(str(FONTS_DIR / "NotoSans-Bold.ttf"),tamanho)

def _carregar_arquivo_fonte(caminho: Path, tamanho: int) -> ImageFont.FreeTypeFont:
    if tamanho <= 0:
        raise ValueError("O tamanho da fonte deve ser maior que zero.")

    if not caminho.is_file():
        raise FileNotFoundError(
            f"Arquivo de fonte não encontrado: {caminho}"
        )

    return ImageFont.truetype(font=str(caminho),size=tamanho)

def carregar_fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    """
    Carrega a fonte principal utilizada nos textos das imagens.

    Usa Noto Sans Regular ou Noto Sans Bold.
    """

    caminho = FONT_BOLD if negrito else FONT_REGULAR

    return _carregar_arquivo_fonte(caminho = caminho, tamanho = tamanho)


def carregar_fonte_simbolo(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    """
    Carrega uma fonte para setas e símbolos Unicode.

    Exemplos:
    ↗ ↖ ↘ ↙ ↑ ↓ ← →
    ⬆ ⬇ ⬅ ➡

    DejaVu Sans costuma ter melhor cobertura desses símbolos.
    """
    caminho = (FONT_SYMBOL_BOLD   if negrito
                                      else FONT_SYMBOL_REGULAR)
    return _carregar_arquivo_fonte(caminho = caminho, tamanho = tamanho)


def carregar_fonte_emoji(tamanho: int) -> ImageFont.FreeTypeFont:
    return _carregar_arquivo_fonte(caminho = FONT_SYMBOL_EMOJI, tamanho = tamanho)


#============================================================#
def teste():
    from PIL import  ImageDraw, Image
    img = Image.new("RGBA", (600, 600), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    fonte = fonte_regular(120)
    font2 = carregar_fonte(50, True)
    draw.text(
        (50,50),
        "25/07",
        fill="black",
        font=fonte
    )
    fonte = fonte_bold(120)
    draw.text(
        (50,100),
        "25/07",
        fill="red",
        font=fonte
    )
    draw.text(
        (100,200),
        "25/07",
        fill="red",
        font=font2
    )
    img.show()
    