# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : gerador_de_imagens.py
Autor      : Emerson A. Silva 
Data       : Mon Jul 20 21:55:46 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Esses códigos foram adaptados a partir de códigos gerados no ChatGPT, para gerá-los passei as
informações detalhadas de como seriam as imagens e um arquivo com o dicionário das informações salvo, 
a partir do código gerado fiz as adaptações necessárias no código para ajustar a imagem ao meu gosto e,
também, ajustar ajustes para transformálo em uma função para este serviço.
      

Histórico:
       20/06/2026 - Inicio
       22/06/2026 - Adicionado novos geradores de imagens
       23/07/2026 - Adicionado o gerador da imagem do Quadro do clima
       25/07/2026 - Ajustes na imagem do infoclima para melhorar a visualização e 
                possicionamento dos elementos na imagem
===============================================================================
"""

import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from typing import Any
import cairosvg


DIAS_ABREVIADOS = {
    "Segunda": "Seg",
    "Terça": "Ter",
    "Quarta": "Qua",
    "Quinta": "Qui",
    "Sexta": "Sex",
    "Sábado": "Sáb",
    "Domingo": "Dom",
}

def base64_para_imagem(imagem_base64: str) -> Image.Image | None:
    if not imagem_base64:
        return None

    if "," not in imagem_base64:
        return None

    cabecalho, dados_base64 = imagem_base64.split(",", 1)

    try:
        dados_imagem = base64.b64decode(dados_base64)
        # SVG
        if "image/svg+xml" in cabecalho.lower():
            dados_png = cairosvg.svg2png(bytestring=dados_imagem)
            imagem = Image.open(BytesIO(dados_png))

        # PNG, JPG, WEBP...
        else:
            imagem = Image.open(BytesIO(dados_imagem))

        imagem.load()

        if imagem.mode not in ("RGB", "RGBA"):
            imagem = imagem.convert("RGBA")

        return imagem

    except (ValueError,
            UnidentifiedImageError,
            OSError,
            base64.binascii.Error):
        return None

    except Exception:
        # Qualquer outro erro inesperado
        return None

def imagem_para_base64(caminho_imagem: str | Path) -> str:
    caminho = Path(caminho_imagem)
    if not caminho.exists():
       return None
   
    imagem_base64 = base64.b64encode(caminho.read_bytes()).decode("utf-8")

    return f"data:image/png;base64,{imagem_base64}"

def Image_para_base64(Image_imagem: Image.Image) -> str:
    buffer = BytesIO()
    Image_imagem.save(buffer, format="PNG")
    imagem_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{imagem_base64}"


def carregar_fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    if negrito:
        fontes = [
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("C:/Windows/Fonts/segoeuib.ttf"),
        ]
    else:
        fontes = [
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/segoeui.ttf"),
        ]

    for caminho_fonte in fontes:
        if caminho_fonte.exists():
            return ImageFont.truetype(
                str(caminho_fonte),
                size=tamanho,
            )

    return ImageFont.load_default()


def gerar_dia_base64(
    dia: int | str,
    dia_semana: str,
    tamanho: int = 500,
) -> str:
    """
    Gera uma imagem PNG circular contendo:

    - o número do dia na parte superior;
    - a abreviação do dia da semana na parte inferior.

    Retorna a imagem no formato data:image/png;base64,...
    """

    # Imagem transparente
    imagem = Image.new(
        mode="RGBA",
        size=(tamanho, tamanho),
        color=(0, 0, 0, 0),
    )

    desenho = ImageDraw.Draw(imagem)

    # Cores
    cor_circulo = (238, 238, 238, 255)
    cor_dia =(0, 0, 0 , 255) #(90, 90, 90, 255)
    cor_semana = (110, 110, 110, 255)

    # Margem externa do círculo
    margem = max(2, int(tamanho * 0.01))

    desenho.ellipse(
        (
            margem,
            margem,
            tamanho - margem,
            tamanho - margem,
        ),
        fill=cor_circulo,
    )

    # Fontes proporcionais ao tamanho da imagem
    fonte_dia = carregar_fonte(
        tamanho=max(14, int(tamanho * 0.28)),
        negrito=False,
    )

    fonte_semana = carregar_fonte(
        tamanho=max(14, int(tamanho * 0.25)),
        negrito=False,
    )

    texto_dia = str(dia)

    # Exemplo: "terça-feira" -> "ter"
    texto_semana = dia_semana.strip()[:3].lower()

    # Medidas do texto
    caixa_dia = desenho.textbbox(
        (0, 0),
        texto_dia,
        font=fonte_dia,
    )

    caixa_semana = desenho.textbbox(
        (0, 0),
        texto_semana,
        font=fonte_semana,
    )

    largura_dia = caixa_dia[2] - caixa_dia[0]
  #  altura_dia = caixa_dia[3] - caixa_dia[1]

    largura_semana = caixa_semana[2] - caixa_semana[0]
  #  altura_semana = caixa_semana[3] - caixa_semana[1]

    # Centralização horizontal
    x_dia = (tamanho - largura_dia) / 2
    x_semana = (tamanho - largura_semana) / 2

    # Posições verticais
    y_dia = tamanho * 0.22
    y_semana = tamanho * 0.58

    desenho.text(
        (x_dia, y_dia),
        texto_dia,
        font=fonte_dia,
        fill=cor_dia,
    )

    desenho.text(
        (x_semana, y_semana),
        texto_semana,
        font=fonte_semana,
        fill=cor_semana,
    )

    # Conversão da imagem para PNG em memória
    buffer = BytesIO()
    imagem.save(buffer, format="PNG")

    imagem_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"data:image/png;base64,{imagem_base64}"


def temperaturas_min_max_base64(
    temp_min: int | float,
    temp_max: int | float,
    largura: int = 60,
    altura: int = 46,
) -> str:
    """
    Gera uma imagem PNG contendo:

        ↓ 15°
        ↑ 27°

    e devolve no formato:

        data:image/png;base64,...
    """

    img = Image.new("RGBA", (largura, altura), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    fonte = carregar_fonte(18)

    azul = (33, 150, 243, 255)
    vermelho = (244, 67, 54, 255)
    cor_texto = (90, 90, 90, 255)

    margem_x = 4
    y1 = 4
    y2 = 23
    # -------------------------
    # Temperatura máxima
    # -------------------------
    
    draw.text(
        (margem_x, y2),
        "↑",
        font=fonte,
        fill=vermelho,
    )
    
    draw.text(
        (margem_x + 16, y2),
        f"{temp_max:.0f}°",
        font=fonte,
        fill=cor_texto,
    )
        # -------------------------
        # Temperatura mínima
        # -------------------------
    
    draw.text(
            (margem_x, y1),
            "↓",
            font=fonte,
            fill=azul,
        )

    draw.text(
        (margem_x + 16, y1),
        f"{temp_min:.0f}°",
        font=fonte,
        fill=cor_texto,
    )


    buffer = BytesIO()
    img.save(buffer, format="PNG")

    imagem_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"data:image/png;base64,{imagem_base64}"


def clima_chuva_base64(
    umidade_min: int | float,
    umidade_max: int | float,
    precipitacao: int | float,
    probabilidade_chuva: int | float,
    largura: int = 170,
    altura: int = 62,
) -> str:
    """
    Gera uma imagem PNG com:

        gota  umidade mínima – máxima
        chuva precipitação   guarda-chuva probabilidade

    Retorna no formato:

        data:image/png;base64,...
    """

    imagem = Image.new(
        mode="RGBA",
        size=(largura, altura),
        color=(255, 255, 255, 0),
    )

    desenho = ImageDraw.Draw(imagem)

    fonte = carregar_fonte(16)
    fonte_negrito = carregar_fonte(16, negrito=True)

    # Cores
    azul = (30, 136, 229, 255)
    azul_escuro = (21, 101, 192, 255)
    cinza = (85, 85, 85, 255)
    cinza_claro = (125, 125, 125, 255)

    # -------------------------------------------------
    # Funções internas para desenhar os ícones
    # -------------------------------------------------

    def desenhar_gota(x: int, y: int) -> None:
        """Desenha uma gota de água."""

        pontos = [
            (x + 7, y),
            (x + 2, y + 8),
            (x + 1, y + 12),
            (x + 3, y + 16),
            (x + 7, y + 18),
            (x + 11, y + 16),
            (x + 13, y + 12),
            (x + 12, y + 8),
        ]

        desenho.polygon(pontos, fill=azul)

        desenho.ellipse(
            (x + 1, y + 8, x + 13, y + 19),
            fill=azul,
        )

    def desenhar_chuva(x: int, y: int) -> None:
        """Desenha uma pequena nuvem com chuva."""

        cor_nuvem = (105, 105, 105, 255)

        desenho.ellipse(
            (x + 1, y + 2, x + 10, y + 11),
            fill=cor_nuvem,
        )

        desenho.ellipse(
            (x + 6, y, x + 17, y + 11),
            fill=cor_nuvem,
        )

        desenho.ellipse(
            (x + 13, y + 3, x + 21, y + 11),
            fill=cor_nuvem,
        )

        desenho.rectangle(
            (x + 4, y + 6, x + 18, y + 11),
            fill=cor_nuvem,
        )

        # Pingos
        desenho.line(
            (x + 6, y + 14, x + 4, y + 18),
            fill=azul,
            width=2,
        )

        desenho.line(
            (x + 12, y + 14, x + 10, y + 18),
            fill=azul,
            width=2,
        )

        desenho.line(
            (x + 18, y + 14, x + 16, y + 18),
            fill=azul,
            width=2,
        )

    def desenhar_guarda_chuva(x: int, y: int) -> None:
        """Desenha um pequeno guarda-chuva."""

        # Parte superior
        desenho.pieslice(
            (x, y, x + 18, y + 18),
            start=180,
            end=360,
            fill=azul_escuro,
        )

        # Cabo
        desenho.line(
            (x + 9, y + 9, x + 9, y + 18),
            fill=azul_escuro,
            width=2,
        )

        desenho.arc(
            (x + 9, y + 14, x + 15, y + 21),
            start=0,
            end=110,
            fill=azul_escuro,
            width=2,
        )

    # -------------------------------------------------
    # Formatação dos valores
    # -------------------------------------------------

    texto_umidade = (
        f"{umidade_min:.0f}% – "
        f"{umidade_max:.0f}%"
    )

    texto_precipitacao = (
        f"{precipitacao:.1f} mm"
    ).replace(".", ",")

    texto_probabilidade = (
        f"{probabilidade_chuva:.0f}%"
    )

    # -------------------------------------------------
    # Primeira linha: umidade
    # -------------------------------------------------

    desenhar_gota(
        x=8,
        y=5,
    )

    desenho.text(
        (31, 5),
        texto_umidade,
        font=fonte_negrito,
        fill=cinza,
    )

    # -------------------------------------------------
    # Segunda linha: chuva e probabilidade
    # -------------------------------------------------

    desenhar_chuva(
        x=5,
        y=34,
    )

    desenho.text(
        (31, 34),
        texto_precipitacao,
        font=fonte,
        fill=cinza,
    )

    desenhar_guarda_chuva(
        x=112,
        y=34,
    )

    desenho.text(
        (137, 34),
        texto_probabilidade,
        font=fonte,
        fill=cinza_claro,
    )

    # -------------------------------------------------
    # Conversão para Base64
    # -------------------------------------------------

    buffer = BytesIO()
    imagem.save(buffer, format="PNG")

    imagem_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"data:image/png;base64,{imagem_base64}"


#Gera uma imagem com a fase da Lua, data e dia da semana.
def gerar_imagem_fase_lua(
    nome_fase: str,
    data: str,
    dia_semana: str,
    imagem_lua_base64: str,
    largura: int = 500,
    altura: int = 500,
    ) -> Image.Image:
    
 
    # Fundo preto
    imagem_final = Image.new(
        mode="RGB",
        size=(largura, altura),
        color="black",
    )

   
    # Espaço reservado para os textos inferiores
    margem = 0
    altura_textos = 15

    tamanho_maximo_lua = (
        largura - 2 * margem,
        altura - altura_textos - margem,
    )
     
    imagem_lua = base64_para_imagem(imagem_lua_base64)
     
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

def carregar_fonte_emoji(tamanho: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    fontes = [
        "C:/Windows/Fonts/seguiemj.ttf",
        "C:/Windows/Fonts/seguisym.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]

    for caminho in fontes:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)

    return ImageFont.load_default()

def carregar_fonte_simbolo(tamanho: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """
    Carrega uma fonte para setas e outros símbolos Unicode.

    Esta fonte costuma renderizar corretamente:
    ↗ ↖ ↘ ↙ ↑ ↓ ← →
    ⬆ ⬇ ⬅ ➡
    """

    fontes = [
        "C:/Windows/Fonts/seguisym.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    for caminho in fontes:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)

    return ImageFont.load_default()

def eh_emoji(caractere: str) -> bool:
    """Verifica se o caractere pertence a faixas comuns de emojis."""
    if not caractere:
        return False

    codigo = ord(caractere)
    return (
        0x1F000 <= codigo <= 0x1FAFF
        or 0x2600 <= codigo <= 0x26FF
        or 0x2700 <= codigo <= 0x27BF
    )

def eh_simbolo(caractere: str) -> bool:
    """Verifica se o caractere é uma seta ou símbolo semelhante."""

    if not caractere:
        return False

    codigo = ord(caractere)

    return (
        0x2190 <= codigo <= 0x21FF  # ← ↑ → ↓ ↗ ↘ etc.
        or 0x2B00 <= codigo <= 0x2BFF  # ⬆ ⬇ ⬅ etc.
        or caractere in {
            "▲",
            "▼",
            "△",
            "▽",
            "◀",
            "▶",
            "●",
            "○",
        }
    )

def limpar_variacoes_unicode(texto: str) -> str:
    return (
        texto
        .replace("\ufe0f", "")
        .replace("\ufe0e", "")
    )


def desenhar_texto_unicode(draw: ImageDraw.ImageDraw,
                            posicao: tuple[int, int],
                            texto: str,
                            fonte_texto: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                            fonte_emoji: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                            fonte_simbolo: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                            cor: str | tuple[int, int, int] = "#202124") -> int:
    """
    Desenha texto misturando fonte comum, emojis e símbolos.

    Diferentemente da função anterior, esta verifica todos os
    caracteres do texto, não apenas o primeiro.

    Retorna a coordenada X onde o texto terminou.
    """

    if not texto:
        return posicao[0]

    texto = limpar_variacoes_unicode(str(texto))

    x, y = posicao

    for caractere in texto:
        if eh_simbolo(caractere):
            fonte_atual = fonte_simbolo
            usar_cor_embutida = False

        elif eh_emoji(caractere):
            fonte_atual = fonte_emoji
            usar_cor_embutida = True

        else:
            fonte_atual = fonte_texto
            usar_cor_embutida = False

        try:
            draw.text(
                (x, y),
                caractere,
                font=fonte_atual,
                fill=cor,
                embedded_color=usar_cor_embutida,
            )

        except (ValueError, OSError):
            # Algumas versões do Pillow ou algumas fontes não
            # aceitam embedded_color.
            draw.text(
                (x, y),
                caractere,
                font=fonte_atual,
                fill=cor,
            )

        largura_caractere = draw.textlength(
            caractere,
            font=fonte_atual,
        )

        x += max(int(largura_caractere), 1)

    return x

def largura_texto_unicode(draw: ImageDraw.ImageDraw,
                            texto: str,
                            fonte_texto: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                            fonte_emoji: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                            fonte_simbolo: ImageFont.FreeTypeFont | ImageFont.ImageFont
                          ) -> int:
    """Calcula a largura aproximada de um texto com emojis e símbolos."""
    texto = limpar_variacoes_unicode(str(texto))
    largura = 0.0

    for caractere in texto:
        if eh_simbolo(caractere):
            fonte_atual = fonte_simbolo

        elif eh_emoji(caractere):
            fonte_atual = fonte_emoji

        else:
            fonte_atual = fonte_texto

        largura += draw.textlength(
            caractere,
            font=fonte_atual,
        )

    return int(largura)

def ajustar_texto(draw: ImageDraw.ImageDraw,
                    texto: str,
                    largura_maxima: int,
                    fonte_texto: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                    fonte_emoji: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                    fonte_simbolo: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                ) -> str:
    """
    Reduz o texto com reticências quando ele ultrapassa
    a largura reservada.
    """

    texto = limpar_variacoes_unicode(str(texto))

    if largura_texto_unicode(
        draw,
        texto,
        fonte_texto,
        fonte_emoji,
        fonte_simbolo,
    ) <= largura_maxima:
        return texto

    reticencias = "..."

    while texto:
        texto = texto[:-1].rstrip()

        texto_reduzido = f"{texto}{reticencias}"

        largura = largura_texto_unicode(
            draw,
            texto_reduzido,
            fonte_texto,
            fonte_emoji,
            fonte_simbolo,
        )

        if largura <= largura_maxima:
            return texto_reduzido

    return reticencias

def quadro_clima_base64(dados_clima: dict[str, Any],
                        largura: int = 600,
                        altura: int = 300,
                        ) -> Image.Image | None:
    
    if not isinstance(dados_clima, dict):
        return None

    try:
        # =========================================================
        # Dados do dicionário
        # =========================================================
        
        current = dados_clima.get("current") or {}

        valor_temperatura = current.get("temperature")

        if valor_temperatura not in (None, ""):
            temperatura = f"{valor_temperatura} °C"
        else:
            temperatura = "-- °C"

        tab_clima = dados_clima.get("tab_clima") or []
        tab_astro = dados_clima.get("tab_astro") or []
        fase_lua = dados_clima.get("fase_lua") or {}

        imagem_clima = base64_para_imagem(
            dados_clima.get("img_clima")
        )

        # =========================================================
        # Imagem principal
        # =========================================================
        imagem = Image.new(
            mode = "RGBA",
            size = (largura, altura),
            color = "#FFFFFF"  #(0, 0, 0, 0) Tranparente   "#FFFFFF"->Branco
         )

        draw = ImageDraw.Draw(imagem)

        # =========================================================
        # Fontes
        # =========================================================
       # fonte_titulo = carregar_fonte(13)
        fonte_temperatura = carregar_fonte(40, True)
        fonte_clima = carregar_fonte(12, True)  #True para negrito
        fonte_tabela = carregar_fonte(14)
        fonte_lua = carregar_fonte(14)

        fonte_emoji_clima = carregar_fonte_emoji(14)
        fonte_emoji_tabela = carregar_fonte_emoji(12)
        fonte_emoji_lua = carregar_fonte_emoji(12)

        fonte_simbolo_clima = carregar_fonte_simbolo(12)
        fonte_simbolo_tabela = carregar_fonte_simbolo(12)
        fonte_simbolo_lua = carregar_fonte_simbolo(12)

        # =========================================================
        # Cores
        # =========================================================
        cor_texto = "#202124"
        cor_secundaria = "#3C4043"
        cor_temperatura = "#FF4B22"
        cor_linha = "#D5DCE5"

        margem = 5

        # =========================================================
        # Ícone e temperatura
        # =========================================================
        centro_imagem = largura // 2

        if imagem_clima is not None:
            imagem_clima.thumbnail(
                (200, 200),
                Image.Resampling.LANCZOS,
            )

            x_icone = centro_imagem - 50
            y_icone = 10

            imagem.alpha_composite(
                imagem_clima,
                dest=(x_icone, y_icone),
            )

        largura_temperatura = draw.textlength(
            temperatura,
            font=fonte_temperatura,
        )

        x_temperatura = centro_imagem + 30
        y_temperatura = 10

        # Garante que a temperatura não ultrapasse a imagem.
        x_temperatura = min(
            x_temperatura,
            largura - int(largura_temperatura) - margem,
        )

        draw.text(
            (x_temperatura, y_temperatura),
            temperatura,
            font=fonte_temperatura,
            fill=cor_temperatura,
        )

        # =========================================================
        # Informações de tab_clima
        # =========================================================
        y_tab_clima = 90

        quantidade_colunas = max(
            min(len(tab_clima), 4),
            1,
        )

        largura_disponivel = largura - (margem * 2)
        largura_coluna = largura_disponivel // quantidade_colunas

        for indice, item in enumerate(tab_clima[:4]):
            x_coluna = margem + indice * largura_coluna

            # Reserva um pequeno espaço entre as colunas.
            largura_texto_maxima = largura_coluna - 2

            texto_ajustado = ajustar_texto(
                draw=draw,
                texto=str(item),
                largura_maxima=largura_texto_maxima,
                fonte_texto=fonte_clima,
                fonte_emoji=fonte_emoji_clima,
                fonte_simbolo=fonte_simbolo_clima,
            )

            desenhar_texto_unicode(
                draw=draw,
                posicao=(x_coluna, y_tab_clima),
                texto=texto_ajustado,
                fonte_texto=fonte_clima,
                fonte_emoji=fonte_emoji_clima,
                fonte_simbolo=fonte_simbolo_clima,
                cor=cor_secundaria,
            )

        # =========================================================
        # Tabela tab_astro
        # =========================================================
        inicio_tabela_y = 115
        altura_linha = 22

        x_texto_esquerdo = 60
        x_texto_direito = int(largura * 0.58)

        for indice, linha in enumerate(tab_astro):
            if not isinstance(linha, (list, tuple)):
                continue

            if len(linha) < 2:
                continue

            y = inicio_tabela_y + indice * altura_linha

            if y + altura_linha > altura - 38:
                break

            texto_esquerdo = str(linha[0])
            texto_direito = str(linha[1])

            desenhar_texto_unicode(
                draw=draw,
                posicao=(x_texto_esquerdo, y + 5),
                texto=texto_esquerdo,
                fonte_texto=fonte_tabela,
                fonte_emoji=fonte_emoji_tabela,
                fonte_simbolo=fonte_simbolo_tabela,
                cor=cor_texto,
            )

            desenhar_texto_unicode(
                draw=draw,
                posicao=(x_texto_direito, y + 5),
                texto=texto_direito,
                fonte_texto=fonte_tabela,
                fonte_emoji=fonte_emoji_tabela,
                fonte_simbolo=fonte_simbolo_tabela,
                cor=cor_texto,
            )

            draw.line(
                (
                    0,
                    y + altura_linha,
                    largura,
                    y + altura_linha,
                ),
                fill=cor_linha,
                width=1,
            )

        # =========================================================
        # Fase da Lua
        # =========================================================
        emoji_lua = fase_lua.get("emoji", "🌙")

        nome_lua = (
            fase_lua.get("nome")
            or fase_lua.get("descricao")
            or "Fase da Lua"
        )

        texto_lua = f"{emoji_lua} {nome_lua}"

        desenhar_texto_unicode(
            draw=draw,
            posicao=(margem, altura - 29),
            texto=texto_lua,
            fonte_texto=fonte_lua,
            fonte_emoji=fonte_emoji_lua,
            fonte_simbolo=fonte_simbolo_lua,
            cor=cor_texto,
        )

        return imagem.convert("RGB")
    

    except (
        KeyError,
        TypeError,
        ValueError,
        OSError,
    ):
        return None