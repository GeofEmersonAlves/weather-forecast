# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : get_tokens.py
Autor      : Emerson A. Silvca
Data       : Sat Jul 25 16:42:26 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição: Serviço responsável por guardar e entregar os tokens da aplicação
        
Histórico:
       25/07/2026 - Inicio 
===============================================================================
"""
import os
import streamlit as st
from dotenv import load_dotenv   #Para ler o arquivo .env

load_dotenv()

#Configura qual dos dois tokens possíveis está funcional
def set_weatherstack_token_usar(weatherstack_token: str):
    st.session_state.weatherstack_token_usar = weatherstack_token
    return

def get_weatherstack_token_usar() -> str | None:
    if "weatherstack_token_usar" in st.session_state:
        return st.session_state.weatherstack_token_usar
    
    else:
        return None


#Retorna o token 1
def get_weatherstack_token1() -> str:
    weatherstack_token1 = (st.secrets.get("WEATHERSTACK_TOKEN1") or
                          os.getenv("WEATHERSTACK_TOKEN1")                              ) 
    return weatherstack_token1

#Retorna o token 2
def get_weatherstack_token2() -> str:
    weatherstack_token2 = (st.secrets.get("WEATHERSTACK_TOKEN2") or
                          os.getenv("WEATHERSTACK_TOKEN2")                              ) 
    return weatherstack_token2


