"""
Paso 6:
Separar los SKU de cada uno de los productos en distintas columnas según el separador " / ".
"""

import pandas as pd

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/5.Limpieza_sku/Paso5_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str})

sku_split = df['SKU'].str.split(" / ", expand = True)

#Pendiente, mirar último chat con ChatGPT