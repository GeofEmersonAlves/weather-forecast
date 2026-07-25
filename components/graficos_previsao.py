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
    Precisei mudar os parametros de layout dos gráficos para que, na hora da conversão
do gráfico em imagem para o Excel, o layout não seja alterado, para isto os layouts foram
definidos explicitamente.

Histórico:
       21/07/2026 - Inicio 
       24/07/2026 - Ajustes no layout dos dos gráficos para que nao mudem o layout 
                na exportacao da figura para o excel
===============================================================================
"""
import pandas as pd

#Biblioteca para gráficos
import plotly.graph_objects as go

def grafico_max_min(dados_previsao: dict, cols_minmax: list, title_graf: str, title_y: str ) -> go.Figure :
    cols_para_grafico = ["data","dia", "dia_semana"] + cols_minmax
    colmin = cols_minmax[0]
    colmax = cols_minmax[1]
    
    for item in dados_previsao:
        if item[colmin] == None:
            item[colmin] = 0
        
        if item[colmax] == None:
            item[colmax] = 0    
    
    #Cria um dataframe novo só com as informações necessárias para o gráfico
    df = pd.DataFrame([{col: item.get(col) for col in cols_para_grafico} for item in dados_previsao])
    
    fig = go.Figure()

    # texto do eixo x
    df["eixo_x"] = df["dia"] + "<br>" + df["dia_semana"].str[:3]
    
    # Valor de mínima
    fig.add_trace(go.Scatter(x=df["eixo_x"],
                             y=df[colmin],
                             mode="lines+markers",
                             name="Mínima",
                             line=dict(color="#35AEEF",width=1.5),
                             marker=dict(size=10,color="white",line=dict(color="#35AEEF",width=1.5)),
                             fill="tozeroy",
                             fillcolor="rgba(53, 174, 239, 0.20)"
                             )
                  )
    
    # Valor de máxima
    fig.add_trace(go.Scatter(x=df["eixo_x"],
                             y=df[colmax],
                             mode="lines+markers",
                             name="Máxima",
                             line=dict(color="#F05A4F",width=1.5),
                             marker=dict(size=10,color="white",line=dict(color="#F05A4F",width=1.5)),
                             fill="tonexty",
                             fillcolor="rgba(240, 90, 79, 0.22)",
                            )
                )
    
    fig.update_layout(title=dict(text=f"<b>{title_graf}</b>",
                                 x=0,
                                 xanchor="left",
                                 y=0.98,
                                 yanchor="top",
                                  font=dict(family="Arial",size=20,color="#000000")
                                ),
                      font=dict(family="Arial",size=14,color="#000000"),                      
                      hovermode="x unified",
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      legend=dict(orientation="h",
                                  x=0,
                                  xanchor="left",
                                  y=1.08,
                                  yanchor="bottom",
                                  font=dict(family="Arial",size=13,color="#000000")
                                 ),
                      margin=dict(l=65,r=20,t=90,b=55)
                    )
    fig.update_xaxes(showgrid=False,
                     title=None,
                     tickfont=dict(family="Arial",size=13,color="#000000"),
                    )
    fig.update_yaxes(title=dict(text=title_y,font=dict(family="Arial",size=14,color="#000000")),
                     tickfont=dict(family="Arial",size=13,color="#000000"),
                     showgrid=False,
                     zeroline=False
                   )
    
    return fig


def grafico_chuva(dados_previsao: dict, title_graf: str) -> go.Figure:
    cols_para_grafico = ["dia", "dia_semana", "precipitacao_mm", "probabilidade_chuva"]
    
    #Codígo para o hovertemplate das barras cinza e azul
    hover_template ="<span style='color:#999999'>" \
                    "<b>%{x}</b>" \
                    "</span>" \
                    "<br>" \
                    "<span style='color:#0A84D6'>●</span>" \
                    "<b>☔ Prob. Chuva %{customdata[1]}%</b>" \
                    "<br>" \
                    "<span style='color:#0A84D6'>●</span>" \
                    "<b>🌧️ Chuva %{customdata[0]} mm</b>" \
                    "<extra></extra>"                
                     
    
    #Alguma vezes esses dados chegam como Nulos no dicionario de previsao do tempo
    for item in dados_previsao:
        if item["precipitacao_mm"] == None:
            item["precipitacao_mm"] = 0
        
        if item["probabilidade_chuva"] == None:
            item["probabilidade_chuva"] = 0   
    
    
    df = pd.DataFrame([{col: item.get(col) for col in cols_para_grafico} for item in dados_previsao])

    # texto do eixo x
    df["eixo_x"] = df["dia"] + "<br>" + df["dia_semana"].str[:3]

    #Inicio da montagem o grafico de precipitacao e probabilidade de chuva
    fig = go.Figure()

    # Altura da barra cinza de fundo.
    # Pega o valor máximo de precipitacao, e depois pega o méximo ente precipitacao e 1,
    #isso por que as vezes o valor de precipitacao vem 0 e a barra cinza nao aparece
    limite = max(df["precipitacao_mm"].max(), 1) 
    limite *= 1.25

    # Barra cinza de fundo
    fig.add_bar(x=df["eixo_x"],
                y=[limite] * len(df), #Cria uma lista tipo [limite, limite, ...] com len(df) elementos. Todas as barras com tamanho igual
                customdata=df[["precipitacao_mm","probabilidade_chuva"]],  #Campos que serão mostrados ho hovertemplate em customdata[]
                width=0.24,
                marker=dict(color="#E6E6E6",line=dict(width=0)),
                hovertemplate=(hover_template),
                showlegend=False
              )

    # Barra azul, um gráfico de barras simples
    fig.add_bar(x=df["eixo_x"],
                y=df["precipitacao_mm"],
                customdata=df[["precipitacao_mm","probabilidade_chuva"]], #Campos que serão mostrados ho hovertemplate em customdata[]
                width=0.24,
                marker=dict(color="#4E97D1",line=dict(width=0)),
                hovertemplate=(hover_template),
                showlegend=False
               )

    # Valor dentro da "caixinha"
    for _, linha in df.iterrows():
        fig.add_annotation(x=linha["eixo_x"],
                           y=max(linha["precipitacao_mm"], 0.8),
                           text=f"<b>{linha['precipitacao_mm']}</b>",
                           showarrow=False,
                           bgcolor= "rgba(255,255,255,0)", #'rgba(0,0,0,0)',  #"white",
                           bordercolor="#E4E4E4",
                           borderwidth=1,
                           borderpad=4,
                           font=dict(size=13,color="#001A5F")
                          )

    fig.update_layout(barmode="overlay",
                      title=dict(text=f"<b>{title_graf}</b>",
                                 x=0,
                                 xanchor="left",
                                 y=0.98,
                                 yanchor="top",
                                 font=dict(family="Arial",size=20,color="#000000")
                                ),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      margin=dict(l=20,r=20,t=40,b=30),
                      height=450,
                      xaxis=dict(title=None,
                                 showgrid=False,
                                 tickfont=dict(family="Arial",size=13,color="#000000")
                                ),
                      yaxis=dict(title=dict(text="Milímetros (mm)",
                                 font=dict(family="Arial",size=14,color="#000000")),
                                 tickfont=dict(family="Arial",size=13,color="#000000"),
                                 showgrid=False,
                                 showticklabels=False,
                                 zeroline=False,
                                 range=[0, limite]
                                )
                    )

    return fig