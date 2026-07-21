# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : weatherinfo_scraped.py
Autor      : Emerson A. Silva
Data       : Mon Jul 20 10:48:17 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Faz um scrapping de uma pagina de clima para obter as informações climaticas
      

Histórico:
       20/07/2026 - Inicio 
===============================================================================
"""
import streamlit as st
from bs4 import BeautifulSoup
from copy import deepcopy
from urllib.parse import urljoin
from slugify import slugify

from models.info_clima import novo_info_clima
from services.busca_cidades import traz_cidade_clima
from services.weather_api import direcao_vento_emoji, astro_evento #weather_icon
import services.requisicao as req
from services.fase_da_lua import fase_da_lua

#pip install python-slugify

URLS= ["https://tempoagora.uol.com.br/previsao-do-tempo/agora/cidade/", 
       "https://tempoagora.uol.com.br/previsao-do-tempo/cidade/",
       "https://tempoagora.uol.com.br/"]

def gera_url(base, id_cidade: int, cidade: str, uf: str ) -> str:
    cidade = slugify(cidade,separator="")
    caminho_slug = f"{cidade}-{uf}"

    # Monta a URL final usando f-string ou urljoin
    url_final = urljoin(base, f"{id_cidade}/{caminho_slug}")    
    
    return url_final

def scrap_page1(dados_cidade : dict) -> dict:
    cidade = dados_cidade['city']
    estado = dados_cidade["uf"]
    id_cid = dados_cidade["idcity"]
    
    url_dados = gera_url(URLS[0], id_cid, cidade, estado)

    resposta = req.faz_requisicao(url_dados, use_raise=False)

    soup = BeautifulSoup(resposta.text, "lxml")
    card = soup.select_one("div.card._justify-center")

    # Temperatura principal e ícone
    span_temperatura = card.select_one("span.-font-55")

    temperatura = span_temperatura.get_text(strip=True)

    icone_clima = span_temperatura.find_previous("img")["src"]

    # Bloco de descrição e sensação térmica
    info = card.select_one(".no-gutters")

   # imgs = info.select("img")
    spans = info.select("span")

    # Condição do tempo
  #  icone_tempo =  info.select_one("img")["src"]
    descricao = spans[0].get_text(strip=True)

    # Sensação térmica
   # icone_sensacao = imgs[1]["src"]
    sensacao = spans[1].get_text(strip=True)

    # Variáveis
    variaveis = card.select(".variables-list .item")

    vento = variaveis[0].select("div")[-1].get_text(" ", strip=True)
    umidade = variaveis[1].select("div")[-1].get_text(" ", strip=True)
   # pressao = variaveis[2].select("div")[-1].get_text(" ", strip=True)

    # Download do ícone principal do clima
    url_weather_icon = urljoin(URLS[2], icone_clima)
    
    weather_icon_img = url_weather_icon #weather_icon(url_weather_icon)

    final = {"temperatura": temperatura.replace("º", ""),
            'img_clima': weather_icon_img,
            "descricao" : descricao,
            "vento": vento,
            "umidade":umidade,
            "sensacao": sensacao}
    
    return final

def scrap_page2(dados_cidade : dict) -> list:
    cidade = dados_cidade['city']
    estado = dados_cidade["uf"]
    id_cid = dados_cidade["idcity"]
    
    url_dados = gera_url(URLS[1], id_cid, cidade, estado)

    resposta = req.faz_requisicao(url_dados, use_raise=False)
   
    soup = BeautifulSoup(resposta.text, "lxml")

    #elemento = soup.find(id="min-temp-1")
    #temp_min = elemento.text.strip()
    
    #elemento = soup.find(id="max-temp-1")
    #temp_max = elemento.text.strip()
   
    dados = {}
    for item in soup.select("ul.variables-list li"):
        nome = item.select_one(".variable").get_text(strip=True)
        valor = item.get_text(" ", strip=True)
        dados[nome] = valor

    txt_temp = dados["Temperatura"]
    temp_min = txt_temp.replace("°","").split(" ")[1]
    temp_max = txt_temp.replace("°","").split(" ")[2]
    
    txt_temp_min = "🌡️⬇️Temp. Mínima:"
    txt_temp_mim_valor = f"🔻{temp_min} °C"
    
    txt_temp_max = "🌡️⬆️Temp. Máxima:"
    txt_temp_max_valor = f"🔺{temp_max} °C"
 
    txt_chuva = dados["Chuva"]
    vol_chuva = txt_chuva.split(" ")[1]
    porc_chuva = txt_chuva.split(" ")[2]
    porc_chuva = porc_chuva.replace("\n","").replace("\t","").replace(" ","").replace("-","")
    txt_sol = dados["Sol"]
    sol_nasc = txt_sol.split(" ")[1]
    sol_desc = txt_sol.split(" ")[2]
    
    txt_sol_up_h = "🧭 "+sol_nasc
    txt_sol_up = astro_evento('sunrise')
    txt_sol_down_h = "🧭 "+sol_desc
    txt_sol_down = astro_evento('sunset')
    
    txt_precipita = "🌧️ Precipitação"
    txt_preci_valor = f"💧 {vol_chuva} - {porc_chuva} "
        
    tab_astro = [
           [txt_temp_max, txt_temp_max_valor],
           [txt_temp_min, txt_temp_mim_valor],
           [txt_sol_up, txt_sol_up_h ],
           [txt_sol_down, txt_sol_down_h],
           [txt_precipita, txt_preci_valor]
       ]
    
    return tab_astro


@st.cache_data(show_spinner="⏳ Carregando condições climáticas . . .",  ttl = 1800)
def clima_agora(dados_cidade : dict) -> dict:
    info_clima_vazio = novo_info_clima()
    
    cidade_clima = traz_cidade_clima(dados_cidade)
 
    info_clima_vazio["request"]["type"] = "Scrapping" 
    info_clima_vazio["request"]["language"] = "PT-BR"
    info_clima_vazio["request"]["unit"] = "m"
    
    info_clima_vazio["location"]["name"] = dados_cidade["cidade"]
    info_clima_vazio["location"]["country"] = dados_cidade["pais"]
    info_clima_vazio["location"]["region"] = dados_cidade["regiao"]
    info_clima_vazio["location"]["lat"] = dados_cidade["lat"]
    info_clima_vazio["location"]["lon"] = dados_cidade["long"]
    
    mais_info = scrap_page1(cidade_clima)
    info_clima_vazio["current"]["temperature"] = mais_info["temperatura"]
    info_clima_vazio['img_clima'] = mais_info['img_clima']
    
    vento = mais_info['vento']
    direcao = vento.split(" - ")[0]
    vento_veloc =  vento.split(" - ")[1]
    vento_dir_emoji = direcao_vento_emoji(direcao)
    texto_vento = f"💨 Vento {vento_veloc} {vento_dir_emoji}{direcao}"
    
    texto_umidade = f"💧 Umidade {mais_info['umidade']}"
    
    valor_sensacao =  mais_info['sensacao'].split(" - ")[1].replace("°", "")
    texto_sensacao = f"🌡️ Sensação {valor_sensacao} ºC"
    
    info_clima_vazio['tab_clima'] = [mais_info['descricao'], 
                                     texto_vento, 
                                     texto_umidade,
                                     texto_sensacao]
    
    info_tab_astro = scrap_page2(cidade_clima)
    
    info_clima_vazio['tab_astro'] = info_tab_astro
    info_clima_vazio["fonte_dados"] = F"{URLS[2]}"

    fase_lua = fase_da_lua()

    info_clima_vazio["fase_lua"] = fase_lua

    return deepcopy(info_clima_vazio) 



#scrap_page({"idcity":271, 'cidade':"Curitiba", "uf":"PR"})

