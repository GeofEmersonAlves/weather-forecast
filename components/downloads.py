# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 23:43:08 2026

@author: Emerson
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO


@st.cache_data
def convert_csv_for_download(df : pd.DataFrame):
    return df.to_csv().encode("utf-8")

@st.cache_data
def convert_xlsx_for_download(df : pd.DataFrame, sheet_name: str='Planilha1', index : bool = True) -> bytes:
    #Criar um buffer na memória
    buffer = BytesIO()
    # 3. Escreva o DataFrame no buffer usando o engine xlsxwriter
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index = index, sheet_name = sheet_name)

    return buffer.getvalue()



def download_csv(df : pd.DataFrame, filename):
    close_csv = convert_csv_for_download(df)
    st.download_button(
        label="Baixar .csv",
        data=close_csv,
        file_name=filename +".csv",
        mime="text/csv",
        icon=":material/download:"
    )

def download_excel_xlsx(df : pd.DataFrame, filename, index : bool = True):              
           close_xlsx = convert_xlsx_for_download(df, index=index)
           st.download_button(
               label="Baixar Excel",
               data=close_xlsx,
               file_name=filename +".xlsx",
               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
               icon=":material/download:"
           )


def salvar_csv(df:pd.DataFrame, fileName:str) -> str:
    BASE_DIR = Path(__file__).parent.parent
    file_path = BASE_DIR / "uploads" / fileName
    
    try:
        df.to_csv(file_path)
        return f"Arquivo:   \n{file_path}    \n gravado com sucesso!"
    
    except Exception as e:
        return f"ERRO ao salvar o arquivo: \n {e}"