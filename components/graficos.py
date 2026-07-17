# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 00:01:12 2026

@author: Emerson
"""
import streamlit as st
import pandas as pd
from data.mercado_acoes import moeda_nativa

#Biblioteca para gráficos
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from plotly import data as informacoes

def grafico_area(df : pd.DataFrame, moeda : str, titulo : str):
    inicio = pd.Timestamp(df["Datetime"].iloc[0]).replace(
    hour=9, minute=0, second=0
    )

    fim = pd.Timestamp(df["Datetime"].iloc[0]).replace(
        hour=17, minute=30, second=0
    )
    
    fig = px.area(df,
                  height=300,
                  x ='Datetime',
                  y = moeda,
                  title=titulo,
                  custom_data=['Hora','Datetime'],
                  markers=True,
                  color_discrete_sequence=["#F5DEB3"] # FFFAFA B0E0E6 FFF5EE F5DEB3
                  )
   
    fig.update_yaxes(
            range=[
                df[moeda].min() ,
                df[moeda].max()* 1.001 ,
                ],
            griddash='dot',
            gridcolor='#ffffff',
            gridwidth=1
        )
    
    fig.update_xaxes(
            range=[inicio, fim],
            dtick=3600000,          # 1 hora
            tickformat="%Hh"
        )
    
    fig.update_layout(title_x=0.04,
                      title_y=0.85,
                  xaxis_title='',
                  yaxis_title='',
                  plot_bgcolor="#333333",
                  margin=dict(l=0, r=0, b=0, t=70)
                  )
    
    fig.update_yaxes(
        showticklabels=False
        )
    
    fig.update_traces(
        marker=dict(size=3),
        hovertemplate="<br>".join([
                     "<b>%{customdata[0]}</b><br>",
                     #"%{customdata[1]}"
                     "💵R$ %{y:,.4f}",
                    "<extra></extra>"
                     ])
    )
    
    
    st.plotly_chart(fig)
    
def mostrar_grafico_linha(df : pd.DataFrame):
    data_inicial = st.session_state.filtros['data_inicial']
    data_final = st.session_state.filtros['data_final']
    titulo_grafico = f"Valor no fechamento de {data_inicial:%d/%m/%Y} até {data_final:%d/%m/%Y}"                   
    
    cotacoes_close_long = df.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Valor')
    
    fig = px.line(cotacoes_close_long, 
                  x = 'Date', 
                  y = 'Valor', 
                  color = 'Ticker',
                  line_shape='spline',
                  title=titulo_grafico)
   
    titulo_eixoy=f"Valor no fechamento ({moeda_nativa(st.session_state.filtros['tickers'][0])})"             
    
    fig.update_layout(
        title_x  = 0.3,
        height=400, 
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="whitesmoke",
        font=dict(
                    family= "Arial, sans-serif", #"Courier New, monospace",
                    size=12,
                    color="black",
                    weight='bold'
                ),
        title_font=dict(
                    family= "Arial, sans-serif", #"Courier New, monospace",
                    size=16,
                    color="black",
                ),
        xaxis=dict(
                    #rangeslider=dict(
                    #    visible=True
                    #),
                    showgrid=True,          # Exibe a grade no eixo X
                    gridcolor='LightGray',  # Define a cor da linha
                    gridwidth=1 ,            # Define a espessura da linha
                    unifiedhovertitle=dict(text="<b>📅 %{x|%d/%m/%Y}</b>")
                ),
        yaxis=dict(
                showgrid=True,         # Oculta a grade no eixo Y
                gridcolor='LightGray',  # Define a cor da linha
                zeroline=True,          # Exibe a linha zero (eixo principal)
                zerolinecolor='Black',
                
            ),

        legend_title_font_color="black",
        legend_font_color="black",
        hovermode="x unified",
        xaxis_title='Data',
        yaxis_title=titulo_eixoy,
        
        hoverlabel=dict(
                bgcolor="black",
                bordercolor="#B0B0B0",
                font=dict(
                    family="Courier New, monospace",
                    size=12,
                    color="white"
                    )
                )
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E6E6E6",
        linecolor="black",
        tickfont_color="black",
        title_font_color="black",
        showspikes=True,
        spikemode='across+toaxis',
        showline=True
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E6E6E6",
        linecolor="black",
        tickfont_color="black",
        title_font_color="black",
        showspikes=True,
        spikemode='across+toaxis',
        showline=True
    )    
    
 #   fig.update_traces(
 #       hovertemplate="<br>".join([
 #                    "<b>%{fullData.name}</b><br>"
 #                    "📅 %{x|%d/%m/%Y}<br>"
 #                    "💰 Fechamento: R$ %{y:,.2f}"
 #                    "<extra></extra>"
 #                    ])
 #   )
    for trace in fig.data:
        trace.hovertemplate = (
            f"<b><span style='color:{trace.line.color};'>{trace.name}</span></b><br>"
            "💰R$ %{y:,.2f}"
            "<extra></extra>"
        )
    
    st.plotly_chart(fig)

#https://plotly.com/python/hover-text-and-formatting/
def grafico_cotacoes_moedas(df : pd.DataFrame):
    colunas_moedas = df.columns.drop("Data")
    fig = make_subplots(
        rows=4,
        cols=2,
        subplot_titles=colunas_moedas.tolist()
    )

    for i, moeda in enumerate(colunas_moedas):
        linha = i // 2 + 1
        coluna_subplot = i % 2 + 1

        fig.add_trace(
            go.Scatter(
                x=df["Data"],
                y=df[moeda],
                name=moeda,
            ),
            row=linha,
            col=coluna_subplot,
        )

    fig.update_layout(
        title="Cotação das principais moedas",
        height=1000,
        hovermode="x unified",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)
    