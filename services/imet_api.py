# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : imet.py
Autor      : Emerson
Data       : Fri Jul 17 16:57:31 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Faz uma requisicao na API do IMET para pegar a imagem de precipitacao 
      

Histórico:
       17/07/2026 - Inicio 
===============================================================================
"""
from services.requisicao import faz_requisicao
import base64
from io import BytesIO
from PIL import Image
import streamlit as st

@st.cache_data(show_spinner="⏳ Carregando mapa de precipitação . . .",  ttl = 43200) #Cache de 12 hora para o mapa de precipitacao
def mapa_precipitacao(ANO : int, PERIODO : str, MES : int) -> Image.Image | None:
    HEAD = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        )
    }
    
    url = f"https://apiclima.inmet.gov.br/progp/{ANO}/{PERIODO}/{MES}"
   
    resposta = faz_requisicao(url, HEAD = HEAD, use_raise = True)
    
    if resposta:
        dados = resposta.json()
        base64_img = dados[0]["base64"]    
        imagem = Image.open(BytesIO(base64.b64decode(base64_img.split(",", 1)[1])))
          
    else:
        imagem = None
    
    return imagem