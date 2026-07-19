# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : bing_weather_scrap.py
Autor      : Emerson A. Silvca
Data       : Fri Jul 17 22:44:43 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Faz scraping dos dados climaticos da pagina de clima do bing.com
      

Histórico:
       17/07/2026 - Inicio ......
===============================================================================
"""
import services.requisicao as req
#from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def html_bing_weather(cidade : str) -> str | None:
    
    #url = f"https://www.google.com/search?q=tempo+agora+{quote_plus(cidade)}"
    url="https://www.climatempo.com.br/previsao-do-tempo/cidade/558/saopaulo-sp"
    head = req.cria_headers()
    print(url)
    resposta = req.faz_requisicao(url, head)
    
    if resposta is None:
        return None

    html_bing = resposta.text
    
    return html_bing


bing_html = html_bing_weather("São Paulo-SP")

if bing_html:    
    with open("bing_html.txt", "w", encoding="utf-8") as file:
        file.write(bing_html)
        
    print(bing_html)
    soup = BeautifulSoup(bing_html, "lxml")
    
    src = soup.find('.cico')
    print(src)

