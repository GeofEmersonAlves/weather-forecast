# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : app.py
Autor      : Emerson Alves da Silva
Data       : 
Versão     : 1.0
Python     :  Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
         Aplicação desenvolvida em **Python** e **Streamlit** para consulta 
      das condições meteorológicas e previsão do tempo em cidades brasileiras.
      

Histórico:
       16/07/2026 - Inicio do projeto
/===============================================================================
"""

#IMPORTAÇÃO DAS BIBLIOTECAS E FRAMEWORKS
import streamlit as st
from state.estado_app import inicializar_estado_app

#print(st.__version__)  #Para ver a versão do streamlit instalada

#Inicializa todas as variáveis de estado da sessão
inicializar_estado_app()

#Definiçã das páginas para navegação
weather_page = st.Page("pages/weather_page.py", 
                       title = "Clima agora!",
                       default=True )

test_page = st.Page("pages/testes.py")

pg = st.navigation([weather_page, test_page], position='top')


pg.run()