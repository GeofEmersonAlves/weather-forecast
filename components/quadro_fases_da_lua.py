# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : quadro_fases_da_lua.py
Autor      : Emerson A. Silva
Data       : Wed Jul 22 14:09:31 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Componente que mostra uma tabela com as fases da lua e a fase da lua atual
  ao selecionar um dia da lista a lua deste dia aparece ao no lutga da lua atual

Histórico:
       22/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
#from components.layout import texto_alinhado 
import services.fase_da_lua as lua
import services.gerar_img_base64 as gerar_img
from services.gerar_img_base64 import imagem_para_base64

BASE_DIR = Path(__file__).parent.parent

@st.cache_data(ttl=120) #guarda a imagem geraco no cache por 2 minutos
def imagem_lua_cache(nome_fase: str,
                      data: str,
                      dia_semana: str,
                      img_lua_base64: str) -> Image.Image:
    
    img_cache = gerar_img.gerar_imagem_fase_lua(nome_fase, data, dia_semana, img_lua_base64)
    
    return img_cache

def gera_df_fases_lua(previsoes :list[dict]) -> pd.DataFrame:    
    dados_exibir=[]
    for dia in previsoes:
        dia_bola = gerar_img.gerar_dia_base64(dia['dia'], dia['dia_semana'])
        nome_fase_lua = dia["fase_lua"]
        if nome_fase_lua is not None:
            
            fase_lua = lua.info_fase_da_lua_com_none(nome_fase_lua)
            path_img_lua = BASE_DIR / fase_lua.get('image')
           
            img_lua = imagem_para_base64(path_img_lua)  # Image.open(path_img_lua)
            
            dados ={'dia': dia['dia'],
                    'dia_semana': dia['dia_semana'],
                    'dia_bola': dia_bola,
                    'img_lua': img_lua,
                    'Descrição': fase_lua['nome']
                }
            
            dados_exibir.append(dados)
    df_faseslua = pd.DataFrame(dados_exibir).set_index("dia")
    return df_faseslua

def muda_img_fase_lua():
    id_lua_selec = st.session_state.lua_select["selection"]['rows']
    
    if len(id_lua_selec) == 0:
        idlua = 0
        
    else:
        idlua = id_lua_selec[0]
    
    img_lua_base64 = st.session_state.__df_faseslua__.iloc[idlua]['img_lua']
    nome_fase = st.session_state.__df_faseslua__.iloc[idlua]['Descrição']
    data = st.session_state.__df_faseslua__.index[idlua]
    dia_semana = st.session_state.__df_faseslua__.iloc[idlua]['dia_semana']

    img_lua_com_data = imagem_lua_cache(nome_fase, data, dia_semana, img_lua_base64)
    st.session_state.__img_lua__ =  gerar_img.Image_para_base64(img_lua_com_data)
     
    return

def quadro_fases_da_lua(previsoes :list[dict]):
    df_faseslua = gera_df_fases_lua(previsoes)
    
    if "__df_faseslua__" not in st.session_state:
        st.session_state.__df_faseslua__ = df_faseslua
    
    if "__img_lua__" not in st.session_state:
        img_lua_base64 = st.session_state.__df_faseslua__.iloc[0]['img_lua']
        nome_fase = st.session_state.__df_faseslua__.iloc[0]['Descrição']
        data = st.session_state.__df_faseslua__.index[0]
        dia_semana = st.session_state.__df_faseslua__.iloc[0]['dia_semana']
        
        img_lua_com_data = imagem_lua_cache(nome_fase, data, dia_semana, img_lua_base64)
        st.session_state.__img_lua__ =  gerar_img.Image_para_base64(img_lua_com_data)
        
    
    moon1, moon2 = st.columns(2)
    
    with moon1: #Mostra a tabela com as fases da lua
        st.dataframe(df_faseslua.drop(columns=["dia_semana"]), 
           height  = 490,  
           row_height = 60,
           on_select = muda_img_fase_lua,
           selection_mode = "single-row",
           key = "lua_select",
           column_config={
               "dia_bola": st.column_config.ImageColumn(
                   "Dia",
                   width=20
               ),
               "img_lua": st.column_config.ImageColumn(
                   "Lua",
                   width=20
               ),
           },
           hide_index=True
           )

    with moon2:
        st.image(st.session_state.__img_lua__, width = 420)
        with st.expander("🌒🌓🌔🌕🌖🌗🌘"):
            #GIF animado das fases da lua
            PATH_GIF = BASE_DIR / "assets/images/translacao-da-lua-1.gif"
            gif_base64 = imagem_para_base64(PATH_GIF)
            st.markdown(
                        f'<img src="{gif_base64}" alt="fases da lua gif"><br>',
                        unsafe_allow_html=True,
                    )
            #Imagem com as fases da lua
            PATH_IMG_FASES = BASE_DIR / "assets/images/Fases_da_Lua.png"
            PATH_IMG_FASES = Path(PATH_IMG_FASES)
            img_fases = Image.open(PATH_IMG_FASES)
            st.image(img_fases, width = "stretch")
        
    return


#def tabela_fases_da_lua(previsoes :list[dict]):
#        img_lua = df_faseslua.iloc[0]['img_lua']
#        descr = "Fase da lua hoje: " +df_faseslua.iloc[0]['Descrição']
#        texto_alinhado(descr,alinhamento='center', fontsize=20, color='blue')
#        st.image(img_lua, width = 420)
        
