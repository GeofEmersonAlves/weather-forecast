# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : Weather Forecast
Arquivo    : time_zone.py
Autor      : Emerson
Data       : Mon Jul 27 14:49:41 2026
Versão     : 1.0
Python     : Python 3.13.14 | packaged by Anaconda, Inc. 

Descrição:
        Serviço criado para resolver o problema dos timezone dos horários, como o app
    esta online e pode ser acessado de qualquer lugar, surguiu este problema
      
#pip install timezonefinder
Histórico:
       27/07/2026 - Inicio 
===============================================================================
"""
from datetime import datetime, date
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

def hora_brasilia_to_fuso_local(hora_brasilia: str, lat : float, long: float) -> str:
    
    hora_brasilia = datetime.strptime(hora_brasilia, "%H:%M:%Sh").time()
    
    dt_brasilia = datetime.combine(date.today(), hora_brasilia)
    
    # Torne o objeto datetime "ciente" do fuso de Brasília (-03:00)
    tz_brasilia = ZoneInfo("America/Sao_Paulo")
    dt_brasilia = dt_brasilia.replace(tzinfo=tz_brasilia)

    # 3. Descubra o fuso horário local com base nas coordenadas (lat/long)
    tf = TimezoneFinder()
    nome_fuso_local = tf.timezone_at(lat = lat, lng=long) 
    
    tz_local = ZoneInfo(nome_fuso_local)
    hora_local = dt_brasilia.astimezone(tz_local)
    
    return hora_local.strftime('%H:%M:%S')