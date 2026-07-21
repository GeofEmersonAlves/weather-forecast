# 🌦️ Weather Forecast

  Aplicação desenvolvida em **Python** e **Streamlit** para consulta das condições meteorológicas e previsão do tempo em cidades brasileiras.

  O projeto integra dados meteorológicos de diferentes fontes para automatizar a geração de relatórios operacionais em Excel, 
substituindo parte de um processo que atualmente é realizado manualmente.

## Funcionalidades

- 🌤️ Consulta das condições meteorológicas atuais
- 📅 Previsão do tempo para os próximos dias 
- 🏙️ Consulta de múltiplas cidades brasileiras 
- 🌧️ Consumo da API do Weatherstack 
- 🗺️ Comsumo da API  d o INMET para mapa de precipitação mensal
- 🗺️ Coleta de dados (webscraping) de paginas de clima 
- 📊 Interface interativa desenvolvida em Streamlit
- 📄 Geração automática de relatórios em Excel a partir de um modelo pré-definido (em implementação)

## Tecnologias

- Python
- Streamlit
- Requests
- Pandas
- OpenPyXL
- BeautifulSoup
- Dotenv
- Geopy - OpenStreetMap(GRATUITO)
- streamlit-geolocation
- Babel
- python-slugify
- cairosvg
- plotly

## Fontes de Dados

- **API Weatherstack** –  Excelente para dados ao vivo, com velocidade na entrega e cobertura global massiva
- 
- **API INMET (Instituto Nacional de Meteorologia)** – obtenção automática do mapa de prognóstico de precipitação trimestral

## Explicacao do codigo regex
    (.+?): Captura o nome da cidade (qualquer caractere até encontrar o hífen).
    -: Encontra o hífen que separa a cidade da UF.
    ([A-Z]{2}): Captura exatamente as duas letras maiúsculas da UF.
    \s*: Ignora espaços em branco que possam existir antes dos parênteses.
    \((.+?)\): Captura o texto que está dentro dos parênteses, que representa o país."

## Objetivo

Este projeto nasceu como um protótipo para automatizar a geração da aba **PREVISÃO DO TEMPO** de um relatório operacional utilizado em projetos.

Além de servir como estudo de consumo de APIs, Web Scraping, manipulação de Excel e desenvolvimento com Streamlit.
