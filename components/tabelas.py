# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 22:17:15 2026

@author: Emerson
"""
#pip install streamlit-aggrid
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from typing import Any

custom_css = {
    ".ag-root-wrapper": {
        "border": "1px solid #C0C0C0"
    },
    ".ag-header-cell": {
        "border-right": "1px solid #CFCFCF"
    },
    ".ag-cell": {
        "border-right": "1px solid #E0E0E0"
    }
}

locale_text = {
    "equals": "Igual",
    "notEqual": "Diferente",

    "greaterThan": "Maior que",
    "greaterThanOrEqual": "Maior ou igual a",
    "lessThan": "Menor que",
    "lessThanOrEqual": "Menor ou igual a",
    "inRange": "Entre",

    "blank": "Em branco",
    "notBlank": "Não em branco",

    "contains": "Contém",
    "notContains": "Não contém",
    "startsWith": "Começa com",
    "endsWith": "Termina com",

    "filterOoo": "Filtrar...",
    "searchOoo": "Pesquisar...",
    "selectAll": "Selecionar tudo",
    "blanks": "Vazios",

    "sortAscending": "Ordenar crescente",
    "sortDescending": "Ordenar decrescente",
    "pinColumn": "Fixar coluna",
    "autosizeThiscolumn": "Ajustar esta coluna",
    "autosizeAllColumns": "Ajustar todas as colunas",

    "copy": "Copiar",
    "copyWithHeaders": "Copiar com cabeçalhos",
    "export": "Exportar",
    "csvExport": "Exportar CSV",
}

def criar_column_config(df : pd.DataFrame) -> dict[str, Any]:
    dict_config={
        'Date' : st.column_config.DateColumn("Data", format='DD/MM/YYYY'),
        **{coluna: st.column_config.NumberColumn(format="R$ %,.2f")  for coluna in df.columns[1:]}
      }
    
    return dict_config


def mostrar_dataframe_multiindex(df : pd.DataFrame) -> dict:
    df_vis = df.copy()
    
    df_vis.columns = [ f"{preco} - {ticker}"  if len(ticker) > 0  else f"{preco}"
                        for preco, ticker in df_vis.columns]
    
    configuracao = criar_column_config(df_vis)
    selecao = st.dataframe(df_vis,
                     height = 350,
                     hide_index = True,
                     width = "stretch",
                     placeholder = '-',
                     on_select="rerun",
                     selection_mode = "multi-row",
                     row_height =40,
                     column_config = configuracao
                     )
    return selecao
    
   
def mostrar_tabela_like_excel(tabela: pd.DataFrame, chave="tabela_aggrid"):
    df = tabela.reset_index().rename(columns={"index": "Data"})
    
    gb = GridOptionsBuilder.from_dataframe(df)
    
    gb.configure_default_column(
        editable=False,
        groupable=False,
        sortable=True,
        filter=True,
        resizable=True,
        floatingFilter=False,
    )

    for coluna in  df.columns[1:]:
        gb.configure_column(
            coluna,
            type=["numericColumn"],
            valueFormatter="x.toFixed(2)"
        )
    
    grid_options = gb.build()
    grid_options["localeText"] = locale_text

    # seleção e cópia
    grid_options["rowSelection"] = "multiple"
    grid_options["enableRangeSelection"] = True
    grid_options["enableCellTextSelection"] = True
    grid_options["suppressCopyRowsToClipboard"] = False
    
    AgGrid(
        df,
        gridOptions=grid_options,
        theme="balham",
        custom_css=custom_css,
        height=min(len(tabela)*28,600),
        fit_columns_on_grid_load=True,
        reload_data=False,
        update_on=[],
        key=chave,
    )

#theme="balham" alpine