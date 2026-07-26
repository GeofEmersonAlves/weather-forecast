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
       24/07/2026 - Para facilitar o relatório e não repedir codigo foi incluido  user_loc_formatado
       26/07/2026 - Correção dos bugs que apareceram quando o app ficou online
===============================================================================
"""
#import streamlit as st
import services.geolocation as geoloc
import components.stream_geolocation as str_geoloc
from geopy.geocoders import Nominatim  # OpenStreetMap(GRATUITO)
from models.local_vazio import local_empty

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
    return {
            "lat": -23.87072186750067,
            "long": -46.13784252958647,
            "pais": "Brasil",
            "estado": "Brasil",
            "uf": "SP",
            "cidade": "Guarujá",
            "idcity": 798,
            "litoral": True,
            "bairro": "APA da Serra do Guararu",
            "regiao": "Reigião sudeste",
            "obs": "Local padrão - 🏖️🩴 Prainha Branca 🌊🏝️"
        }


def local_formatado(local: dict) -> dict:
    txt_loc = f"🌍 {local['cidade']}/{local['uf']} - {local['regiao']} do {local['pais']}"
    txt_coord = f"🌐 ({local['lat']}, {local['long']})"
    txt_origem_coord = f"📍{local['obs']}"
    
    local_dict = {"local" : txt_loc,
                  "coordenadas": txt_coord,
                  "origem_coordenadas":txt_origem_coord}
    
    return local_dict

#Pega a localizacao do usuario pelo gps ou pelo IP, e retorna 
def retorna_local(local_atual: dict) -> dict:   
    local = local_empty()
    
    location = {}
     #Tenta pega a localizacao pelo streamlit
    geolocalizacao = str_geoloc.geolocation()
    if geolocalizacao.get('latitude') is not None:
        location = geoloc.geolocation_with_latlon(geolocalizacao.get('latitude'), 
                                                 geolocalizacao.get('longitude'))
        #print(location)
        local['lat'] = geolocalizacao.get('latitude')
        local['long'] = geolocalizacao.get('longitude')
        local['obs'] = "Localização atual"
        
    else: #Se não conseguir pega pelo IP, se o local nao for o default
        if local_atual == local_default():
            return  local_default()
        
        if local_atual['obs'] =="Localização atual":
            return local_atual
        
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
    
        if local['uf'] == None or local['cidade'] == None:
            return local_default()
    
    return local