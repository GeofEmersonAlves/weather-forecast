# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : info_clima.py.py
Autor      : Emerson A. Silva
Data       : Mon Jul 20 11:16:36 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Modelo do dicionario padrão de clima

Histórico:
       20/07/2026 - Inicio ......
===============================================================================
"""
from copy import deepcopy

__INFO_CLIMA_PADRAO__ = {
    "request": {
        "type": None,
        "query": None,
        "language": None,
        "unit": None,
    },
    "location": {
        "name": None,
        "country": None,
        "region": None,
        "lat": None,
        "lon": None,
        "timezone_id": None,
        "localtime": None,
        "localtime_epoch": None,
        "utc_offset": None,
    },
    "current": {
        "observation_time": None,
        "temperature": None,
        "weather_code": None,
        "weather_icons": [],
        "weather_descriptions": [],
        "astro": {
            "sunrise": None,
            "sunset": None,
            "moonrise": None,
            "moonset": None,
            "moon_phase": None,
            "moon_illumination": None,
        },
        "air_quality": {
            "co": None,
            "no2": None,
            "o3": None,
            "so2": None,
            "pm2_5": None,
            "pm10": None,
            "us-epa-index": None,
            "gb-defra-index": None,
        },
        "wind_speed": None,
        "wind_degree": None,
        "wind_dir": None,
        "pressure": None,
        "precip": None,
        "humidity": None,
        "cloudcover": None,
        "feelslike": None,
        "uv_index": None,
        "visibility": None,
        "is_day": None,
    },
    "img_clima": None,
    "tab_clima": [],
    "tab_astro": [],
    "fonte_dados": None,
    "fase_lua": {
        "descricao": None,
        "emoji": None,
        "image": None,
    },
}

def novo_info_clima() -> dict:
    return deepcopy(__INFO_CLIMA_PADRAO__)