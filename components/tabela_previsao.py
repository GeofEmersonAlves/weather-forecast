# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : tabela_previsao.py
Autor      : Emerson A. SilVA
Data       : Tue Jul 21 00:24:01 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Só para organizar a pagina principal, movi este componente para ca
      

Histórico:
       21/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
import pandas as pd
import services.gerar_img_base64 as gerar_img

def tabela_previsao_tempo(previsoes :list[dict]):
     dados_exibir=[]
     for dia in previsoes:
         dia_bola = gerar_img.gerar_dia_base64(dia['dia'], dia['dia_semana'])
         if dia["temp_min"] == None:
             temp_min = 0
         else:
             temp_min = dia["temp_min"]
         
         if dia['temp_max'] == None:
             temp_max = 0
         else:
             temp_max = dia["temp_max"]
         
         temp_max_min = gerar_img.temperaturas_min_max_base64(temp_min, temp_max)
         
         if dia["umidade_min"] == None:
             umidade_min = 0
         else:
             umidade_min =  dia["umidade_min"]
         
         if dia["umidade_max"] == None:
             umidade_max = 0
         else:
             umidade_max =  dia["umidade_max"]
         
         if dia["precipitacao_mm"] == None:
             precipitacao = 0
         else:
             precipitacao =  dia["precipitacao_mm"]
         
         if dia["probabilidade_chuva"] == None:
             probabilidade_chuva = 0
         else:
             probabilidade_chuva =  dia["probabilidade_chuva"]
         
         img_chuva_umidade = gerar_img.clima_chuva_base64(
                                                  umidade_min=umidade_min,
                                                  umidade_max=umidade_max,
                                                  precipitacao=precipitacao,
                                                  probabilidade_chuva=probabilidade_chuva,
                                              )
         
         dados ={'dia_bola': dia_bola,
                 'icone': dia['icone'],
                 'temp_max_min': temp_max_min,
                 'Umidade e chuva': img_chuva_umidade,
                 'Descrição': dia['descricao']
             }
         
         dados_exibir.append(dados)
        
     df_previsao = pd.DataFrame(dados_exibir)
    
     st.dataframe(df_previsao,
         height  = 490 ,  
         row_height = 60,
         column_config={
             "dia_bola": st.column_config.ImageColumn(
                 "Dia",
                 width=60
             ),
             "icone": st.column_config.ImageColumn(
                 "Clima",
                 width="small"
             ),
             "temp_max_min": st.column_config.ImageColumn(
                 "Max/Min",
                 width="small"
             ),
             "Umidade e chuva": st.column_config.ImageColumn(
                 width=180
             ),
         },
         hide_index=True
         )