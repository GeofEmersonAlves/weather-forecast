# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    :
Arquivo    : 
Autor      : Emerson
Data       : Wed Jul 22 00:09:23 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        
      

Histórico:
       dd/mm/aaaa - Inicio ......
===============================================================================
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGENS_LUA = {
    "nova": "lua_nova.jpg",
    "crescente": "lua_crescente.jpg",
    "quarto_crescente": "lua_quarto_crescente.jpg",
    "crescente_gibosa": "lua_gibosa_crescente.jpg",
    "cheia": "lua_cheia.jpg",
    "minguante_gibosa": "lua_gibosa_minguante.jpg",
    "quarto_minguante": "lua_quarto_minguante.jpg",
    "minguante": "lua_minguante.jpg",
}


NOMES_FASES = {
    "nova": "Lua nova",
    "crescente": "Lua crescente",
    "quarto_crescente": "Quarto crescente",
    "crescente_gibosa": "Lua gibosa crescente",
    "cheia": "Lua cheia",
    "minguante_gibosa": "Lua gibosa minguante",
    "quarto_minguante": "Quarto minguante",
    "minguante": "Lua minguante",
}


DIAS_ABREVIADOS = {
    "Segunda": "Seg",
    "Terça": "Ter",
    "Quarta": "Qua",
    "Quinta": "Qui",
    "Sexta": "Sex",
    "Sábado": "Sáb",
    "Domingo": "Dom",
}


def carregar_fonte(
    tamanho: int,
    negrito: bool = False,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Carrega uma fonte do Windows ou usa a fonte padrão."""

    if negrito:
        fontes = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
    else:
        fontes = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]

    for caminho in fontes:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)

    return ImageFont.load_default()


def gerar_imagem_fase_lua(
    fase_lua: str,
    data: str,
    dia_semana: str,
    pasta_imagens: str = "assets/images",
    largura: int = 500,
    altura: int = 500,
) -> Image.Image:
    """
    Gera uma imagem com a fase da Lua, data e dia da semana.
    """

    fase_lua = fase_lua.strip().lower()

    nome_arquivo = IMAGENS_LUA.get(fase_lua)

    if nome_arquivo is None:
        raise ValueError(f"Fase da Lua desconhecida: {fase_lua}")

    PASTA_IMAGENS = BASE_DIR / "assets" / "images"
    caminho_lua = Path(PASTA_IMAGENS / nome_arquivo)

    if not caminho_lua.exists():
        raise FileNotFoundError(
            f"Imagem da Lua não encontrada: {caminho_lua}"
        )

    # Fundo preto
    imagem_final = Image.new(
        mode="RGB",
        size=(largura, altura),
        color="black",
    )

    # Abre a imagem correspondente à fase
    imagem_lua = Image.open(caminho_lua).convert("RGB")

    # Espaço reservado para os textos inferiores
    margem = 0
    altura_textos = 15

    tamanho_maximo_lua = (
        largura - 2 * margem,
        altura - altura_textos - margem,
    )

    # Redimensiona sem deformar
    imagem_lua.thumbnail(
        tamanho_maximo_lua,
        Image.Resampling.LANCZOS,
    )

    posicao_x = (largura - imagem_lua.width) // 2
    posicao_y = 10

    imagem_final.paste(
        imagem_lua,
        (posicao_x, posicao_y),
    )

    desenho = ImageDraw.Draw(imagem_final)

    fonte_data = carregar_fonte(27, negrito=True)
    fonte_dia = carregar_fonte(27, negrito=True)
    fonte_fase = carregar_fonte(27, negrito=True)

    dia_abreviado = DIAS_ABREVIADOS.get(
        dia_semana,
        dia_semana[:3],
    )
    dia_abreviado = f"Hoje ({dia_abreviado})"
    nome_fase = NOMES_FASES.get(
        fase_lua,
        fase_lua.replace("_", " ").title(),
    )

    # Data, no canto inferior esquerdo
    desenho.text(
        (15, altura - 500),
        data,
        fill="white",
        font=fonte_data,
    )

    # Dia da semana, abaixo da data
    desenho.text(
        (20, altura - 470),
        dia_abreviado,
        fill="white",
        font=fonte_dia,
    )

    # Calcula o tamanho do texto para alinhar à direita
    caixa_texto = desenho.textbbox(
        (0, 0),
        nome_fase,
        font=fonte_fase,
    )

    largura_texto = caixa_texto[2] - caixa_texto[0]

    desenho.text(
        (
            largura - largura_texto - 15,
            altura - 40,
        ),
        nome_fase,
        fill="white",
        font=fonte_fase,
    )

    return imagem_final


previsao = {
    "dia": "22/07",
    "dia_semana": "Quarta",
    "fase_lua": "crescente_gibosa",
}

imagem = gerar_imagem_fase_lua(
    fase_lua=previsao["fase_lua"],
    data=previsao["dia"],
    dia_semana=previsao["dia_semana"],
)

imagem.show()