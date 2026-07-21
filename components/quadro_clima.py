# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : quadro_clima.py
Autor      : Emerson A. Silva
Data       : Sun Jul 19 22:07:49 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Componente que mostra as informações do clima
      

Histórico:
       19/07/2026 - Inicio 
       21/07/2026 - Criação da função texto_localizacao para reutilização do código
===============================================================================
"""
import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path

from components.layout import texto_alinhado 

def texto_localizacao(texto_inicio: str, local: dict)->str:
    cidade = local["cidade"]
    uf = local["uf"]
    pais = local["pais"]
    
    texto_loc = f"{texto_inicio} {cidade}-{uf} ({pais})"
    if 'None' not in local['bairro']:
        if len(local['bairro']) > 0 :
            texto_loc += f" ({local['bairro']})"
    texto_loc += " :material/location_on:"

    return texto_loc
    
def mostrar_quadro_clima(clima_json : dict):
    salvar =  clima_json.copy()
    salvar['img_clima'] = 'imagem'

    if st.session_state.local_select["obs"] ==  "Local vazio":
        local = st.session_state.user_location
    else:
        local = st.session_state.local_select
    
    texto_local = texto_localizacao("Tempo agora em", local)
    st.write(texto_local)
    
    if clima_json["request"]['type'] is not None:
        img_weather = clima_json['img_clima']
        
        bl1, bl2, bl3, bl4 = st.columns(4)
        with bl2:
            if img_weather is not None:
               st.image(img_weather, width = 70)
        
        with bl3:
            temp = clima_json.get('current').get('temperature')
            texto_alinhado(f"{temp} ºC", alinhamento = 'left', fontsize = 40, color = '#F0622E')
        
       # font_size = 16
       # color ='#D68C1F'
        
        tab_clima = clima_json['tab_clima']
        df_clima = pd.DataFrame([tab_clima])
        st.table(df_clima, border= 'horizontal', hide_header = True )
        
        tab_astro = clima_json['tab_astro']
        st.table(tab_astro, border= 'horizontal' )
        
        moon1, moon2 = st.columns(2)
        with moon1: #Mostra uma imagem da lua na fase atual
            fase_lua = clima_json['fase_lua']
            path_img_lua = Path(fase_lua.get('image'))
            img_lua = Image.open(path_img_lua)
            st.image(img_lua, width = 60)
            st.write(fase_lua.get('descricao'))
            
        with moon2:
            texto_alinhado(f"Fonte: {clima_json['fonte_dados']}", alinhamento = 'right', fontsize = 12)
        
        with st.expander("🌒🌓🌔🌕🌖🌗🌘Fases da Lua"):
            PATH_IMG_FASES = Path("assets/images/Fases_da_Lua.png")
            img_fases = Image.open(PATH_IMG_FASES)
            st.image(img_fases, width = "stretch")
    else:
        st.error("Sem dados para mostrar")