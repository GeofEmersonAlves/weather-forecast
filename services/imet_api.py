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
        Faz uma requisicao na API do IMET para pegar os mapas de precipitacao 
    

Histórico:
       17/07/2026 - Inicio 
       01/08/2026 - Melhora no tratamento da resosta do INMET, mudança do cache
===============================================================================
"""
from functools import lru_cache  #Para fazer um cache da imagem, não precisa instalar, ja vem com o Python
from services.requisicao import faz_requisicao

__URL__ = "https://apiclima.inmet.gov.br/"

def url_inmet()->str:
    return __URL__

@lru_cache(maxsize = 5)
def mapas_precipitacao(ANO : int, PERIODO : str, MES : int) -> list[dict]:
    HEAD = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        )
    }
    
    url = f"{__URL__}progp/{ANO}/{PERIODO}/{MES}"
   
    resposta = faz_requisicao(url, HEAD = HEAD, use_raise = True)

    dados = []    
    if resposta:
        if resposta.status_code == 200:
            dados = resposta.json()

    return dados