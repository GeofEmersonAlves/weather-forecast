# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : city_options.py
Autor      : Emerson A. Silva
Data       : Sun Jul 19 18:18:51 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Componente que mostra as opcoes de cidades para selecionar uma
      
Histórico:
       19/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
import re # para usar expressão regular (Regex) 
from components.local import pega_local_API
import state.estado_app as estado

def escolheu_cidade():
    # Regex para capturar Cidade, UF e Pais
    expRegex = r"(.+?)-([A-Z]{2})\s*\((.+?)\)"

    match = re.match(expRegex, st.session_state._cidade_selec_)

    if match:
        cidade = match.group(1).strip()
        uf = match.group(2).strip()
        pais = match.group(3).strip()
        
        local_select = next((local for local in st.session_state.resp_busca_cidades[0]["response"]["data"] 
                             if local.get("city") == cidade 
                             and local.get("uf") == uf 
                             and local.get("country") == pais), 
                            None
                        )
        
        local = pega_local_API(local_select)
        estado.alterar_local_select(local)
    
    return

def seleciona_uma_cidade():
    resp_cidades = st.session_state.resp_busca_cidades
    lst_cids = resp_cidades[0]["response"]["data"]
    cidades = [f"{cid['city']}-{cid['uf']} ({cid['country']})" for cid in lst_cids]
    
    st.segmented_control("Escolha uma:", 
                            cidades, 
                            required = True,
                            key = "_cidade_selec_",
                            on_change = escolheu_cidade,
                            selection_mode = "single")

    return