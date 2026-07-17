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

from services.local import local_default

def inicializar_estado_app():
    if "user_location" not in st.session_state:
        st.session_state.user_location = local_default()
        
def aplicar_estado_app(local : dict):
    st.session_state.user_location =  local

def restaura_estado_inical():
    aplicar_estado_app(local_default())
    