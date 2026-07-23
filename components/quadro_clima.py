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
       23/07/2026 - Alteracao para salvar o info_clima na session com a intenção de 
                  melhorar a performance do gerador de relatório Excel
===============================================================================
"""
import streamlit as st
import pandas as pd
from components.layout import texto_alinhado 

def texto_localizacao(texto_inicio: str, local: dict, tem_material_icon : bool = True)->str:
    cidade = local["cidade"]
    uf = local["uf"]
    pais = local["pais"]
    
    texto_loc = f"{texto_inicio} {cidade}-{uf} ({pais})"
    if 'None' not in local['bairro']:
        if len(local['bairro']) > 0 :
            texto_loc += f" ({local['bairro']})"
            
    if tem_material_icon:
        texto_loc += " :material/location_on:"

    return texto_loc
    
def mostrar_quadro_clima(clima_json : dict):
    #salvar =  clima_json.copy()
    #salvar['img_clima'] = 'imagem'

    if st.session_state.local_select["obs"] ==  "Local vazio":
        local = st.session_state.user_location
    else:
        local = st.session_state.local_select
    
    #Salva o info_clima na session para melhorar a performance do gerador de relatório Excel
    if "_info_clima_" not in st.session_state: 
        st.session_state._info_clima_ = clima_json
        
    texto_local = texto_localizacao("Tempo agora em", local)
       
    st.write(texto_local)
    if clima_json["request"]['type'] is not None:
        img_weather = clima_json['img_clima'] #aqui tem somente a url da imagem
       
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
        
        fase_lua = clima_json['fase_lua']
        emoji_lua = fase_lua.get('emoji')
        desc_lua = fase_lua.get('descricao')
        texto_fase_lua = f"{emoji_lua} {desc_lua}"
        st.write(texto_fase_lua)
        
    else:
        st.error("Sem dados para mostrar")