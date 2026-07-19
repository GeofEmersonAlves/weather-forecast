# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : geolocalization.py
Autor      : Emerson A. Silva
Data       : Thu Jul 16 17:25:12 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
      Faz uma requisicao a uma API que retorna a geolocalizão pelo numero IP  
      

Histórico:
       16/07/2026 - Inicio do cogigo
===============================================================================
"""
import streamlit as st
import services.requisicao as req
from geopy.geocoders import Nominatim  # OpenStreetMap(GRATUITO)

__ESTADO_UF__ = {
    "acre": "AC", "alagoas": "AL", "amapá": "AP", "amazonas": "AM",
    "bahia": "BA", "ceará": "CE", "distrito federal": "DF", "espírito santo": "ES",
    "goiás": "GO", "maranhão": "MA", "mato grosso": "MT", "mato grosso do sul": "MS",
    "minas gerais": "MG", "pará": "PA", "paraíba": "PB", "paraná": "PR",
    "pernambuco": "PE", "piauí": "PI", "rio de janeiro": "RJ", "rio grande do norte": "RN",
    "rio grande do sul": "RS", "rondônia": "RO", "roraima": "RR", "santa catarina": "SC",
    "são paulo": "SP", "sergipe": "SE", "tocantins": "TO"
}

def sigla_estado(nome_estado : str) -> str:
    nome_limpo = nome_estado.strip().lower()
    return __ESTADO_UF__.get(nome_limpo, "Estado não encontrado")


def geolocation_with_latlon(lat : str, lon : str)-> dict | None:
    geo = Nominatim(user_agent="meu_app")
    
    local = geo.reverse(f"{lat},{lon}")
    
    return local.raw

@st.cache_data(show_spinner="⏳ Carregando coordenadas pelo IP . . .",  ttl = 1800)
def geolocation_by_IP() -> dict | None:
    url = (
         "http://ip-api.com/json/"
         "?fields=status,message,country,regionName,city,lat,lon,timezone,query"
         "&lang=pt-BR"
      )
  
    resposta = req.faz_requisicao(url)
    
    if resposta is None :    
        return None
    else:
        dados = resposta.json()
    
        if dados.get("status") != "success":
            print(f"Falha na geolocalização: {dados.get('message')}")
            return None
       
        return {
                "pais": dados.get("country"),
                "estado": dados.get("regionName"),
                "cidade": dados.get("city"),
                "latitude": dados.get("lat"),
                "longitude": dados.get("lon"),
                "timezone": dados.get("timezone"),
                "ip": dados.get("query"),
            }


def teste():
    localizacao = geolocation_by_IP()
    if localizacao:
        print(localizacao)
    
    else:
        print("Erro obtendo a localização")
        
#teste()
#teste_open()