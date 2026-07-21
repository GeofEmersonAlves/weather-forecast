# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : graficos_previsao.py
Autor      : Emerson A. Silva
Data       : Tue Jul 21 00:29:40 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
    Componente que faz os gráficos com os dados de previsão do tempo
      

Histórico:
       21/07/2026 - Inicio 
       
{
        "data": "2026-07-28",
        "dia": "28/07",
        "dia_semana": "Terça",
        "temperatura_minima": 14,
        "temperatura_maxima": 27,
        "precipitacao_mm": 0,
        "probabilidade_chuva": 0,
        "descricao": "Sol com algumas nuvens ao longo do dia. Noite de céu limpo.",
        "icone": "9",
        "umidade_minima": 47,
        "umidade_maxima": 100,
        "vento_minimo": 1,
        "vento_maximo": 6,
        "direcao_vento": "ENE",
        "nascer_sol": "06:43:59",
        "por_sol": "17:42:06",
        "fase_lua": "crescente_gibosa"
    },


===============================================================================
"""
import pandas as pd

#Biblioteca para gráficos
#import plotly.express as px
import plotly.graph_objects as go

def grafico_max_min(dados_previsao: dict, cols_minmax: list, title_graf: str, title_y: str ) -> go.Figure :
    #lista_a.extend(lista_b)
    
    cols_para_grafico = ["data","dia", "dia_semana"] + cols_minmax
    colmin = cols_minmax[0]
    colmax = cols_minmax[1]
    
    df = pd.DataFrame(
        [{col: item.get(col) for col in cols_para_grafico} for item in dados_previsao]
        )
    fig = go.Figure()
    # texto do eixo x
    df["eixo_x"] = df["dia"] + "<br>" + df["dia_semana"].str[:3]
    
    # Valor de mínima
    fig.add_trace(
        go.Scatter(
            x=df["eixo_x"],
            y=df[colmin],
            mode="lines+markers",
            name="Mínima",
            line=dict(
                color="#35AEEF",
                width=1.5,
            ),
            marker=dict(
                size=8,
                color="white",
                line=dict(
                    color="#35AEEF",
                    width=1.5,
                ),
            ),
            fill="tozeroy",
            fillcolor="rgba(53, 174, 239, 0.20)",
        )
    )

    # Valor de máxima
    fig.add_trace(
        go.Scatter(
            x=df["eixo_x"],
            y=df[colmax],
            mode="lines+markers",
            name="Máxima",
            line=dict(
                color="#F05A4F",
                width=1.5,
            ),
            marker=dict(
                size=8,
                color="white",
                line=dict(
                    color="#F05A4F",
                    width=1.5,
                ),
            ),
            fill="tonexty",
            fillcolor="rgba(240, 90, 79, 0.22)",
        )
    )

    fig.update_layout(
        title=title_graf,
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h",
            x=0,
            y=1.10,
        ),
        margin=dict(
            l=20,
            r=20,
            t=80,
            b=20,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        title=None,
    )

    fig.update_yaxes(
        title=title_y,
        showgrid=False,
        zeroline=False,
    )

    return fig


def grafico_chuva(dados_previsao: dict) -> go.Figure:
    cols_para_grafico = ["dia", "dia_semana", "precipitacao_mm", "probabilidade_chuva"]
    
    df = pd.DataFrame(
        [{col: item.get(col) for col in cols_para_grafico} for item in dados_previsao]
        )

    df = df.copy()

    # texto do eixo x
    df["eixo_x"] = df["dia"] + "<br>" + df["dia_semana"].str[:3]

    # altura da barra cinza
    limite = max(df["precipitacao_mm"].max(), 1)
    limite *= 1.25

    fig = go.Figure()

    # Barra de fundo
    fig.add_bar(
        x=df["eixo_x"],
        y=[limite] * len(df),
        customdata=df[
        ["precipitacao_mm","probabilidade_chuva"]
        ],
        width=0.24,
        marker=dict(
            color="#E6E6E6",
            line=dict(width=0),
        ),
       hovertemplate=(
        "<span style='color:#999999'>"
        "<b>%{x}</b>"
        "</span>"
        "<br>"
        "<span style='color:#0A84D6'>●</span> "
        "<b>☔ Prob. Chuva %{customdata[1]}%</b>"
        "<br>"
        "<span style='color:#0A84D6'>●</span> "
        "<b>🌧️ Chuva %{customdata[0]} mm</b>"
        "<extra></extra>"
    ),
        showlegend=False,
    )

    # Barra azul
    fig.add_bar(
        x=df["eixo_x"],
        y=df["precipitacao_mm"],
        customdata=df[
        ["precipitacao_mm","probabilidade_chuva"]
         ],
        width=0.24,
        marker=dict(
            color="#0A84D6",
            line=dict(width=0),
        ),
        hovertemplate=(
         "<span style='color:#999999'>"
         "<b>%{x}</b>"
         "</span>"
         "<br>"
         "<span style='color:#0A84D6'>●</span> "
         "<b>☔ Prob. Chuva %{customdata[1]}%</b>"
         "<br>"
         "<span style='color:#0A84D6'>●</span> "
         "<b>🌧️ Chuva %{customdata[0]} mm</b>"
         "<extra></extra>"
     ),
        showlegend=False,
    )

    # Valor dentro da "caixinha"
    for _, linha in df.iterrows():

        fig.add_annotation(
            x=linha["eixo_x"],
            y=max(linha["precipitacao_mm"], 0.8),
            text=f"<b>{linha['precipitacao_mm']}</b>",
            showarrow=False,
            bgcolor="white",
            bordercolor="#E4E4E4",
            borderwidth=1,
            borderpad=4,
            font=dict(
                size=13,
                color="#666666",
            ),
        )

    fig.update_layout(

        barmode="overlay",

        plot_bgcolor="white",
        paper_bgcolor="white",

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=30,
        ),

        height=450,

        xaxis=dict(
            title=None,
            showgrid=False,
            tickfont=dict(size=13),
        ),

        yaxis=dict(
            title="Milímetros (mm)",
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[0, limite],
        ),
    )

    return fig