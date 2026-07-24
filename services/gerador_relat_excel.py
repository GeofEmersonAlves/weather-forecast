# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : gerador_relat_excel.py 
Autor      : Emerson A. Silva
Data       : Wed Jul 22 22:25:40 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Salva as informações exibidas no dashboad em um relatorio em Excel ja pré 
 formatado, é utilizado o arquivo de template que esta em 
  /template/excel/ReportTemplate.xlsx
    
  Abre o arquivo de modelo, coloca as informações atuais do clima e manda um BytesIO  

Histórico:
       22/07/2026 - Inicio 
       23/07/2026 - Alterações para melhoria da performance na geração do relatório
       23/07/2026 - O quadro do clima agora vira uma imagem feita com as informações do info_clima
===============================================================================
"""
from io import BytesIO
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.worksheet.worksheet import Worksheet
from PIL import Image, ImageOps
import plotly.graph_objects as go
import pandas as pd
from services.gerador_de_imagens import base64_para_imagem, quadro_clima_base64

__PATH_MODELS__=  Path("templates/excel")
__MODEL_FILE__ = "ReportTemplate.xlsx"


def pil_para_imagem_excel(imagem: Image.Image, largura: int = 80, altura: int = 60,) -> ExcelImage:
    buffer = BytesIO()

    imagem.convert("RGBA").save(
        buffer,
        format="PNG",
    )

    buffer.seek(0)

    imagem_excel = ExcelImage(buffer)
    imagem_excel.width = largura
    imagem_excel.height = altura

    # Mantém o buffer vivo enquanto a planilha é salva
    imagem_excel._buffer_referencia = buffer

    return imagem_excel

def plotly_para_imagem_excel(
    fig: go.Figure,
    largura_exportacao: int = 1400,
    altura_exportacao: int = 650,
    largura_excel: int = 900,
    largura_borda: int = 3,
    cor_borda: str = "#202020",
) -> ExcelImage:
    """
    Converte um gráfico Plotly em PNG, adiciona borda
    e retorna uma imagem pronta para inserir no Excel.

    A altura no Excel é calculada automaticamente para
    preservar a proporção da imagem.
    """

    fig.update_layout(
        width=largura_exportacao,
        height=altura_exportacao,
        margin=dict(
            l=90,
            r=40,
            t=100,
            b=100,
        ),
    )

    fig.update_xaxes(
        tickangle=0,
        automargin=True,
    )

    fig.update_yaxes(
        automargin=True,
    )

    imagem_bytes = fig.to_image(
        format="png",
        width=largura_exportacao,
        height=altura_exportacao,
        scale=2,
    )

    imagem_pil = Image.open(BytesIO(imagem_bytes)).convert("RGB")

    imagem_pil = ImageOps.expand(
        imagem_pil,
        border=largura_borda,
        fill=cor_borda,
    )

    buffer_imagem = BytesIO()
    imagem_pil.save(buffer_imagem, format="PNG")
    buffer_imagem.seek(0)

    imagem_excel = ExcelImage(buffer_imagem)

    # Proporção original da imagem
    proporcao = imagem_pil.height / imagem_pil.width

    imagem_excel.width = largura_excel
    imagem_excel.height = int(largura_excel * proporcao)

    # Mantém o buffer aberto até o workbook ser salvo
    imagem_excel._buffer_imagem = buffer_imagem

    return imagem_excel

def preencher_relatorio_clima_Tempo_Agora(clima_json: dict, 
                                          previsoes: pd.DataFrame,
                                          mapa_imet1: Image.Image,
                                          mapa_imet2: Image.Image,
                                          graf_temp_maxmin: go.Figure,
                                          graf_umid_maxmim: go.Figure,
                                          graf_chuva: go.Figure) -> BytesIO:
   
    BASE_DIR = Path(__file__).parent.parent
    caminho_modelo = Path(BASE_DIR / __PATH_MODELS__  / __MODEL_FILE__)
    buffer_file = BytesIO()
    
    if caminho_modelo.exists():
        # Abre o arquivo modelo
        workbook = load_workbook(caminho_modelo)
        # Seleciona a planilha que vai trabalhar 
        planilha: Worksheet = workbook["Tempo Agora"]
        
        if clima_json is not None:
            # Coloca o Titulo
            planilha["B1"] = clima_json["texto_local"]
            
            #Gera a imagem do Quadro do clima e coloca no relatório
            img_quadro_clima = quadro_clima_base64(clima_json)
            imagem_excel = pil_para_imagem_excel(img_quadro_clima, largura = 530, altura = 310)
            planilha.add_image(imagem_excel, "B2")
        
        #Coloca a imagem o mapa de precipitação no relatório
        # Adiciona uma borda preta de 2 pixels
        mapa_imet2 = ImageOps.expand(mapa_imet2,
                                     border=1,
                                     fill="#000000",   # cor da borda
                                    )
        imagem_excel = pil_para_imagem_excel(mapa_imet2, largura=310, altura = 310)
        planilha.add_image(imagem_excel, "G2")
        
        #Coloca os gráficos no relatório
        larg_grfs = 414
        alt_grfs = 263.2
         
        imagem_excel = plotly_para_imagem_excel(graf_temp_maxmin,
                                                largura_exportacao=1400,
                                                altura_exportacao=650,
                                                largura_excel=larg_grfs,
                                               )
        planilha.add_image(imagem_excel, "B20")
        
        imagem_excel = plotly_para_imagem_excel(graf_umid_maxmim,
                                                largura_exportacao=1400,
                                                altura_exportacao=650,
                                                largura_excel=larg_grfs,
                                               )
        planilha.add_image(imagem_excel, "F20")
        
        imagem_excel = plotly_para_imagem_excel(graf_chuva,
                                                largura_exportacao=1400,
                                                altura_exportacao=650,
                                                largura_excel=larg_grfs,
                                               )
        planilha.add_image(imagem_excel, "B34")
        
    
        #Monta a tabela de previsões
        row_excel = 4
        for indice, registro in previsoes.iterrows():
           img = base64_para_imagem(registro.get("dia_bola"))
           if img is not None:
               imagem_excel = pil_para_imagem_excel(img, largura=60, altura = 60)
               planilha.add_image(imagem_excel, f"B{row_excel}")
           else:
               planilha[f"B{row_excel}"] = "SEM ICONE"
            
           imagem_pil = base64_para_imagem(registro.get("icone")) #weather_icon(registro.get("icone"))
           if imagem_pil is not None:
               imagem_excel = pil_para_imagem_excel(imagem_pil, largura = 60, altura = 60)
               planilha.add_image(imagem_excel, f"C{row_excel}")
           else:
               planilha[f"C{row_excel}"] = "SEM ICONE"
           
           img = base64_para_imagem(registro.get("temp_max_min"))
           if img is not None:
               imagem_excel = pil_para_imagem_excel(img, largura=70, altura = 60)
               planilha.add_image(imagem_excel, f"D{row_excel}")
           else:
               planilha[f"D{row_excel}"] = "SEM ICONE"
           
           img = base64_para_imagem(registro.get("Umidade e chuva"))
           if img is not None:
               imagem_excel = pil_para_imagem_excel(img, largura=140, altura = 60)
               planilha.add_image(imagem_excel, f"E{row_excel}")
           else:
               planilha[f"E{row_excel}"] = "SEM ICONE"
                      
           planilha[f"F{row_excel}"] = registro.get('Descrição')
           
           row_excel += 1
           
        workbook.save(buffer_file)
        buffer_file.seek(0) #faz o "cursor" do arquivo voltar para o início
    
    return buffer_file