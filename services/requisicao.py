# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : requisicao.py
Autor      : Emerson A. Silva
Data       : Thu Jul 16 17:33:22 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Classe que gerencia as requisicoes a api e paginas html
      

Histórico:
       16/07/2026 - Inicio 
===============================================================================
"""

#Importação da bibliotecas
import requests
from requests import Response
from requests.exceptions import RequestException

def cria_headers() -> dict[str, str]:
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Connection": "keep-alive",
    }


def faz_requisicao(URL : str, HEAD : dict[str, str] | None = None, use_raise : bool = True) -> Response | None:
    try:
      res = requests.get(
            url=URL,
            headers=HEAD,
            timeout=15
        )
      
      if use_raise:
          res.raise_for_status()
     
      return res
       
    except RequestException as erro:
        print(f"Falha na requisição: {erro}")
        return None


#print(requests.__version__)