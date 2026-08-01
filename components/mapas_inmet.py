# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : mapas_inmet.py
Autor      : Emerson Alves da Silva
Data       : Sat Aug  1 17:03:11 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Exibe os dados recebidos do INMET na forma de uma tabela com os mapas,
    caso não receba os mapas exibe uma mensgem de aviso.
      

Histórico:
       01/08/2026 - Inicio
===============================================================================
"""
import streamlit as st
import pandas as pd

def mostra_mapas_immet(mapas_immet: list[dict]):
    if len(mapas_immet) == 0:
        st.info("O INMET não retornou os mapas de precipitação!")
    
    else:
        df = pd.DataFrame(mapas_immet)
        df = df["base64"]
        st.dataframe(df, 
                     height  = 370 ,  
                     row_height = 350,
                     hide_index = True,
                     column_config={"base64": st.column_config.ImageColumn("Mapas de Precipitação", 
                                                                           width="medium")})
        