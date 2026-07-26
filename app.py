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
       25/07/2026 - Fim da versao 1.0.0
===============================================================================
"""
#IMPORTAÇÃO DAS BIBLIOTECAS E FRAMEWORKS
import streamlit as st
from PIL import Image
from state.estado_app import inicializar_estado_app

LOGO256_X_256 = "assets/icons/weather_forecast_icon256px_256px.png"
icone = Image.open(LOGO256_X_256)
st.session_state._icone_app_ = icone

#print(st.__version__)  #Para ver a versão do streamlit instalada

#Inicializa todas as variáveis de estado da sessão
inicializar_estado_app()

#Definiçã das páginas para navegação
weather_page = st.Page("pages/weather_page.py", 
                       title = "Weather Forecast",
                       icon =  "🌤️",
                       default=True )
sobre_page = st.Page(
            "pages/sobre_page.py",
            title="Sobre",
            icon="ℹ️",
        )

pg = st.navigation([weather_page,sobre_page], position='top')


pg.run()