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
       26/07/2026 - Correção dos bugs que apareceram quando o app ficou online+
       27/07/2026 - Atualização das coordenadas do local default, 
                 as corrdenadas  lat, long agora são bem na areia da Prainha Branca 😎 
       29/07/2026 - Correção de um bug quando na funcao pega_local_API(local_api: dict):
       30/07/2026 - Correção de bug, no servico geolocation
===============================================================================
"""
#import streamlit as st
import services.geolocation as geoloc
import components.stream_geolocation as str_geoloc

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

def local_default():
    return {
            "lat": -23.865897,
            "long": -46.135357,
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

def pega_local_API(local_api: dict | None)->dict:
    if local_api:
        regiao = direcoes.get(local_api['region'], "")
        if len(regiao) > 0 :
            regiao = f"Região {regiao}"
        
        #Para algumas cidades fora do brasil, as vezes vem sem lat e long, neste caso eu pego pelo OpenStreetMap
        lat = local_api["latitude"]
        long = local_api["longitude"]
        
        if not (lat and long):
            lat, long = geoloc.geolocation_with_city(local_api["city"], 
                                                     local_api["uf"], 
                                                     local_api["country"])
            
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
        
    else:
        local = local_default()
            
    return local


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
    local = local_atual.copy()

    geolocalizacao = str_geoloc.geolocation()

    latitude = geolocalizacao.get("latitude")
    longitude = geolocalizacao.get("longitude")

    if latitude is not None and longitude is not None:
        local["lat"] = latitude
        local["long"] = longitude
        local["obs"] = "Localização atual"

        location = geoloc.geolocation_with_latlon(latitude,longitude)

        if location is None:
            return local

    else:
        if local_atual == local_default():
            return local_default()

        if local_atual.get("obs") == "Localização atual":
            return local_atual

        geoloc_ip = geoloc.geolocation_by_IP()

        if not geoloc_ip:
            return local_atual

        latitude = geoloc_ip.get("latitude")
        longitude = geoloc_ip.get("longitude")

        if not (latitude and longitude):
            return local_atual

        local["lat"] = latitude
        local["long"] = longitude
        local["obs"] = "Localização aproximada pelo IP"

        location = geoloc.geolocation_with_latlon(latitude, longitude)

        if location is None:
            return local

    address = location.get("address", {})

    estado = address.get("state")
    cidade = (address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("municipality")
              )

    local["pais"] = address.get("country", local.get("pais"))
    local["estado"] = estado or local.get("estado")
    local["uf"] = geoloc.sigla_estado(estado) if estado else local.get("uf")
    local["cidade"] = cidade or local.get("cidade")

    bairro = (address.get("city_district")
              or address.get("suburb")
              or ""
             )

    neighbourhood = address.get("neighbourhood") or ""

    if bairro and neighbourhood and bairro != neighbourhood:
        local["bairro"] = f"{bairro} - {neighbourhood}"
    else:
        local["bairro"] = bairro or neighbourhood

    local["regiao"] = address.get("region",local.get("regiao", ""))

    return local