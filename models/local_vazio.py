# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : local_vazio.py
Autor      : Emerson A. Silva
Data       : Mon Jul 20 11:16:36 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Modelo do dicionario padrão de local

Histórico:
       21/07/2026 - Inicio 
===============================================================================
"""
from copy import deepcopy

__LOCAL_EMPTY__ = {"lat": None,
                   "long": None,
                   "pais": None,
                   "estado": None,
                   "uf": None,
                   "cidade": None,
                   "idcity": None,
                   "litoral": None,
                   "bairro": "",
                   "regiao": None,
                   "obs": "Local vazio"
                   }

def local_empty()-> dict:
    return deepcopy(__LOCAL_EMPTY__)
