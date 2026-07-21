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
       19/07/2026 - Atualizações para incluir a busca de cidades
                    O quadro de dados do tempo virou um componente
       20/07/2026 - Inicio do scrapping da pagina do tempoagora.uol
===============================================================================
"""

#IMPORTAÇÃO DAS BIBLIOTECAS E FRAMEWORKS
import streamlit as st
from PIL import Image

#Bibliotecas do projeto
import state.estado_app as estado
from components.layout import  data_por_extenso, texto_alinhado 
from components.local import retorna_local
from components.select_city import find_cities_weather
from components.city_options import seleciona_uma_cidade
from components.quadro_clima import mostrar_quadro_clima, texto_localizacao
from components.tabela_previsao import tabela_previsao_tempo
import components.graficos_previsao as graf_prev 
from services.imet_api import mapa_precipitacao
from services.pega_infoclima import  info_clima_agora
import services.previsao_tempo as previsao_tempo
from utils.datas import hoje


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
    local = retorna_local()  #Componente mostra um botão para pegar a localização, caso nao pegar busca pelo IP
    estado.alterar_user_location(local)
    
    user_local = st.session_state.user_location
    
    tem_cidades = find_cities_weather()  #Mostra a opção para buscar cidades
    
    if tem_cidades:  #Se o usuário digitou algo no busca cidades, mostra as cidades encontradas para selecioar
        resp_cidades = st.session_state.resp_busca_cidades
        if resp_cidades[0]['type'] == "erro":
            st.error(resp_cidades[0]['response']['message'])
            estado.restaurar_local_select()
        else: 
            seleciona_uma_cidade()  #Permite o usuario selecionar uma cidade entre as cidades encontradas
        
    #st.map(latitude = user_local['lat'], longitude = user_local['long'])
    
    #Mostra as informações da localização do usuário
    texto_local = f"🌍 {user_local['cidade']}/{user_local['uf']} - {user_local['regiao']} do {user_local['pais']}"
    texto_alinhado(texto_local,fontsize = 14)
    texto_alinhado(f"🌐 ({user_local['lat']}, {user_local['long']})")
    texto_alinhado(f"📍{user_local['obs']}")
    
if st.session_state.local_select["obs"] == "Local vazio":
    local_clima = user_local
    
else:
    local_clima = st.session_state.local_select
    

#Chama o servico que retorna as informações do clima    
info_clima_json = info_clima_agora(local_clima)

col1, col2, col3 = st.columns([1.5, 3.2, 1.2])
with col1:  #Quadro com clima atual
  
    if info_clima_json:
        mostrar_quadro_clima(info_clima_json)
        
    else:
        st.error("Sem dados para mostrar.")
        
with col2: #Previsão do tempo
   texto_alinhado("🌤️🌦️🌥️ Previsão do tempo 🌥️🌦️🌤️", fontsize = 18, alinhamento='center', color='red')
   st.write(texto_localizacao("Previsão para 15 dias",local_clima))
   previsoes = previsao_tempo.pega_previsao_tempo(local_clima)
   
   if previsoes:
       tab_tabela, tab_grafico  = st.tabs(["📋 Tabela","📈 Gráficos"], on_change = "ignore")
       
       with tab_tabela:
            tabela_previsao_tempo(previsoes)
            
       with tab_grafico: 
            cols_tempmaxmin = ["temp_min","temp_max"]
            cols_umidademaxmin =["umidade_min","umidade_max"]
            fig_temp_maxmin = graf_prev.grafico_max_min(previsoes, 
                                                        cols_tempmaxmin,
                                                        "Previsão para 15 dias de temperatura",
                                                        "Celsius (°C)")
            
            fig_umidade_maxmim = graf_prev.grafico_max_min(previsoes, 
                                                        cols_umidademaxmin,
                                                        "Previsão para 15 dias de umidade do ar",
                                                        "Porcentagem (%)")
            
            fig_chuva = graf_prev.grafico_chuva(previsoes)
            
            tab_graf_temp, tab_graf_chuva , tab_graf_umidade = st.tabs(["🌡️Temperatura",
                                                                        "🌧️Chuva",
                                                                        "💧 Umidade do ar"], 
                                                                      on_change = "ignore")
            with tab_graf_temp:
                st.plotly_chart(fig_temp_maxmin)
            with tab_graf_chuva:
                st.plotly_chart(fig_chuva)
            with tab_graf_umidade:
                st.plotly_chart(fig_umidade_maxmim)
        
       fonte_previsao =  previsao_tempo.fonte_dados()
       texto_alinhado(f"Fonte: {fonte_previsao}", alinhamento = 'right', fontsize = 12)
   else:
       st.error("Sem dados para mostrar.")
       
with col3: #Mapas de precipitacão
    tab_mensal, tab_semestral = st.tabs(["Precipitação Mensal", "Precipitação Trimestral"], on_change = "ignore")
    mapa_imet_precipita_mensal = mapa_precipitacao(data_hoje.year, "Mensal", data_hoje.month)
    mapa_imet_precipita_semestral = mapa_precipitacao(data_hoje.year, "Trimestral", data_hoje.month)

    with tab_mensal:    
        st.image(mapa_imet_precipita_mensal, width = "stretch")
        texto_alinhado("Fonte: https://apiclima.inmet.gov.br/", alinhamento = 'right', fontsize = 12)
    with tab_semestral:    
        st.image(mapa_imet_precipita_semestral, width = "stretch")
        texto_alinhado("Fonte: https://apiclima.inmet.gov.br/", alinhamento = 'right', fontsize = 12)
        
    data_por_extenso(data_hoje, fontsize = 18)
    






