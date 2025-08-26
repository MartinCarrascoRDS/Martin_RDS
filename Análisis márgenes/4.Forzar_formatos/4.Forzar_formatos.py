"""
Paso 4:
Forzar formato fecha en columna Fecha de venta
Forzar formato numérico en columnas numéricas
"""

import pandas as pd
import re
import numpy as np

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
estados = input('¿Filtraste los estados en el paso anterior? (True si lo hiciste, False si no): ').strip()
año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS

if estados.lower() == 'true':
    estados_filtrados = True
elif estados.lower() == 'false':
    estados_filtrados = False
else:
    raise ValueError('Por favor ingresa un valor válido de estados filtrados (TRUE O FALSE)')

if estados_filtrados:
    archivo_venta = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/{año}/{fecha}/Paso3_{cuenta_meli}_{fecha}_listo.xlsx'
    hoja_venta = 'Sheet1'
else:
    archivo_venta = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/{año}/{fecha}/Paso3_{cuenta_meli}_{fecha}_omitido.xlsx'
    hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, hoja_venta, dtype = {'# de venta': str})
    
df = df[df['SKU'].notna() & df['Cargo por venta e impuestos (CLP)'].notna() & df['Ingresos por productos (CLP)'].notna()]

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

df['Costo final envío (CLP) Neto'] = df.apply(lambda row: 3500 / 1.19 - row['Ingresos por envío (CLP) Neto'] if row['Forma de entrega'] == 'Mercado Envíos Flex' else - (row['Costos de envío (CLP) Neto'] + row['Ingresos por envío (CLP) Neto']), axis=1)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/4.Forzar_formatos/Paso4_listo.xlsx'

df.to_excel(output_path, index = False)

