# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : local.py
Autor      : Emerson A. Silva
Data       : Thu Jul 16 21:21:39 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Para organigar a pagina principa, movi todas as funções que lidam
        com o dicionario Local para cá, criando este componente

Histórico:
       16/07/2026 - Inicio 
===============================================================================
"""
import services.geolocation as geoloc
import components.stream_geolocation as str_geoloc
from geopy.geocoders import Nominatim  # OpenStreetMap(GRATUITO)

direcoes = {
    "N": "Norte",
    "S": "Sul",
    "L": "Leste",
    "O": "Oeste",
    "NE": "Nordeste",
    "SE": "Sudeste",
    "NO": "Noroeste",
    "SO": "Sudoeste",
    "CO": "Centro-Oeste",
}

def pega_local_API(local_api: dict):
    regiao = direcoes.get(local_api['region'], "")
    if len(regiao) > 0 :
        regiao = f"Região {regiao}"
    
    #Para algumas cidades fora do brasil, as vezes vem sem lat e long, neste caso eu pego pelo OpenStreetMap
    lat = local_api["latitude"]
    long = local_api["longitude"]
    
    if lat is None or long is None:
        geolocator = Nominatim(user_agent="meu_app")
        cidade = f"{local_api['city']}-{local_api['uf'], {local_api['country']}}"
        resp = geolocator.geocode(cidade)
        lat = resp.latitude
        long = resp.longitude
        
    local = {"lat": lat,
           "long": long,
           "pais": local_api["country"],
           "estado": local_api["country"],
           "uf": local_api["uf"],
           "cidade": local_api["city"],
           "idcity": local_api["idcity"],
           "litoral": local_api["seaside"],
           "bairro": "",
           "regiao": regiao,
           "obs": "Local selecionado"}
    return local

def local_default():
    return {"lat": "-23.5489",
           "long": "-46.6388",
           "pais": "Brasil",
           "estado": "São Paulo",
           "uf": "SP",
           "cidade": "São Paulo",
           "idcity": 558,
           "litoral": False,
           "bairro": "",
           "regiao": "Região Sudeste",
           "obs": "Local padrão"}

def local_empty():
    return {"lat": None,
           "long": None,
           "pais": None,
           "estado": None,
           "uf": None,
           "cidade": None,
           "idcity": None,
           "litoral": None,
           "bairro": "",
           "regiao": None,
           "obs": "Local vazio"}

#Pega a localizacao do usuario pelo gps ou pelo IP, e retorna 
def retorna_local() -> dict:   
    #Localizaçãoi padrao inicial
    local=local_default()
    
    location = {}
    
    #Tenta pega a localizacao pelo streamlit, se nao conseguir pega pelo IP
    geolocalizacao = str_geoloc.geolocation()
    if geolocalizacao.get('latitude') is not None:
        location = geoloc.geolocation_with_latlon(geolocalizacao.get('latitude'), 
                                                 geolocalizacao.get('longitude'))
        print(location)
        local['lat'] = geolocalizacao.get('latitude')
        local['long'] = geolocalizacao.get('longitude')
        local['obs'] = "Localização atual"
        
    else:
        geolocIP = geoloc.geolocation_by_IP()
        location = geoloc.geolocation_with_latlon(geolocIP.get('latitude'), 
                                                   geolocIP.get('longitude'))
        local['lat'] = geolocIP.get('latitude')
        local['long'] = geolocIP.get('longitude')
        local['obs'] = "Localização aproximada pelo IP"
    
    if location is not None:
        local['pais']  = location.get('address').get('country')
        local['estado'] = location.get('address').get('state')
        local['uf'] = geoloc.sigla_estado(location.get('address').get('state'))
        local['cidade'] = location.get('address').get('city')
        bairro = location.get('address').get('city_district')
        neighbour = location.get('address').get('neighbourhood')
        local['bairro'] = f"{bairro} - {neighbour}"
        local['regiao'] = location.get('address').get('region')
    
    return local