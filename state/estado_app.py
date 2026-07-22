# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : estado_app.py
Autor      : Emerson A. Silva
Data       : Thu Jul 16 21:52:56 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    Controla as variaveis de estado da aplicação
      

Histórico:
       16/07/2026 - Inicio
===============================================================================
"""

import streamlit as st
from components.local import local_default
from services.busca_cidades import lst_empty_resp
from models.local_vazio import local_empty

def inicializar_estado_app():
    if "user_location" not in st.session_state:
        st.session_state.user_location = local_default()
    
    if "local_select" not in st.session_state:
        st.session_state.local_select = local_empty()
    
    if "resp_busca_cidades" not in st.session_state:
        st.session_state.resp_busca_cidades = lst_empty_resp()
    
def alterar_resp_busca_cidades(resp_busca_cidades : list[dict[str, object]]):
    st.session_state.resp_busca_cidades = resp_busca_cidades.copy()

def alterar_local_select(local_select : dict):
    st.session_state.local_select = local_select.copy()

def alterar_user_location(local : dict):
    st.session_state.user_location =  local
    
def restaurar_local_select():
    alterar_local_select(local_empty())
    
def restaura_estado_inical():
    alterar_user_location(local_default())
    alterar_local_select(local_empty())
    alterar_resp_busca_cidades(lst_empty_resp())
    