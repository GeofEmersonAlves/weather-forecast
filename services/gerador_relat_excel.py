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
===============================================================================
"""
from io import BytesIO
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.worksheet.worksheet import Worksheet
from PIL import Image
import pandas as pd
from services.gerar_img_base64 import base64_para_imagem

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

def preencher_relatorio_clima_Tempo_Agora(clima_json: dict, previsoes : pd.DataFrame) -> BytesIO:
    BASE_DIR = Path(__file__).parent.parent
    caminho_modelo = Path(BASE_DIR / __PATH_MODELS__  / __MODEL_FILE__)
    buffer_file = BytesIO()
    
    if caminho_modelo.exists():
        # Abre o arquivo modelo
        workbook = load_workbook(caminho_modelo)
        
        planilha: Worksheet = workbook["Tempo Agora"]
        
        # Altera células
        planilha["A1"] = clima_json["texto_local"]
        
        imagem_pil = base64_para_imagem(clima_json['img_clima'])
        if imagem_pil is not None:
            imagem_excel = pil_para_imagem_excel(imagem_pil, largura=100, altura = 80)
            planilha.add_image(imagem_excel,"B3")
        else:
            planilha["B3"] = "SEM ICONE"
                 
        temp = clima_json.get('current').get('temperature')
        texto_temp = f"{temp} ºC"
        planilha["D3"] = texto_temp
        
        tab_clima = clima_json['tab_clima']
        planilha["A5"] = tab_clima[0] + (" " * 10) + tab_clima[1]
        planilha["E5"] = tab_clima[2] + (" " * 23) + tab_clima[3]
        
        tab_astro = clima_json['tab_astro']
        
        planilha["D7"] = tab_astro[0][1]
        planilha["D8"] = tab_astro[1][1]
        planilha["D9"] = tab_astro[2][1]
        planilha["D10"] = tab_astro[3][1]
        planilha["D11"] = tab_astro[4][1]
    
        row_excel = 14
        for indice, registro in previsoes.iterrows():
           img = base64_para_imagem(registro.get("dia_bola"))
           if img is not None:
               imagem_excel = pil_para_imagem_excel(img, largura=60, altura = 60)
               planilha.add_image(imagem_excel, f"A{row_excel}")
           else:
               planilha[f"A{row_excel}"] = "SEM ICONE"
            
           imagem_pil = base64_para_imagem(registro.get("icone")) #weather_icon(registro.get("icone"))
           if imagem_pil is not None:
               imagem_excel = pil_para_imagem_excel(imagem_pil, largura = 75, altura = 60)
               planilha.add_image(imagem_excel, f"B{row_excel}")
           else:
               planilha[f"B{row_excel}"] = "SEM ICONE"
           
           img = base64_para_imagem(registro.get("temp_max_min"))
           if img is not None:
               imagem_excel = pil_para_imagem_excel(img, largura=70, altura = 60)
               planilha.add_image(imagem_excel, f"C{row_excel}")
           else:
               planilha[f"C{row_excel}"] = "SEM ICONE"
           
           img = base64_para_imagem(registro.get("Umidade e chuva"))
           if img is not None:
               imagem_excel = pil_para_imagem_excel(img, largura=140, altura = 60)
               planilha.add_image(imagem_excel, f"D{row_excel}")
           else:
               planilha[f"D{row_excel}"] = "SEM ICONE"
                      
           planilha[f"E{row_excel}"] = registro.get('Descrição')
           
           row_excel += 1
           
        workbook.save(buffer_file)
        buffer_file.seek(0) #faz o "cursor" do arquivo voltar para o início
    
    return buffer_file