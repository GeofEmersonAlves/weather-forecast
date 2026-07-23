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


__NOMES_FASES__ = {
    "nova": "Lua Nova",
    "crescente": "Lua Crescente",
    "quarto_crescente": "Quarto Crescente",
    "crescente_gibosa": "Lua Gibosa Crescente",
    "cheia": "Lua Cheia",
    "minguante_gibosa": "Lua Gibosa Minguante",
    "quarto_minguante": "Quarto Minguante",
    "minguante": "Lua Minguante",
}


__FASES_LUA__ = {
    "Lua Nova": {
        "nome" : "Lua nova",
        "emoji": "🌑",
        "image": "assets/images/lua_nova.jpg",
    },
    "Lua Crescente": {
        "nome" : "Lua crescente",
        "emoji": "🌒",
        "image": "assets/images/lua_crescente.jpg",
    },
    "Quarto Crescente": {
        "nome" : "Lua quarto crescente",
        "emoji": "🌓",
        "image": "assets/images/lua_quarto_crescente.jpg",
    },
    "Lua Gibosa Crescente": {
        "nome" : "Lua gibosa crescente",
        "emoji": "🌔",
        "image": "assets/images/lua_gibosa_crescente.jpg",
    },
    "Lua Cheia": {
        "nome" : "Lua cheia",          
        "emoji": "🌕",
        "image": "assets/images/lua_cheia.jpg",
    },
    "Lua Gibosa Minguante": {
        "nome" : "Lua gibosa minguante",
        "emoji": "🌖",
        "image": "assets/images/lua_gibosa_minguante.jpg",
    },
    "Quarto Minguante": {
        "nome" : "Lua quarto minguante",
        "emoji": "🌗",
        "image": "assets/images/lua_quarto_minguante.jpg",
    },
    "Lua Minguante": {
        "nome" : "Lua minguante",
        "emoji": "🌘",
        "image": "assets/images/lua_minguante.jpg",
    },
}

def emojis_fases_da_lua() -> str:
    emojis = ""
    
    for lua in __FASES_LUA__:
       # print(lua)
        emoji_lua = __FASES_LUA__.get(lua)["emoji"]
        emojis += emoji_lua
    
    return emojis

def info_fase_da_lua(fase_lua : str ) -> dict:
    return __FASES_LUA__ .get(fase_lua)

def info_fase_da_lua_com_none(nome: str) -> dict:
    fase_da_lua = __NOMES_FASES__.get(nome)
    info = info_fase_da_lua(fase_da_lua)
    return info

def fase_da_lua()->dict:
    resposta = req.faz_requisicao(__URL__ )
    
    soup = BeautifulSoup(resposta.text, "lxml")
    
    txt_fase_lua = soup.select_one(".moon-now").get_text(strip=True)
    
    fase_lua = info_fase_da_lua(txt_fase_lua)
    fase_lua['descricao'] = txt_fase_lua


    return fase_lua
