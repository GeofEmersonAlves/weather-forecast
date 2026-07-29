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
       26/07/2026 - Correção dos bugs que apareceram quando o app ficou online
       26/07/2026 - Oficializando a versão 1.0.2 como a versão mais estavél e online
       27/07/2026 - Correção do problema dos timezone nos horários
       27/07/2026 - Oficializando a versão 1.0.3
       29/07/2026 - Correção de um bug no componente local
       29/07/2026 - Oficializando a versão 1.0.4
===============================================================================
"""
#IMPORTAÇÃO DAS BIBLIOTECAS E FRAMEWORKS
import streamlit as st
from PIL import Image
from pathlib import Path
from state.estado_app import inicializar_estado_app

#ROOT = Path(__file__).resolve().parent.parent   # ajuste conforme sua estrutura

LOGO256_X_256 = Path("assets/icons/weather_forecast_icon256px_256px.png")
                                             
icone = Image.open(LOGO256_X_256)
st.session_state._icone_app_ = icone
st.session_state._app_version = "Versão 1.0.4 • Julho/2026"

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