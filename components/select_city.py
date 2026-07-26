# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : select_city.py
Autor      : Emerson
Data       : Sat Jul 18 12:01:47 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    Componente seletor de cidades com autocomplete real a partir da quarta letra digitada
    chama o serviço busca_cidades() para encontrar a lista de cidades recebidas

Histórico:
       18/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
from  services.busca_cidades import buscar_cidades

def find_cities():
    #st.write(f"Digitado:{texto} {len(texto.strip())}")
    letras_cidade = st.session_state.__letras_cidade__
    
    if letras_cidade is not None:
        resp_cidades =  buscar_cidades(letras_cidade)
        st.session_state.resp_busca_cidades = resp_cidades.copy()

def find_cities_weather() -> bool:
    
    st.text_input("🔍Busque por cidades...",
                           placeholder="Digite no mínimo 4 letras...",
                           key = "__letras_cidade__",
                           on_change = find_cities,
                           icon = ":material/search:"
                           )

    return (st.session_state.resp_busca_cidades[0]["type"] != "vazia")

