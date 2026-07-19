# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : weather_api.py
Autor      : Emerson
Data       : Thu Jul 16 22:53:26 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Faz todo o tratamento com a api de Clima
      

Histórico:
       16/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv   #Para ler o arquivo .env
import os
from services.requisicao import faz_requisicao

load_dotenv()

Base_URL_API = "http://api.weatherstack.com/"
ws_token = os.getenv("WEATHERSTACK_TOKEN")

WEATHER_CODES = {
    113: "Céu limpo",
    116: "Parcialmente nublado",
    119: "Nublado",
    122: "Encoberto",
    143: "Névoa",

    176: "Pancadas de chuva próximas",
    179: "Pancadas de neve próximas",
    182: "Pancadas de chuva congelante próximas",
    185: "Garoa congelante próxima",

    200: "Trovoadas nas proximidades",

    227: "Nevasca com vento",
    230: "Nevasca intensa",

    248: "Neblina",
    260: "Neblina congelante",

    263: "Garoa fraca isolada",
    266: "Garoa fraca",

    281: "Garoa congelante",
    284: "Garoa congelante forte",

    293: "Chuva fraca isolada",
    296: "Chuva fraca",
    299: "Períodos de chuva moderada",
    302: "Chuva moderada",
    305: "Períodos de chuva forte",
    308: "Chuva forte",

    311: "Chuva congelante fraca",
    314: "Chuva congelante moderada ou forte",

    317: "Aguanieve fraca",
    320: "Aguanieve moderada ou forte",

    323: "Neve fraca isolada",
    326: "Neve fraca",
    329: "Neve moderada isolada",
    332: "Neve moderada",
    335: "Neve forte isolada",
    338: "Neve forte",

    350: "Granizo pequeno",

    353: "Pancadas leves de chuva",
    356: "Pancadas moderadas ou fortes de chuva",
    359: "Pancadas torrenciais de chuva",

    362: "Pancadas leves de aguanieve",
    365: "Pancadas moderadas ou fortes de aguanieve",

    368: "Pancadas leves de neve",
    371: "Pancadas moderadas ou fortes de neve",

    374: "Pancadas leves de granizo",
    377: "Pancadas moderadas ou fortes de granizo",

    386: "Chuva fraca com trovoadas",
    389: "Chuva moderada ou forte com trovoadas",

    392: "Neve fraca com trovoadas",
    395: "Neve moderada ou forte com trovoadas",
}

WEATHER_CODES_EXTRA = {
    125: "Névoa seca",
    146: "Fumaça",
    149: "Névoa de fumaça",
    152: "Smog",
}

WEATHER_CODES.update(WEATHER_CODES_EXTRA)

WEATHER_INFO = {
    113: {"descricao": "Céu limpo", "icone": "clear_day", "emoji": "☀️", "categoria": "clear"},
    116: {"descricao": "Parcialmente nublado", "icone": "partly_cloudy", "emoji": "⛅", "categoria": "clouds"},
    119: {"descricao": "Nublado", "icone": "cloudy", "emoji": "☁️", "categoria": "clouds"},
    122: {"descricao": "Encoberto", "icone": "overcast", "emoji": "☁️", "categoria": "clouds"},
    143: {"descricao": "Névoa", "icone": "mist", "emoji": "🌫️", "categoria": "fog"},

    176: {"descricao": "Pancadas de chuva próximas", "icone": "light_rain", "emoji": "🌦️", "categoria": "rain"},
    179: {"descricao": "Pancadas de neve próximas", "icone": "snow", "emoji": "🌨️", "categoria": "snow"},
    182: {"descricao": "Chuva congelante próxima", "icone": "sleet", "emoji": "🌨️", "categoria": "sleet"},
    185: {"descricao": "Garoa congelante", "icone": "freezing_drizzle", "emoji": "🧊", "categoria": "ice"},

    200: {"descricao": "Trovoadas próximas", "icone": "thunder", "emoji": "⛈️", "categoria": "storm"},

    227: {"descricao": "Nevasca com vento", "icone": "blizzard", "emoji": "🌨️", "categoria": "snow"},
    230: {"descricao": "Nevasca intensa", "icone": "blizzard", "emoji": "❄️", "categoria": "snow"},

    248: {"descricao": "Neblina", "icone": "fog", "emoji": "🌫️", "categoria": "fog"},
    260: {"descricao": "Neblina congelante", "icone": "freezing_fog", "emoji": "🌫️", "categoria": "fog"},

    263: {"descricao": "Garoa fraca isolada", "icone": "drizzle", "emoji": "🌦️", "categoria": "drizzle"},
    266: {"descricao": "Garoa fraca", "icone": "drizzle", "emoji": "🌦️", "categoria": "drizzle"},

    281: {"descricao": "Garoa congelante", "icone": "freezing_drizzle", "emoji": "🧊", "categoria": "ice"},
    284: {"descricao": "Garoa congelante forte", "icone": "freezing_drizzle", "emoji": "🧊", "categoria": "ice"},

    293: {"descricao": "Chuva fraca isolada", "icone": "light_rain", "emoji": "🌦️", "categoria": "rain"},
    296: {"descricao": "Chuva fraca", "icone": "light_rain", "emoji": "🌧️", "categoria": "rain"},
    299: {"descricao": "Períodos de chuva moderada", "icone": "moderate_rain", "emoji": "🌧️", "categoria": "rain"},
    302: {"descricao": "Chuva moderada", "icone": "moderate_rain", "emoji": "🌧️", "categoria": "rain"},
    305: {"descricao": "Períodos de chuva forte", "icone": "heavy_rain", "emoji": "🌧️", "categoria": "rain"},
    308: {"descricao": "Chuva forte", "icone": "heavy_rain", "emoji": "🌧️", "categoria": "rain"},

    311: {"descricao": "Chuva congelante fraca", "icone": "freezing_rain", "emoji": "🧊", "categoria": "ice"},
    314: {"descricao": "Chuva congelante forte", "icone": "freezing_rain", "emoji": "🧊", "categoria": "ice"},

    317: {"descricao": "Aguanieve fraca", "icone": "sleet", "emoji": "🌨️", "categoria": "sleet"},
    320: {"descricao": "Aguanieve moderada", "icone": "sleet", "emoji": "🌨️", "categoria": "sleet"},

    323: {"descricao": "Neve fraca isolada", "icone": "light_snow", "emoji": "🌨️", "categoria": "snow"},
    326: {"descricao": "Neve fraca", "icone": "light_snow", "emoji": "🌨️", "categoria": "snow"},
    329: {"descricao": "Neve moderada isolada", "icone": "snow", "emoji": "🌨️", "categoria": "snow"},
    332: {"descricao": "Neve moderada", "icone": "snow", "emoji": "🌨️", "categoria": "snow"},
    335: {"descricao": "Neve forte isolada", "icone": "heavy_snow", "emoji": "❄️", "categoria": "snow"},
    338: {"descricao": "Neve forte", "icone": "heavy_snow", "emoji": "❄️", "categoria": "snow"},

    350: {"descricao": "Granizo pequeno", "icone": "hail", "emoji": "🧊", "categoria": "hail"},

    353: {"descricao": "Pancadas leves de chuva", "icone": "rain_showers", "emoji": "🌦️", "categoria": "showers"},
    356: {"descricao": "Pancadas moderadas de chuva", "icone": "rain_showers", "emoji": "🌧️", "categoria": "showers"},
    359: {"descricao": "Pancadas torrenciais", "icone": "heavy_showers", "emoji": "🌧️", "categoria": "showers"},

    362: {"descricao": "Pancadas leves de aguanieve", "icone": "sleet_showers", "emoji": "🌨️", "categoria": "showers"},
    365: {"descricao": "Pancadas fortes de aguanieve", "icone": "sleet_showers", "emoji": "🌨️", "categoria": "showers"},

    368: {"descricao": "Pancadas leves de neve", "icone": "snow_showers", "emoji": "🌨️", "categoria": "showers"},
    371: {"descricao": "Pancadas fortes de neve", "icone": "snow_showers", "emoji": "❄️", "categoria": "showers"},

    374: {"descricao": "Pancadas leves de granizo", "icone": "hail_showers", "emoji": "🧊", "categoria": "hail"},
    377: {"descricao": "Pancadas fortes de granizo", "icone": "hail_showers", "emoji": "🧊", "categoria": "hail"},

    386: {"descricao": "Chuva fraca com trovoadas", "icone": "thunder_rain", "emoji": "⛈️", "categoria": "storm"},
    389: {"descricao": "Chuva forte com trovoadas", "icone": "thunder_rain", "emoji": "⛈️", "categoria": "storm"},
    392: {"descricao": "Neve fraca com trovoadas", "icone": "thunder_snow", "emoji": "⛈️", "categoria": "storm"},
    395: {"descricao": "Neve forte com trovoadas", "icone": "thunder_snow", "emoji": "⛈️", "categoria": "storm"},

    # Códigos extras observados na API
    125: {"descricao": "Névoa seca", "icone": "haze", "emoji": "🌫️", "categoria": "haze"},
    146: {"descricao": "Fumaça", "icone": "smoke", "emoji": "💨", "categoria": "smoke"},
    149: {"descricao": "Névoa de fumaça", "icone": "smoky_haze", "emoji": "🌫️", "categoria": "smoke"},
    152: {"descricao": "Smog", "icone": "smog", "emoji": "🏭", "categoria": "smoke"},
}

MOON_PHASES = {
    "New Moon": {
        "descricao": "Lua Nova",
        "emoji": "🌑",
        "image": "assets/images/lua_nova.jpg",
    },
    "Waxing Crescent": {
        "descricao": "Lua Crescente",
        "emoji": "🌒",
        "image": "assets/images/lua_crescente.jpg",
    },
    "First Quarter": {
        "descricao": "Quarto Crescente",
        "emoji": "🌓",
        "image": "assets/images/lua_quarto_crescente.jpg",
    },
    "Waxing Gibbous": {
        "descricao": "Lua Gibosa Crescente",
        "emoji": "🌔",
        "image": "assets/images/lua_gibosa_crescente.jpg ",
    },
    "Full Moon": {
        "descricao": "Lua Cheia",
        "emoji": "🌕",
        "image": "assets/images/lua_cheia.jpg",
    },
    "Waning Gibbous": {
        "descricao": "Lua Gibosa Minguante",
        "emoji": "🌖",
        "image": "assets/images/lua_gibosa_minguante.jpg",
    },
    "Last Quarter": {
        "descricao": "Quarto Minguante",
        "emoji": "🌗",
        "image": "assets/images/lua_quarto_minguante.jpg",
    },
    "Waning Crescent": {
        "descricao": "Lua Minguante",
        "emoji": "🌘",
        "image": "assets/images/lua_minguante.jpg",
    },
}

WIND_DIRECTION = {
    "N": {
        "emoji": "⬆️",
        "descricao": "Norte",
    },
    "NNE": {
        "emoji": "⬆️↗️",
        "descricao": "Norte-Nordeste",
    },
    "NE": {
        "emoji": "↗️",
        "descricao": "Nordeste",
    },
    "ENE": {
        "emoji": "➡️↗️",
        "descricao": "Leste-Nordeste",
    },
    "E": {
        "emoji": "➡️",
        "descricao": "Leste",
    },
    "ESE": {
        "emoji": "➡️↘️",
        "descricao": "Leste-Sudeste",
    },
    "SE": {
        "emoji": "↘️",
        "descricao": "Sudeste",
    },
    "SSE": {
        "emoji": "⬇️↘️",
        "descricao": "Sul-Sudeste",
    },
    "S": {
        "emoji": "⬇️",
        "descricao": "Sul",
    },
    "SSW": {
        "emoji": "⬇️↙️",
        "descricao": "Sul-Sudoeste",
    },
    "SW": {
        "emoji": "↙️",
        "descricao": "Sudoeste",
    },
    "WSW": {
        "emoji": "⬅️↙️",
        "descricao": "Oeste-Sudoeste",
    },
    "W": {
        "emoji": "⬅️",
        "descricao": "Oeste",
    },
    "WNW": {
        "emoji": "⬅️↖️",
        "descricao": "Oeste-Noroeste",
    },
    "NW": {
        "emoji": "↖️",
        "descricao": "Noroeste",
    },
    "NNW": {
        "emoji": "⬆️↖️",
        "descricao": "Norte-Noroeste",
    },
}

ASTRO_EVENTS = {
    "sunrise": {
        "emoji": "🌅⬆️",
        "descricao": "Nascer do Sol",
    },
    "sunset": {
        "emoji": "🌇⬇️",
        "descricao": "Pôr do Sol",
    },
    "moonrise": {
        "emoji": "🌙⬆️",
        "descricao": "Nascer da Lua",
    },
    "moonset": {
        "emoji": "🌙⬇️",
        "descricao": "Pôr da Lua",
    },
}

def fonte_dados() -> str:
    return Base_URL_API

def classificar_indice_uv(indice_uv: float) -> str:
  if indice_uv <= 2:
      return "🟢 Baixo"
  elif indice_uv <= 5:
        return "🟡 Moderado"
  elif indice_uv <= 7:
        return "🟠 Alto"
  elif indice_uv <= 10:
        return "🔴 Muito Alto"
  else:
        return "🟣 Extremo"
    
    
def astro_evento(evento_astro : str)-> str:
    return f"{ASTRO_EVENTS.get(evento_astro).get('emoji')}{ASTRO_EVENTS.get(evento_astro).get('descricao')}"

def direcao_vento_emoji(direcao : str)-> str:
    return WIND_DIRECTION.get(direcao).get('emoji')

def direcao_vento_descricao(direcao : str)-> str:
    return WIND_DIRECTION.get(direcao).get('descricao')
    
def weather_icon(json_weather : dict) -> Image.Image | None: 
    url_icon = json_weather.get('current').get('weather_icons')[0]
    resp = faz_requisicao(
       url_icon,
       use_raise=True
   )
    if resp is None:
       return None

    img_weather = Image.open(BytesIO(resp.content))
  
    return img_weather


def fase_da_lua(moon_phase : str ) -> dict:
    return MOON_PHASES.get(moon_phase)
    
def clima_descricao(weather_code : int ) -> dict:
    return WEATHER_INFO.get(weather_code)

@st.cache_data(show_spinner="⏳ Carregando condicções climaticas . . .",  ttl = 1800)
def clima_agora(lat : str, long: str) -> dict:
    text_request =f"{Base_URL_API}current?access_key={ws_token}&query={lat},{long}"
           
    resposta = faz_requisicao(text_request, use_raise = False)
    
    if resposta is None:
        return None

    dados = resposta.json()

    if not dados.get("success", True):
        return None
    
    return dados