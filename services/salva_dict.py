# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    :
Arquivo    : 
Autor      : Emerson
Data       : Mon Jul 20 10:59:59 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        
      

Histórico:
       dd/mm/aaaa - Inicio ......
===============================================================================
"""
import json

def salvar_json(dicionario : dict, filename : str = "dados.json"):
    with open(filename, "w", encoding="utf-8") as arquivo:
        json.dump(dicionario, arquivo, indent=4, ensure_ascii=False)