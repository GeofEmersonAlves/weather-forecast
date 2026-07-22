# 🌦️ Weather Forecast
  Dashboard meteorológico desenvolvido com Python, Streamlit, Plotly e Web Scraping.
  
![Python](https://img.shields.io/badge/Python-3.13-blue)

![Streamlit](https://img.shields.io/badge/Streamlit-1.50-red)

![License](https://img.shields.io/badge/License-MIT-green)

![Plotly](https://img.shields.io/badge/Plotly-6-blueviolet)

## Funcionalidades
- 📍 Geolocalização
- 🌤️ Consulta das condições meteorológicas atuais
- 📅 Previsão do tempo para os próximos dias 
- 🏙️ Consulta de múltiplas cidades brasileiras 
- 🌧️ Consumo da API do Weatherstack 
- 🗺️ Comsumo da API  d o INMET para mapa de precipitação mensal
- 🗺️ Coleta de dados (webscraping) de paginas de clima 
- 📊 Interface interativa desenvolvida em Streamlit
- 📄 Geração automática de relatórios em Excel a partir de um modelo pré-definido (em implementação)
- 📊 Gráficos interativos

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
- WeatherStack
- INMET
- Pillow

## Ténicas utilizadas
- Web Scraping
- REST API
- Data Visualization
- Caching
- Session State
- Interactive Dashboard
- Responsive Layout
- Image Processing

## Fontes de Dados

- **API Weatherstack** –  Excelente para dados ao vivo, com velocidade na entrega e cobertura global massiva
- 
- **API INMET (Instituto Nacional de Meteorologia)** – obtenção automática do mapa de prognóstico de precipitação trimestral

## 📁 Estrutura do Projeto
```
weather-forecast/
│
├── assets/                  # Ícones e imagens da aplicação
│   ├── icons/
│   └── images/
│
├── components/              # Componentes da interface Streamlit
│   ├── city_options.py
│   ├── downloads.py
│   ├── graficos_previsao.py
│   ├── layout.py
│   ├── local.py
│   ├── quadro_clima.py
│   ├── select_city.py
│   ├── stream_geolocation.py
│   └── tabela_previsao.py
│
├── models/                  # Modelos de dados
│   ├── info_clima.py
│   └── local_vazio.py
│
├── pages/                   # Páginas da aplicação
│   ├── weather_page.py
│   └── testes.py
│
├── services/                # APIs, Web Scraping e regras de negócio
│   ├── busca_cidades.py
│   ├── fase_da_lua.py
│   ├── geolocation.py
│   ├── gerar_img_base64.py
│   ├── imet_api.py
│   ├── pega_infoclima.py
│   ├── previsao_tempo.py
│   ├── requisicao.py
│   ├── salva_dict.py
│   ├── weather_api.py
│   └── weatherinfo_scraped.py
│
├── state/                   # Gerenciamento de estado da aplicação
│   └── estado_app.py
│
├── templates/
│   └── excel/
│
├── utils/
│   └── datas.py
│
├── .streamlit/
│   └── config.toml
│
├── app.py                   # Ponto de entrada da aplicação
├── requirements.txt
├── README.md
└── LICENSE
```

## Explicacao do codigo regex
    (.+?): Captura o nome da cidade (qualquer caractere até encontrar o hífen).
    -: Encontra o hífen que separa a cidade da UF.
    ([A-Z]{2}): Captura exatamente as duas letras maiúsculas da UF.
    \s*: Ignora espaços em branco que possam existir antes dos parênteses.
    \((.+?)\): Captura o texto que está dentro dos parênteses, que representa o país."

## Objetivo

Este projeto nasceu como um protótipo para automatizar a geração da aba **PREVISÃO DO TEMPO** de um relatório operacional utilizado em projetos.

Além de servir como estudo de consumo de APIs, Web Scraping, manipulação de Excel e desenvolvimento com Streamlit.


