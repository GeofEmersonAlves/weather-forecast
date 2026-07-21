# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : pega_infoclima.py
Autor      : Emerson A. Silva
Data       : Mon Jul 20 10:21:56 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
         Serviço que busca as informações do clima, essas informações podem virda API para clima,
      caso não consiga faz um scrapping do TempoAgora para obter as informações do clima, 
        

Histórico:
       20/07/2027 - Inicio ......
===============================================================================
"""

import services.weather_api as wt_api 
from services.weatherinfo_scraped import clima_agora as scrap_clima_agora
#from services.salva_dict import salvar_json


def info_clima_agora(cidade : dict) -> dict:
    lat = cidade["lat"]
    long = cidade["long"]
        
    info_clima_json = wt_api.clima_agora(lat, long)
    #salvar =  info_clima_json.copy()
    #salvar['img_clima'] = 'imagem'
    #salvar_json(salvar,"infoclima.json")
    
    if not info_clima_json:
        info_clima_json = scrap_clima_agora(cidade)
               
    
    return info_clima_json