# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : select_city.py
Autor      : Emerson
Data       : Sat Jul 18 12:01:47 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    Componenmte seletor de cidades com autocomplete real a partir da quarta letra digitada

Histórico:
       18/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
from  services.busca_cidades import buscar_cidades

import json       

#Fiz para ver o resultado e fazer uns testes, vou mantê-la aqui sei lá por que
def salva_dict(dicionario : dict):
    with open("dados.json","w", encoding="utf-8") as arquivo:
        json.dump(dicionario, arquivo, indent=4, ensure_ascii=False)

def find_cities():
    #st.write(f"Digitado:{texto} {len(texto.strip())}")
    letras_cidade = st.session_state.__letras_cidade__
    
    if letras_cidade is not None:
        if len(letras_cidade.strip()) >= 4:
            resp_json =  buscar_cidades(letras_cidade)
            
            if "response" in resp_json[0]:
                st.write() 
            
               # cidades_json =  resp_json.get('response').get('data')
            st.json(resp_json)

def select_city_weather(atual_city: str) :
   # lst_cidades = [atual_city]
    
    st.text_input("🔍Busque por uma cidade...",
                           placeholder="Digite no mínimo 4 letras...",
                           key = "__letras_cidade__",
                           on_change = find_cities,
                           icon = ":material/search:"
                           )
    
   
    
    return 

"""

option = st.selectbox(
    "Cidade",
    lst_cidades,
    index=None,
    placeholder="Busque por uma cidade...",
    accept_new_options=True,
)

moeda_final = st.segmented_control(legenda, 
                                    lista_moedas, 
                                    selection_mode = "single", 
                                    default = moeda_final_default,
                                    on_change = converter_moeda,
                                        key =  "_moeda_final_") 
    """