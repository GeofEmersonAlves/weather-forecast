# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : previsao_tempo.py
Autor      : Emerson
Data       : Mon Jul 20 19:26:30 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    Faz scrapping na pagina de previsoes de tempo do tempo agora
para pegar as informações de previsão do tempo para 15 dias.
     #https://tempoagora.uol.com.br/dist/images/v2/svg/6.svg

    No html ja vem um json com os dados da previsao,  pego o json e tenho 
todos os dados de previsão da pagina

div class="_none" data-visualization-content="calendar">
            <div class="calendar" id="calendar" data-infos="[{&

Histórico:
       20/07/2026 - Inicio 
       21/07/2026 - Correção da url, estava pegando a previsao sempre de sao paulo
===============================================================================
"""
import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import services.requisicao as req
from services.busca_cidades import traz_cidade_clima
from services.weatherinfo_scraped import gera_url

#558/saopaulo-sp

@st.cache_data(show_spinner="⏳ Carregando previsão do tempo . . .",  ttl = 1800)
def pega_previsao_tempo(dados_cidade : dict)->dict:    
    __URLS__ =["https://tempoagora.uol.com.br/previsao-do-tempo/15-dias/cidade/",
           "https://tempoagora.uol.com.br/dist/images/v2/svg/"]

    cidade_clima = traz_cidade_clima(dados_cidade)

    cidade = cidade_clima['city']
    estado = cidade_clima["uf"]
    id_cid = cidade_clima["idcity"]
     
    url_dados = gera_url(__URLS__[0], id_cid, cidade, estado)

    resp = req.faz_requisicao(url_dados)
    soup = BeautifulSoup(resp.text, "lxml")

    calendario = soup.select_one("#calendar")
    dados_json = calendario.get("data-infos")
    dados = json.loads(dados_json)

    previsoes = []
    for dia in dados:
            previsao = {
                "data": dia.get("date"),
                "dia": dia.get("day"),
                "dia_semana": dia.get("dayWeekFullMin"),
    
                "temp_min": dia.get("temperature", {}).get("min"),
                "temp_max": dia.get("temperature", {}).get("max"),
    
                "precipitacao_mm": dia.get("rain", {}).get("precipitation"),
                "probabilidade_chuva": dia.get("rain", {}).get("probability"),
    
                "descricao": (
                    dia.get("textIcon", {})
                    .get("text", {})
                    .get("pt")
                ),
    
                "icone": (
                    dia.get("textIcon", {})
                    .get("icon", {})
                    .get("day")
                ),
    
                "umidade_min": dia.get("humidity", {}).get("min"),
                "umidade_max": dia.get("humidity", {}).get("max"),
    
                "vento_minimo": dia.get("wind", {}).get("minVelocity"),
                "vento_maximo": dia.get("wind", {}).get("maxVelocity"),
                "direcao_vento": dia.get("wind", {}).get("direction"),
    
                "nascer_sol": dia.get("sun", {}).get("sunshine"),
                "por_sol": dia.get("sun", {}).get("sunset"),
    
                "fase_lua": dia.get("moonPhases", {}).get("phase"),
            }
    
            previsoes.append(previsao)
        
    for day in previsoes:
        cod_ico = day["icone"]
        # Download do ícone 
        url_weather_icon = urljoin(__URLS__[1], f"{cod_ico}.svg")
        
        day["icone"] = url_weather_icon
        
    return previsoes
    


