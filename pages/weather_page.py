# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : weather_page.py
Autor      : Emerson Alves da Silva
Data       : 
Versão     : 1.0
Python     :  Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
         Página princial do app Weather Forecast.
      

Histórico:
       16/07/2026 - Inicio do projeto
/===============================================================================
"""

#IMPORTAÇÃO DAS BIBLIOTECAS E FRAMEWORKS
import streamlit as st
from PIL import Image
import pandas as pd
from pathlib import Path

#Bibliotecas do projeto
from components.layout import  data_por_extenso, texto_alinhado 
from components.select_city import select_city_weather
from utils.datas import hoje
from services.local import retorna_local
import services.weather_api as wt_api 
from state.estado_app import alterar_user_location
from services.imet import mapa_precipitacao


__LOGO50_X_50 = "assets/icons/weather_50px_50px.png"
__LOGO100_X_100 = "assets/icons/weather_100px_100px.png"
icone = Image.open(__LOGO50_X_50)

st.set_page_config("Weather´s page: Clima e previsão do tempo",
                   page_icon=icone,
                   layout="wide",
                   initial_sidebar_state="expanded"
                    )

st.logo(__LOGO100_X_100, icon_image = __LOGO50_X_50)

data_hoje = hoje()

with st.sidebar: 
    alterar_user_location(retorna_local())
    local = st.session_state.user_location
    select_city_weather(f"{local['cidade']}-{local['uf']}")
    st.write(st.session_state.__letras_cidade__)
    #st.subheader("📍 Sua localização")

clima_api_json = wt_api.clima_agora(local['lat'], local['long'])

col1, col2, col3 = st.columns(3)
with col1:
    texto_topo = f"Tempo agora em {local['cidade']}/{local['uf']}"
    if "None" not in local['bairro']:
        texto_topo += f" ({local['bairro']})"
    
    texto_topo += " :material/location_on:"
    
    st.write(texto_topo)
    
    #texto_alinhado(texto_topo, alinhamento = 'center', fontsize = 20, color = '#FFFFFF')
    url_img_clima = clima_api_json.get('current').get('weather_icons')[0]
    
    img_weather = wt_api.weather_icon(clima_api_json)
    
    bl1, bl2, bl3, bl4 = st.columns(4)
    with bl2:
        if img_weather is not None:
           st.image(img_weather, width = 70)
    
    with bl3:
        temp = clima_api_json.get('current').get('temperature')
        texto_alinhado(f"{temp} ºC", alinhamento = 'left', fontsize = 40, color = '#FFFFFF')
    
    font_size = 16
    color ='#D68C1F'
    
    descr = wt_api.clima_descricao(int(clima_api_json.get("current").get("weather_code")))
    texto_descricao = f"{descr.get('emoji')} {descr.get('descricao')}"
    
    vento_veloc = clima_api_json.get('current').get('wind_speed')
    vento_dir = clima_api_json.get('current').get('wind_dir')
    vento_dir_emoji = wt_api.direcao_vento_emoji(vento_dir)
    texto_vento = f"💨 Vento {vento_veloc} km/h {vento_dir_emoji}{vento_dir}"
    
    umidade =  clima_api_json.get('current').get('humidity')
    texto_umidade = f"💧 Umidade {umidade} %"
    
    sens  = clima_api_json.get('current').get('feelslike')
    texto_sensacao = f"🌡️ Sensação {sens} ºC"
    
    tab_clima=[texto_descricao, texto_vento, texto_umidade, texto_sensacao]
    df_clima = pd.DataFrame([tab_clima])
    st.table(df_clima, border= 'horizontal', hide_header = True )
    
    txt_sol_up_h = "🧭 "+clima_api_json.get('current').get('astro').get('sunrise')
    txt_sol_up = wt_api.astro_evento('sunrise')
    
    txt_sol_down_h = "🧭 "+clima_api_json.get('current').get('astro').get('sunset')
    txt_sol_down = wt_api.astro_evento('sunset')
    
    txt_moon_up_h = "🧭 "+clima_api_json.get('current').get('astro').get('moonrise')
    txt_moon_up = wt_api.astro_evento('moonrise')
    
    txt_moon_down_h = "🧭 "+clima_api_json.get('current').get('astro').get('moonset')
    txt_moon_down = wt_api.astro_evento('moonset')
    
    txt_precipita = "🌧️ Precipitação"
    txt_preci_valor = f"💧 {clima_api_json.get('current').get('precip')} mm"
    
    txt_uv = "☀️ Índice UV"
    vlr_uv = int(clima_api_json.get('current').get('uv_index'))
    txt_uv_desc = f"{wt_api.classificar_indice_uv(vlr_uv)} ({vlr_uv})"
    
    tab_astro = [
            [txt_sol_up, txt_sol_up_h ],
            [txt_sol_down, txt_sol_down_h],
            [txt_moon_up, txt_moon_up_h],
            [txt_moon_down, txt_moon_down_h],
            [txt_precipita, txt_preci_valor],
            [txt_uv, txt_uv_desc]
        ]
    
    st.table(tab_astro, border= 'horizontal' )
    #texto_alinhado(txt_sol_up, alinhamento = 'right', fontsize = font_size, color = color)    
    
    moon1, moon2 = st.columns(2)
    with moon1: #Mostra uma imagem da lua na fase atual
        fase_lua = wt_api.fase_da_lua(clima_api_json.get("current").get("astro").get("moon_phase"))
        path_img_lua = Path(fase_lua.get('image'))
        img_lua = Image.open(path_img_lua)
        st.image(img_lua, width = 60)
        st.write(fase_lua.get('descricao'))
        
    with moon2:
        texto_alinhado(f"Fonte: {wt_api.fonte_dados()}", alinhamento = 'right', fontsize = 12)
    
    with st.expander("🌒🌓🌔🌕🌖🌗🌘Fases da Lua"):
        PATH_IMG_FASES = Path("assets/images/Fases_da_Lua.png")
        img_fases = Image.open(PATH_IMG_FASES)
        st.image(img_fases, width = "stretch")
        
with col2:
    st.write("aqui entra a previsao")
    
with col3:
    mapa_imet_precipitacao = mapa_precipitacao(data_hoje.year, "Mensal", data_hoje.month)
    st.image(mapa_imet_precipitacao, width = "stretch")
    texto_alinhado("Fonte: https://apiclima.inmet.gov.br/", alinhamento = 'right', fontsize = 12)
    
    data_por_extenso(data_hoje, fontsize = 18)
    texto_local = f"🌍 {local['cidade']}/{local['uf']} - {local['regiao']} do {local['pais']}"
    texto_alinhado(texto_local,fontsize = 14)
    texto_alinhado(f"🌐 ({local['lat']}, {local['long']})")
    texto_alinhado(f"📍{local['obs']}")






