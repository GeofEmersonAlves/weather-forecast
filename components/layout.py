# -*- coding: utf-8 -*-
"""
********************************************************************
* Rotina......: layout.py
* Data início.: 01/07/2026
* Objetivo....: Componente para lidar com os estilos do projeto
* Autor.......: Emerson Alves da Silva
* Obs.........:
********************************************************************
"""
import streamlit as st
import base64
from datetime import date, time
from babel.dates import format_date

def muda_cor_fundo_container(cor_de_fundo: str, key: str, padding : int = 0, border_radius : int = 0):
    estilo_css = f"""
    <style>
        div[data-testid="stVerticalBlock"]:has(div.st-key-{key}) {{
            background-color: {cor_de_fundo};
            padding: {padding}px;
            border-radius: {border_radius}px;
            box-shadow: 4px 4px 12px rgba(100, 100, 100, 0.25);
        }}
    </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def imagem_fundo_tela(img_path : str):
    img_base64 = get_base64_of_bin_file(img_path)
    # Código CSS para definir a imagem de fundo
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def texto_alinhado(texto : str, alinhamento : str = 'right', fontsize : int = 10, color : str = '#A0A0A0'):
    texto = f"""
    <p style="text-align:{alinhamento}; font-size:{fontsize}px; color:{color}; margin:0;">
        {texto}
    </p>
    """
    st.write(texto, unsafe_allow_html=True)

def mostra_atualizado(hora_atualizado : time):
    texto = f"""
    <p style="text-align:right; font-size:8px; color:#A0A0A0; margin:0;">
        🕒 Atualizado em {hora_atualizado:%H:%M:%S}
    </p>
    """
    st.write(texto, unsafe_allow_html=True)

def data_por_extenso(data : date, alinhamento : str='right', fontsize : int = 10):
    data_ext = format_date(data, format='full',locale='pt_BR')
    texto = f"""
    <p style="text-align:{alinhamento}; font-size:{fontsize}px; color:#A0A0A0; margin:0;">
        📅{data_ext}
    </p>
    """
  #  f"<p style=text-align:{alinhamento}; font-size:{fontsize}px;>📅{texto}</p>"
    
    st.markdown(texto, unsafe_allow_html=True)

def css_box_with_shadow(backcolor : str = "black"): #melhorar depois, premitindo passar cor do fundo 
    # CSS personalizado para a cor e sombra do form
    form_css = f"""
    <style>
    div[data-testid="stForm"] {{
        background: {backcolor};
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow:
            0 4px 8px rgba(0, 0, 0, 0.05),
            0 12px 24px rgba(0, 0, 0, 0.08);
    }}
    </style>
    """
    st.markdown(form_css, unsafe_allow_html=True)

def aplicar_css_excel():
    st.markdown("""
    <style>

    /* DataFrame */

    div[data-testid="stDataFrame"] {

        border: 1px solid #bfbfbf;
        border-radius: 0px;
        overflow: hidden;
    }

    /* Cabeçalho */

    div[data-testid="stDataFrame"] thead th{

        background-color:#E2F0D9;

        color:#000000;

        font-weight:bold;

        border:1px solid #C6C6C6;
    }

    /* Células */

    div[data-testid="stDataFrame"] td{

        border:1px solid #D9D9D9;

        background-color:white;

        color:black;
    }

    /* Zebra */

    div[data-testid="stDataFrame"] tbody tr:nth-child(even){

        background:#F8F8F8;

    }

    /* Linha selecionada */

    div[data-testid="stDataFrame"] tbody tr:hover{

        background:#DDEBF7;

    }

    </style>
    """, unsafe_allow_html=True)
    
def mostrar_tabela_excel(df):
    html = df.to_html(index=False, classes="tabela-excel")

    st.markdown("""
    <style>
    .tabela-excel {
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        font-size: 12px;
    }

    .tabela-excel th {
        background-color: #E2F0D9;
        color: #000000;
        font-weight: bold;
        text-align: center;
        border: 1px solid #A6A6A6;
        padding: 6px;
    }

    .tabela-excel td {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #D9D9D9;
        padding: 6px;
    }

    .tabela-excel tr:nth-child(even) td {
        background-color: #F8F8F8;
    }

    .tabela-excel tr:hover td {
        background-color: #DDEBF7;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(html, unsafe_allow_html=True)