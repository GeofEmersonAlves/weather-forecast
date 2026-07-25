# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : buttonExcelReport.py
Autor      : Emerson
Data       : Thu Jul 23 10:27:59 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Para melhorar a leitura do código e tambem a performance criei este
componente que exibe um botão para geração do relatório em Excel e da a opção
de download deste relatório.

Histórico:
       23/07/2026 - Inicio
       24/07/2026 - Alterações finais para o novo layout do relatório
===============================================================================
"""
import streamlit as st
from services.gerador_relat_excel import preencher_relatorio_clima_Tempo_Agora as excel_report
from components.local import local_formatado
#from services.salva_dict import salvar_json

def button_ExcelReport():
    st.divider()
    if st.button("📊 Gerar relatório em Excel"):
        if "_df_previsao_" in st.session_state: 
            df_previsao = st.session_state._df_previsao_ 
        
        if "_info_clima_" in st.session_state: 
            info_clima = st.session_state._info_clima_
        
        if "_previsoes_" in st.session_state:
            previsoes_dict = st.session_state._previsoes_ 
        
        if "_fonte_previsao_" in st.session_state:
            fonte_previsao = st.session_state._fonte_previsao_
        
        user_local = st.session_state.user_location
        info_user_local = local_formatado(user_local)
        
        #Mapas
        mapa_imet_mensal = st.session_state._mapa_imet_mensal_ 
        mapa_imet_semestral = st.session_state._mapa_imet_semestral_ 
        #Gráficos
        graf_temp_maxmin = st.session_state._graf_temp_maxmin_
        graf_umid_maxmim = st.session_state._graf_umid_maxmim_ 
        graf_chuva = st.session_state._graf_chuva_
        
        
        st.session_state._excel_report_ = excel_report(info_clima,
                                                       info_user_local,
                                                       previsoes_dict,
                                                       df_previsao,
                                                       fonte_previsao,
                                                       mapa_imet_mensal,
                                                       mapa_imet_semestral,
                                                       graf_temp_maxmin,
                                                       graf_umid_maxmim,
                                                       graf_chuva)  #gera o arquivo para download
    
    if "_excel_report_" in st.session_state:
        info_clima = st.session_state._info_clima_
        #salvar_json(info_clima,"novo_info_clima.json")
        localtime = st.session_state._info_clima_["location"]["localtime"]
        txtdata = localtime.split(" ")[0]
        if st.download_button("📥 Baixar último relatório gerado",
                            data = st.session_state._excel_report_,
                            file_name = f"Relatorio-{txtdata}.xlsx",
                            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            ):
            st.session_state.pop('_excel_report_', None) #Limpa o relatório apos o download 
            st.session_state.pop('_info_clima_', None)     
            st.session_state.pop('_df_previsao_', None) 
            
    st.divider()
    return