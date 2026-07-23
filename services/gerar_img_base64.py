# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : gerar_img_base64.py
Autor      : Emerson A. Silva 
Data       : Mon Jul 20 21:55:46 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Peguei este codigo pronto, ele gera uma imagem de um circulo com 
   o dia e o dia da semana dentro
      

Histórico:
       20/06/2026 - Inicio
===============================================================================
"""

import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
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
    """
    Tenta carregar uma fonte TrueType comum do Windows.
    Caso não encontre, utiliza a fonte padrão do Pillow.
    """

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

