# -*- coding: utf-8 -*-
"""
********************************************************************
* Rotina......: Datas
* Data início.: 30/06/2026
* Objetivo....: Funções e métodos para trabalhar com datas
* @author.....: Emerson Alves da Silva
* Obs.........:
'********************************************************************
"""

from datetime import datetime, timedelta, date, time
from babel.dates import format_date

#Retorna a data atual
def hoje() -> date:
    data_hoje = datetime.now().date()
    return data_hoje

def agora() -> time:
    hora_agora = datetime.now().time()
    return hora_agora

#Retorna uma data retroativa
def data_retroativa(data_original : date, dias : int) -> date:    
    data_retroativa = data_original - timedelta(dias)
    return data_retroativa

#Retorna uma data futura
def data_futura(data_original : date, dias : int) -> date:
    data_futura = data_original + timedelta(dias)
    return data_futura

#Retorna o texto de uma data por extenso, formatada
def data_texto(data : date) -> str:
    return format_date(data,format='full',locale='pt_BR')