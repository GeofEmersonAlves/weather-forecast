# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : stream_geolocation.py
Autor      : Emerson A. Silva
Data       : Thu Jul 16 18:34:10 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    Componente que retorna a geolocalização pelo streamlit se o usuario autorizar no navegador
      

Histórico:
       16/07/2026 - Inicio
===============================================================================
"""
import streamlit as st
from streamlit_geolocation import streamlit_geolocation

def geolocation() -> dict :
    geocol1, geocol2, geocol3 = st.columns([1,4,1])
    with geocol1:
        localizacao = streamlit_geolocation()
    
    with geocol2:
        if localizacao.get("latitude") is  None:
            st.warning("Pressione o botão para acessar sua localização.")
        
        else:
            st.success("Localização obtida com Sucesso!")
    
    return localizacao