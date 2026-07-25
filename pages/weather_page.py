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
       22/07/2026 - Inclusão da aba "Fases da lua" com a tabela de fases da lua 
       22/07/2026 - Inclusão da funcionalidade de Geração de Relatório em Excel
       23/07/2026 - Alterações para melhorar a performance devido à Geração de Relatório em Excel
       24/04/2026 - Alterações para antender o novo layout do relatório em excel
===============================================================================
"""

#IMPORTAÇÃO DAS BIBLIOTECAS E FRAMEWORKS
import streamlit as st
#Bibliotecas do projeto
import state.estado_app as estado
from components.layout import  mostra_data_por_extenso, texto_alinhado 
from components.local import retorna_local, local_formatado
from components.select_city import find_cities_weather
from components.city_options import seleciona_uma_cidade
from components.quadro_clima import mostrar_quadro_clima, texto_localizacao
import components.tabela_previsao as tbprevtemp
import components.graficos_previsao as graf_prev 
from components.nota_rodape import nota_de_rodape
from components.quadro_fases_da_lua import quadro_fases_da_lua
from components.buttonExcelReport import button_ExcelReport
from services.imet_api import mapa_precipitacao
from services.pega_infoclima import  info_clima_agora
import services.previsao_tempo as previsao_tempo
from services.fase_da_lua import info_fase_da_lua_com_none
from utils.datas import hoje, data_por_extenso
#from services.salva_dict import salvar_json


# =========== FUNCÃO PARA LIMPAR O CACHE ===========
def limpar_cache():
    st.cache_data.clear()

@st.cache_data(show_spinner="⏳ Carregando previsão do tempo . . .",  ttl = 1800)
def pega_previsao_cache(local_clima : dict)->dict: 
    previsoes=  previsao_tempo.pega_previsao_tempo(local_clima)
    
    return previsoes

#if "cont" not in st.session_state:
#    st.session_state.cont =0

st.set_page_config("Weather Forecast",
                   page_icon = st.session_state._icone_app_,
                   layout="wide",
                   initial_sidebar_state="expanded"
                    )

st.logo(st.session_state._icone_app_, icon_image = st.session_state._icone_app_)

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
    
    button_ExcelReport()
    
    #   Esse dicionario vai para o info_clima como rodape_info :{...}
    #assim posso pegar esse texto para colocar o relatóro em excel
    texto = "Dados obtidos por APIs públicas, INMET e Web Scraping para fins educacionais e demonstrativos."
    versao = "Versão 1.0.0 • Julho/2026"
    rodape_info ={"texto_info": texto,
                  "versao":versao
                  }
    #Mostra as informações da localização do usuário
    info = local_formatado(user_local)
    texto_alinhado(info["local"], fontsize = 14)
    texto_alinhado(info["coordenadas"])
    texto_alinhado(info["origem_coordenadas"])
    
if st.session_state.local_select["obs"] == "Local vazio":
    local_clima = user_local
    
else:
    local_clima = st.session_state.local_select
    

#Chama o servico que retorna as informações do clima    
info_clima_json = info_clima_agora(local_clima)

texto_local = texto_localizacao("Tempo agora em", local_clima, False)

col1, col2, col3 = st.columns([1.5, 3.2, 1.2])
with col1:  #Quadro com clima atual
   
    if info_clima_json:
        info_clima_json["local_clima"] = texto_local
        info_clima_json["data_por_extenso"] =  data_por_extenso(data_hoje)
        info_clima_json["rodape_info"] = rodape_info
        mostrar_quadro_clima(info_clima_json)
        
    else:
        st.error("⚠️ Não foi possível obter os dados do clima. Tente novamente...")
        
with col2: #Previsão do tempo
   #texto_alinhado("🌤️🌦️🌥️ Previsão do tempo 🌥️🌦️🌤️", fontsize = 18, alinhamento='center', color='red')
   st.write(texto_localizacao("🌤️🌦️🌥️ Previsão para 15 dias",local_clima))
   previsoes = pega_previsao_cache(local_clima)
  
   if previsoes:
       st.session_state._previsoes_ = previsoes
       fase_lua = previsoes[0]["fase_lua"]
       emojilua = info_fase_da_lua_com_none(fase_lua)
       emojilua = emojilua["emoji"]
       tab_tabela, tab_faselua, tab_grafico  = st.tabs(["📋 Tabela Clima", f"{emojilua} Tabela Fases da Lua", "📈 Gráficos"], on_change = "ignore")
       
       with tab_tabela:
            #Por questão de performance, o df_previsões é gerado só uma vez e guardado na session
    
            df_previsao = tbprevtemp.gera_df_previsao(previsoes)
            st.session_state._df_previsao_ = df_previsao
                
            tbprevtemp.tabela_previsao_tempo(df_previsao)
       
       with tab_faselua:
           quadro_fases_da_lua(previsoes)
           
       with tab_grafico: 
            cols_tempmaxmin = ["temp_min","temp_max"]
            cols_umidademaxmin =["umidade_min","umidade_max"]
            graf_temp_maxmin = graf_prev.grafico_max_min(previsoes, 
                                                        cols_tempmaxmin,
                                                        "Previsão para 15 dias de temperatura",
                                                        "Celsius (°C)")
            
            graf_umid_maxmim = graf_prev.grafico_max_min(previsoes, 
                                                        cols_umidademaxmin,
                                                        "Previsão para 15 dias de umidade do ar",
                                                        "Porcentagem (%)")
            
            graf_chuva = graf_prev.grafico_chuva(previsoes,"Previsão de chuva para 15 dias")
            
            #Guarda os tres gráficos na session, assim podem ser usados para o Relatório
            st.session_state._graf_temp_maxmin_ = graf_temp_maxmin
            st.session_state._graf_umid_maxmim_ = graf_umid_maxmim
            st.session_state._graf_chuva_ = graf_chuva
            
            tab_graf_temp, tab_graf_chuva , tab_graf_umidade = st.tabs(["🌡️Temperatura",
                                                                        "🌧️Chuva",
                                                                        "💧 Umidade do ar"], 
                                                                      on_change = "ignore")
            with tab_graf_temp:
                st.plotly_chart(graf_temp_maxmin, height = 400)
            with tab_graf_chuva:
                st.plotly_chart(graf_chuva, height = 400)
            with tab_graf_umidade:
                st.plotly_chart(graf_umid_maxmim, height = 400)
        
       fonte_previsao =  previsao_tempo.fonte_dados()
       st.session_state._fonte_previsao_ = fonte_previsao
       texto_alinhado(f"Fonte: {fonte_previsao}", alinhamento = 'right', fontsize = 12)
   else:
       st.error("⚠️ Não foi possível obter dados da previsão do tempo. Tente novamente...")
       st.button("🗑 Limpar Cache",
          type="tertiary",
          on_click = limpar_cache)
       
       
with col3: #Mapas de precipitacão
    tab_mensal, tab_semestral = st.tabs(["Precipitação Mensal", "Precipitação Trimestral"], on_change = "ignore")
    mapa_imet_mensal = mapa_precipitacao(data_hoje.year, "Mensal", data_hoje.month)
    mapa_imet_semestral = mapa_precipitacao(data_hoje.year, "Trimestral", data_hoje.month)
    
    st.session_state._mapa_imet_mensal_ = mapa_imet_mensal
    st.session_state._mapa_imet_semestral_ = mapa_imet_semestral

    with tab_mensal:    
        st.image(mapa_imet_mensal, width = "stretch")
        texto_alinhado("Fonte: https://apiclima.inmet.gov.br/", alinhamento = 'right', fontsize = 12)
    with tab_semestral:    
        st.image(mapa_imet_semestral, width = "stretch")
        texto_alinhado("Fonte: https://apiclima.inmet.gov.br/", alinhamento = 'right', fontsize = 12)
   
    
    mostra_data_por_extenso(data_hoje, fontsize = 18)
    
nota_de_rodape()

texto_alinhado(rodape_info["texto_info"], alinhamento = "right", fontsize = 12, color = "blue")
texto_alinhado(rodape_info["versao"], alinhamento = "right", fontsize = 10, color = "gray")



