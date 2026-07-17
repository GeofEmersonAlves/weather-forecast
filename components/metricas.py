# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 23:06:33 2026

@author: Emerson
"""
import streamlit as st
import pandas as pd
from typing import Any, List
from data.mercado_acoes import moeda_nativa

def calcula_variacao_moedas(df : pd.DataFrame) -> dict[str, float] :
   variacoes = {}

   for coluna in df.columns.drop("Datetime"):
       serie = df[coluna].dropna()

       if len(serie) >= 2:
           variacoes[coluna] = (
               (serie.iloc[-1] / serie.iloc[-2] - 1) * 100
           )
       else:
           variacoes[coluna] = None

   return variacoes

@st.cache_data
def calcular_kpis(df: pd.DataFrame, tickers: list[str]) -> dict[str, Any]:
    fechamento = df["Close"].iloc[-1]
    volume = df["Volume"].iloc[-1]
    variacao = df["Close"].pct_change().iloc[-1]

    menor_variacao = variacao.min()

    return dict(
        qtde_tickers=len(tickers),

        preco_medio=fechamento.mean(),
        variacao_media=variacao.mean(),

        melhor_fechamento_empresa=fechamento.idxmax(),
        melhor_fechamento_valor=fechamento.max(),

        maior_alta_empresa=variacao.idxmax(),
        maior_alta_valor=variacao.max(),

        menor_variacao_empresa=variacao.idxmin(),
        menor_variacao_valor=menor_variacao,
        menor_variacao_label="📉Maior queda" if menor_variacao < 0 else "📈Menor alta",

        volume_total=volume.sum(),
        volume_medio=volume.mean()
    )


    
def mostrar_metricas_tickers(df_metricas: pd.DataFrame, tickers : List):
    if len(tickers) == 1: #Apenas um ticker selecionado
       acao_unica=tickers[0]
       
       serie = df_metricas[acao_unica]
       
       preco_atual = serie.iloc[-1]
       preco_ontem = serie.iloc[-2]
       preco_iniper = serie.iloc[0]

       #Mais elegante
       variacao_hoje = preco_atual / preco_ontem - 1
       variacao_periodo = preco_atual / preco_iniper - 1
       """ Forma convencional
          variacao_hoje = (preco_atual - preco_ontem) / preco_ontem
          variacao_periodo = (preco_atual - preco_iniper) / preco_iniper
       """
       
       preco_maximo = serie.max()
       preco_minimo = serie.min()
       data_maximo = serie.idxmax().strftime("%d/%m/%Y")
       data_minimo = serie.idxmin().strftime("%d/%m/%Y")
       
       moeda = moeda_nativa(acao_unica)
       
       col1, col2, col3,col4 = st.columns(4)
       with col1:  #KPI Preço atual
           
           st.metric("💰Preço atual",
                     value=f"{preco_atual:,.2f} {moeda}",
                     delta=f"{variacao_hoje:.1%} hoje"
                     )
       with col2:
            
            st.metric("🏁Preço inicial",
                     value=f"{preco_iniper:,.2f} {moeda}",
                     delta=f"{variacao_periodo:.1%} no período"
                      )
       with col3:
            
            st.metric("📈Máxima",
                      value=f"{preco_maximo:,.2f} {moeda}",
                      delta=f"{data_maximo}",
                      delta_color ="green",
                      delta_arrow ="off"
                      )
       with col4:
            
            st.metric("📉Mínima",
                      value=f"{preco_minimo:,.2f} {moeda}",
                      delta=f"{data_minimo}",
                      delta_color ="red",
                      delta_arrow ="off"
                      )

        
    elif len(tickers) > 1:
        kpis = calcular_kpis(df_metricas, tickers)
        
        col1, col2, col3,col4 = st.columns(4)
        with col1:
            st.metric("📈Empesas",
                      value = f"{kpis['qtde_tickers']}",
                      delta = f"Melhor ticker: {kpis['melhor_fechamento_empresa']}",
                      delta_color ="green",
                      delta_arrow ="off"
                      )
        with col2:
            st.metric('🚀Maior Alta',
                      value = f"{kpis['maior_alta_empresa']}",
                      delta = f"{kpis['maior_alta_valor']:.2%}",
                      delta_color ="green"
                      )
        with col3:
            st.metric(label=kpis["menor_variacao_label"],
                        value = kpis['menor_variacao_empresa'],
                        delta = f"{kpis['menor_variacao_valor']:.2%}",
                        delta_color ="red"
                        )
        with col4:
            st.metric("🥇Maior fechamento",
                      value = kpis['melhor_fechamento_empresa'],
                      delta = f"{kpis['melhor_fechamento_valor']:.2f}"
                      )

            
def mostrar_metricas_moedas(df_metricas: pd.DataFrame):
    variacoes=calcula_variacao_moedas(df_metricas)
    
    usd = df_metricas['USD'].dropna().iloc[-1]
    ars = df_metricas['ARS'].dropna().iloc[-1] 
    eur = df_metricas['EUR'].dropna().iloc[-1] 
    btc = df_metricas['BTC'].dropna().iloc[-1] 
    #st.write(usd)
    #st.json(variacoes)
    
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        st.metric('💵DOLAR COM.',
                  value = f"R$ {usd:,.3f}",
                  delta = f"{variacoes['USD']:.2%}"
                  )  
    with col2:
        st.metric('💵PESO Arg.',
                  value = f"R$ {ars:,.3f}",
                  delta = f"{variacoes['ARS']:.2%}"
                  )
    with col3:
        st.metric('💶EURO',
                  value = f"R$ {eur:,.3f}",
                  delta = f"{variacoes['EUR']:.2%}"
                  )
    with col4:
        st.metric('🪙BITCOIN',
                  value = f"US$ {btc:,.2f}",
                  delta = f"{variacoes['BTC']:.2%}"
                  )
    
    