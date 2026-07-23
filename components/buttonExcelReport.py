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
===============================================================================
"""
import streamlit as st
from services.gerador_relat_excel import preencher_relatorio_clima_Tempo_Agora as excel_report
from services.salva_dict import salvar_json

def button_ExcelReport():
    st.divider()
    if st.button("📊 Gerar relatório em Excel"):
        if "_df_previsao_" in st.session_state: 
            df_previsao = st.session_state._df_previsao_ 
        
        if "_info_clima_" in st.session_state: 
            info_clima = st.session_state._info_clima_
            
        st.session_state._excel_report_ = excel_report(info_clima, df_previsao)  #gera o arquivo para download
    
    if "_excel_report_" in st.session_state:
        info_clima = st.session_state._info_clima_
        salvar_json(info_clima,"novo_info_clima.json")
       # localtime = st.session_state._info_clima_["location"]["localtime"]
       # txtdata = localtime.split(" ")[0]
        st.download_button(
                "📥 Baixar relatório",
                data = st.session_state._excel_report_,
                file_name="Relatorio-{txtdata}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )   
    st.divider()
    return