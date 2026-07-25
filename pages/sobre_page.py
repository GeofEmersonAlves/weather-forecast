# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : weather.py
Autor      : Emerson Alves da Silva
Data       : 
Versão     : 1.0
Python     :  Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
         Página princial do app Weather Forecast.
      

Histórico:
       24/07/2026 - Geração automátioca do código esta página a partir de 
                informações passadas por mim e tiradas do código do projeto
       25/07/2026 - Edição do código da página para fazer ajustes necessários
===============================================================================
"""
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Sobre | Weather Forecast",
    #page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Fecha a sidebar por padrão
)


# =========================================================
# CAMINHOS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CAMINHO_FOTO = BASE_DIR / "assets" / "images" / "perfil.jpg"
CAMINHO_SCREENSHOT = BASE_DIR / "assets" / "images" / "screenshot_app.png"


# =========================================================
# LINKS
# =========================================================

URL_GITHUB = "https://github.com/SEU-USUARIO"
URL_REPOSITORIO = "https://github.com/SEU-USUARIO/weather-forecast"
URL_LINKEDIN = "https://www.linkedin.com/in/SEU-PERFIL/"


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            padding: 2.2rem;
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 16px;
            background: rgba(240, 246, 255, 0.45);
            margin-bottom: 2rem;
        }

        .hero-title {
            font-size: 2.3rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .hero-subtitle {
            font-size: 1.1rem;
            color: #555;
            line-height: 1.7;
        }

        .section-title {
            font-size: 1.55rem;
            font-weight: 700;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        .profile-name {
            font-size: 1.55rem;
            font-weight: 700;
            margin-bottom: 0;
        }

        .profile-description {
            color: #555;
            line-height: 1.7;
        }

        .info-card {
            height: 100%;
            padding: 1.3rem;
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 14px;
            background-color: rgba(255, 255, 255, 0.55);
        }

        .info-card-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }

        .info-card-text {
            color: #555;
            line-height: 1.6;
        }

        .technology-card {
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 12px;
            margin-bottom: 0.7rem;
        }

        .technology-name {
            font-weight: 600;
            margin-top: 0.25rem;
        }

        .footer-about {
            margin-top: 3rem;
            padding-top: 1.3rem;
            border-top: 1px solid rgba(128, 128, 128, 0.25);
            text-align: center;
            color: #777;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🌦️ Weather Forecast</div>

        <div class="hero-subtitle">
            Aplicação desenvolvida em Python e Streamlit para consulta de
            condições meteorológicas atuais, previsão para os próximos
            15 dias, visualização de gráficos, acompanhamento das fases
            da Lua e geração automatizada de relatórios em Excel.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DESENVOLVEDOR
# =========================================================

st.markdown(
    '<div class="section-title">👨‍💻 Sobre o desenvolvedor</div>',
    unsafe_allow_html=True,
)

col_foto, col_biografia = st.columns(
    [1, 3],
    gap="large",
    vertical_alignment="center",
)

with col_foto:

    if CAMINHO_FOTO.exists():
        st.image(
            CAMINHO_FOTO,
            width=240,
        )
    else:
        st.markdown(
            """
            <div class="info-card" style="text-align:center;">
                <div style="font-size:5rem;">👨‍💻</div>
                <div>Adicione uma foto em:</div>
                <code>assets/images/perfil.jpg</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_biografia:

    st.markdown(
        """
        <div class="profile-name">Emerson Alves da Silva</div>

        <div class="profile-description">
            <p>
                Geofísico, Mestre em Geociências e desenvolvedor Python,
                com experiência em controle de qualidade de aquisição sísmica,
                processamento e análise de dados, automação de processos e
                desenvolvimento de aplicações.
            </p>

            <p>
                Possuo experiência profissional na aquisição sísmica terrestre
                2D e 3D, incluindo coordenação de equipes de controle de qualidade,
                análise de grandes volumes de dados e elaboração de relatórios
                técnicos.
            </p>

            <p>
                Atualmente, aprofundo meus conhecimentos em Ciência de Dados,
                Machine Learning, visualização de dados e desenvolvimento de
                dashboards interativos com Python e Streamlit.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_linkedin, col_github, col_repo = st.columns(3)

    with col_linkedin:
        st.link_button(
            "💼 LinkedIn",
            URL_LINKEDIN,
            use_container_width=True,
        )

    with col_github:
        st.link_button(
            "🐙 GitHub",
            URL_GITHUB,
            use_container_width=True,
        )

    with col_repo:
        st.link_button(
            "📂 Repositório",
            URL_REPOSITORIO,
            use_container_width=True,
        )


st.divider()


# =========================================================
# OBJETIVO DO PROJETO
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Objetivo do projeto</div>',
    unsafe_allow_html=True,
)

st.write(
    """
    O Weather Forecast foi criado inicialmente como um projeto de estudo
    de desenvolvimento Web com Python. Durante seu desenvolvimento, o
    aplicativo evoluiu para uma solução que integra diferentes fontes
    de dados meteorológicos, técnicas de Web Scraping, visualização de
    dados e automação de relatórios.

    O objetivo é apresentar as informações meteorológicas de forma
    clara, organizada e interativa, permitindo que o usuário consulte
    uma cidade, acompanhe a previsão e gere um relatório em Excel com
    os dados mais recentes.
    """
)


# =========================================================
# PRINCIPAIS FUNCIONALIDADES
# =========================================================

st.markdown(
    '<div class="section-title">🚀 Principais funcionalidades</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">📍 Localização e busca</div>
            <div class="info-card-text">
                Identificação da localização atual e busca de cidades
                para consulta das informações meteorológicas.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">📅 Previsão para 15 dias</div>
            <div class="info-card-text">
                Tabela completa com temperaturas, umidade, precipitação,
                condições do tempo e descrição diária.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">📊 Gráficos interativos</div>
            <div class="info-card-text">
                Visualizações de temperatura, chuva e umidade do ar
                desenvolvidas com Plotly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

col4, col5, col6 = st.columns(3, gap="medium")

with col4:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">🌙 Fases da Lua</div>
            <div class="info-card-text">
                Tabela com a fase da Lua prevista para cada dia,
                acompanhada de imagens e descrições.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">🗺️ Mapas do INMET</div>
            <div class="info-card-text">
                Apresentação de mapas de precipitação mensal e trimestral
                disponibilizados pelo INMET.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col6:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-card-title">📄 Relatório em Excel</div>
            <div class="info-card-text">
                Geração automatizada de relatório com tabelas, imagens,
                gráficos e informações meteorológicas atualizadas.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# =========================================================
# TECNOLOGIAS
# =========================================================

st.markdown(
    '<div class="section-title">🛠️ Tecnologias utilizadas</div>',
    unsafe_allow_html=True,
)

tecnologias = [
    ("🐍", "Python"),
    ("🎈", "Streamlit"),
    ("🐼", "Pandas"),
    ("📊", "Plotly"),
    ("📗", "OpenPyXL"),
    ("🍲", "BeautifulSoup"),
    ("🌐", "Requests"),
    ("🖼️", "Pillow"),
    ("🎨", "CairoSVG"),
    ("🔐", "python-dotenv"),
]

colunas = st.columns(5)

for indice, (icone, nome) in enumerate(tecnologias):

    with colunas[indice % 5]:
        st.markdown(
            f"""
            <div class="technology-card">
                <div style="font-size:1.8rem;">{icone}</div>
                <div class="technology-name">{nome}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# DESTAQUES TÉCNICOS
# =========================================================

st.markdown(
    '<div class="section-title">⚙️ Destaques técnicos</div>',
    unsafe_allow_html=True,
)

col_tecnica1, col_tecnica2 = st.columns(2, gap="large")

with col_tecnica1:
    st.markdown(
        """
        - Consumo e integração de APIs REST.
        - Web Scraping com Requests e BeautifulSoup.
        - Padronização dos retornos dos diferentes serviços.
        - Tratamento de timeouts e falhas nas requisições.
        - Cache para reduzir chamadas externas.
        - Armazenamento e reutilização de ícones meteorológicos.
        """
    )

with col_tecnica2:
    st.markdown(
        """
        - Gerenciamento de estado com `st.session_state`.
        - Manipulação de imagens PNG, SVG e Base64.
        - Exportação de gráficos Plotly como imagens.
        - Geração e formatação de arquivos Excel.
        - Organização modular em componentes, serviços e modelos.
        - Separação entre ambiente local e configurações de deploy.
        """
    )


# =========================================================
# SCREENSHOT
# =========================================================

if CAMINHO_SCREENSHOT.exists():

    st.divider()

    st.markdown(
        '<div class="section-title">🖥️ Aplicação</div>',
        unsafe_allow_html=True,
    )

    st.image(
        CAMINHO_SCREENSHOT,
        caption="Interface principal do Weather Forecast",
        use_container_width=True,
    )


# =========================================================
# FONTES DOS DADOS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">🌐 Fontes dos dados</div>',
    unsafe_allow_html=True,
)

st.info(
    """
    O aplicativo utiliza dados provenientes de APIs públicas,
    serviços meteorológicos e Web Scraping.

    Entre as fontes utilizadas estão WeatherStack, Tempo Agora e INMET.

    Os dados e mapas são apresentados para fins educacionais,
    demonstrativos e de portfólio. As informações podem sofrer
    alterações ou indisponibilidade conforme as fontes externas.
    """
)


# =========================================================
# APRENDIZADOS
# =========================================================

st.markdown(
    '<div class="section-title">📚 Aprendizados do projeto</div>',
    unsafe_allow_html=True,
)

st.write(
    """
    O desenvolvimento do Weather Forecast permitiu aprofundar conhecimentos
    em arquitetura de projetos Python, Streamlit, APIs REST, Web Scraping,
    manipulação de imagens, visualização de dados, gerenciamento de estado,
    tratamento de erros e automação de documentos do Microsoft Excel.

    O projeto também proporcionou a aplicação prática de conceitos de
    experiência do usuário, organização visual, otimização de desempenho
    e documentação de software.
    """
)


# =========================================================
# RODAPÉ
# =========================================================

st.markdown(
    """
    <div class="footer-about">
        <strong>Weather Forecast</strong><br>
        Desenvolvido por Emerson Alves da Silva com Python e Streamlit.
    </div>
    """,
    unsafe_allow_html=True,
)


