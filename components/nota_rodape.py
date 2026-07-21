# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : nota_rodape.py
Autor      : Emerson A. Silva
Data       : Tue Jul 21 18:59:57 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Insere uma nota no rodapé da página com as minhas informações
      

Histórico:
       21/07/2026 - Inicio 
===============================================================================
"""

import streamlit as st

def nota_de_rodape():
    st.divider()

    st.markdown("""
    <div style="text-align:center; line-height:1.8">
    <b>Weather Forecast</b>
    Desenvolvido por <b>Emerson Alves da Silva</b>
    🐍 Python 🎈 Streamlit 📊 Plotly 🌐 Requests 🥣 BeautifulSoup ☁️ WeatherStack 🌧️ INMET
    <br>
    <a href="https://github.com/GeofEmersonAlves" target="_blank">🔗GitHub</a> |
    <a href="https://www.linkedin.com/in/emersonalvesdasilva/" target="_blank">🔗LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)
 
    return