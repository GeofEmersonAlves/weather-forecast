# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : busca_cidades.py
Autor      : Emerson
Data       : Sat Jul 18 11:10:34 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    buscar_cidades() é um serviço que sempre retorna uma resposta no mesmo formato, 
independentemente de sucesso ou erro, a resposta padrão esta na "constante"  __RESP_PADRAO__ 
e a função  resp_erro cria a resposta para os erros possiveis    
      

Histórico:
       18/07/2026 - Inicio
       19/07/2026 - Arrumando os vários "bug's" do serviço de buscar cidades
===============================================================================
"""
import requests
from requests.exceptions import (
                                    ConnectionError,
                                    HTTPError,
                                    ReadTimeout,
                                    RequestException,
                                )

from copy import deepcopy
#from pprint import pprint

URL_BUSCA_CIDADES = (
    "https://tempoagora.uol.com.br/json/busca-cidades"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
}

__RESP_PADRAO__ = [
    {
        "type": "city",
        "response": {
            "success": False,
            "message": "",
            "time": None,
            "totalRows": None,
            "totalPages": None,
            "page": None,
            "data": [],
        },
    }
]

def resp_erro(msg_erro : str) -> list(dict):
    resp = deepcopy(__RESP_PADRAO__)
    resp[0]['response']['message'] = msg_erro
    
    return resp
         

def buscar_cidades(nome: str) -> list[dict]:
    nome = nome.strip()

    if len(nome) < 4:
         return  resp_erro("Informe pelo menos quatro caracteres.")
        
        
    try:
        resposta = requests.post(
            URL_BUSCA_CIDADES,
            headers=HEADERS,
            data={"name": nome},
            timeout=(5, 20),
        )

        resposta.raise_for_status()
        resultado = resposta.json()

    except ReadTimeout:
        return  resp_erro("O servidor demorou demais para responder.")

    except ConnectionError:
        return  resp_erro("Não foi possível conectar ao servidor.")

    except HTTPError as erro:
        return resp_erro(f"O servidor retornou o erro HTTP: {erro.response.status_code}")

    except requests.exceptions.JSONDecodeError:
        return resp_erro("O servidor retornou uma resposta inválida.") 

    except RequestException:
        return resp_erro("Ocorreu um erro durante a busca das cidades.")


    #Programação Defensiva: Nunca confiar que os dados recebidos terão exatamente o formato esperado
    if not isinstance(resultado, list) or not resultado:
        return resp_erro("Erro inesperado.")

    primeiro_resultado = resultado[0]

    if not isinstance(primeiro_resultado, dict):
        return resp_erro("Erro inesperado.")

    response = primeiro_resultado.get("response", {})
    if not isinstance(response, dict):
        return resp_erro("Erro inesperado.")

    cidades = response.get("data", [])
    if not isinstance(cidades, list):
        return resp_erro("Erro inesperado.")
    

    return resultado
    
