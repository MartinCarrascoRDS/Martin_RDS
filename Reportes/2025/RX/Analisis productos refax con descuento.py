"""
09/10/2025

Refax nos está dando descuento en 50 productos. La idea es seleccionar los 50 productos que más vendemos. Se identificarán los 50 sku más vendidos entre junio y septiembre,
y se observará cuantos de ellos están en la lista inicial de 50 sku seleccionados.
"""

import pandas as pd
import re

def obtener_multiplicador(sku):
    if isinstance(sku, str):
        match = re.search(r'[Xx](\d+)', sku)
        if match:
            return int(match.group(1))
    return 1

ventas = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/RX/Top productos XX- RX Junio - Septiembre 2025 (1).xlsx')
seleccion1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/RX/PRECIO ESPECIAL REFAX 2 (2025-10-08).xlsx')
top_skus = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/RX/Top productos XX- RX Junio - Septiembre 2025.xlsx', usecols = ['SKU_limpio'])

top_skus['Producto'] = range(1, len(top_skus) + 1)

top_skus_expand = (
    top_skus
    .assign(SKU_limpio = top_skus['SKU_limpio'].str.split(" / "))
    .explode('SKU_limpio')
    .reset_index(drop = True)
)

top_skus_expand['Multiplicador'] = top_skus_expand['SKU_limpio'].apply(obtener_multiplicador)

seleccion1 = seleccion1[seleccion1['UNICO O REPETIDO'] == 'ÚNICO']

precio_a_codigo = seleccion1.set_index('CODIGO')['PRECIO 9 SEPTIEMBRE'].to_dict()
top_skus_expand['Precio primera selección'] = top_skus_expand['SKU_limpio'].map(precio_a_codigo)
top_skus_expand['Precio primera selección'] = top_skus_expand['Precio primera selección'].fillna('No se encuentra en la primera selección')

top_skus_expand.to_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/RX/Top productos XX- RX con faltantes Junio - Septiembre 2025.xlsx', index = False)