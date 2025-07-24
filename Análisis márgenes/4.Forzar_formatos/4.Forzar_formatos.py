"""
Paso 4:
Forzar formato fecha en columna Fecha de venta
Forzar formato numérico en columnas numéricas
"""

import pandas as pd
import re
import numpy as np

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/Paso3_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, hoja_venta, dtype = {'# de venta': str})

meses_es = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

def convertir_fechas(fecha_str):
    if pd.isna(fecha_str):
        return pd.NaT
    try:
        fecha_str = str(fecha_str).lower()
        fecha_str = re.sub(r"\s*hs\.?", "", fecha_str)
        partes = fecha_str.split(' de ')
        if len(partes) < 3:
            return pd.NaT
        dia = partes[0].strip().zfill(2)
        mes = meses_es.get(partes[1].strip(), '01')
        año_hora = partes[2].strip()
        año = año_hora.split()[0]
        return pd.to_datetime(f"{año}/{mes}/{dia}", format="%Y/%m/%d")
    except Exception:
        return pd.NaT
    
df = df[df['SKU'].notna() & df['Cargo por venta e impuestos (CLP)'].notna()]  

if 'Fecha de venta' in df.columns:
    df['Fecha de venta'] = df['Fecha de venta'].apply(convertir_fechas)

columnas_numericas = [
    'Unidades', 'Ingresos por productos (CLP)', 'Cargo por venta e impuestos (CLP)',
    'Ingresos por envío (CLP)', 'Costos de envío (CLP)'
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors = 'coerce')
    if col in ['Ingresos por envío (CLP)', 'Costos de envío (CLP)']:
        df[col] = df[col].fillna(0)
    if col in ['Ingresos por productos (CLP)', 'Cargo por venta e impuestos (CLP)',
               'Ingresos por envío (CLP)', 'Costos de envío (CLP)']:
        df[f"{col} Neto"] = df[col] / 1.19

df['Costo final envío (CLP) Neto'] = df.apply(lambda row: 3500 if row['Forma de entrega'] == 'Mercado Envíos Flex' else - (row['Costos de envío (CLP) Neto'] + row['Ingresos por envío (CLP) Neto']), axis=1)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/4.Forzar_formatos/Paso4_listo.xlsx'

df.to_excel(output_path, index = False)

