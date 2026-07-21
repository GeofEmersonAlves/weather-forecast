# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : fase_da_lua.py
Autor      : Emerson A. Silva
Data       : Mon Jul 20 18:04:33 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Faz scrapping em uma pagina que mostra as fases da lua,
        obtem dados da lua via scrapping
      

Histórico:
       20/07/2026 - Inicio 
===============================================================================
"""
import  services.requisicao as req
from bs4 import BeautifulSoup

__URL__ = "https://www.calendarr.com/brasil/lua-hoje/"


__FASES_LUA__ = {
    "Lua Nova": {
        "emoji": "🌑",
        "image": "assets/images/lua_nova.jpg",
    },
    "Lua Crescente": {
        "emoji": "🌒",
        "image": "assets/images/lua_crescente.jpg",
    },
    "Quarto Crescente": {
        "emoji": "🌓",
        "image": "assets/images/lua_quarto_crescente.jpg",
    },
    "Lua Gibosa Crescente": {
        "emoji": "🌔",
        "image": "assets/images/lua_gibosa_crescente.jpg",
    },
    "Lua Cheia": {
        "emoji": "🌕",
        "image": "assets/images/lua_cheia.jpg",
    },
    "Lua Gibosa Minguante": {
        "emoji": "🌖",
        "image": "assets/images/lua_gibosa_minguante.jpg",
    },
    "Quarto Minguante": {
        "emoji": "🌗",
        "image": "assets/images/lua_quarto_minguante.jpg",
    },
    "Lua Minguante": {
        "emoji": "🌘",
        "image": "assets/images/lua_minguante.jpg",
    },
}

def info_fase_da_lua(fase_lua : str ) -> dict:
    return __FASES_LUA__ .get(fase_lua)

def fase_da_lua()->dict:
    resposta = req.faz_requisicao(__URL__ )
    
    soup = BeautifulSoup(resposta.text, "lxml")
    
    txt_fase_lua = soup.select_one(".moon-now").get_text(strip=True)
    
    fase_lua = info_fase_da_lua(txt_fase_lua)
    fase_lua['descricao'] = txt_fase_lua


    return fase_lua
