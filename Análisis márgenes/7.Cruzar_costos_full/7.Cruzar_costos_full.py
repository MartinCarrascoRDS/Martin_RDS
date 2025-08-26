"""
Paso 7:
Cruzar los costos de los productos que se venden en Full, generando una nueva columna llamada "Costo_full".
"""

import pandas as pd
import re

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/6.Separar_sku/Paso6_listo.xlsx'
hoja_venta = 'Sheet1'
archivo_costo = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/COSTOS PARA CRUCE/Costos para cruce al 2025-13-08.xlsx'
hoja_costo = 'CostosFull'

df_ventas = pd.read_excel(archivo_venta, sheet_name=hoja_venta, dtype={'# de venta': str})
df_costos = pd.read_excel(archivo_costo, sheet_name=hoja_costo)

df_costos['SKU'] = df_costos['SKU'].astype(str).str.upper().str.strip()

df_costos_limpio = df_costos[['SKU', 'PRECIO CONFIRMADO']].copy()

duplicados_ventas = df_ventas.duplicated(subset=['# de venta'], keep='first')
if duplicados_ventas.any():
    df_ventas = df_ventas[~duplicados_ventas]
    print(f"Se eliminaron {duplicados_ventas.sum()} filas duplicadas en el DataFrame de ventas.")

duplicados_costos = df_costos_limpio.duplicated(subset=['SKU'], keep='first')
if duplicados_costos.any():
    df_costos_limpio = df_costos_limpio[~duplicados_costos]
    print(f"Se eliminaron {duplicados_costos.sum()} filas duplicadas en el DataFrame de costos.")


"""
ESTE MÉTODO FUE USADO CUANDO LA BASE DE COSTOS PARA PRODUCTOS EN FULL NO TENÍA SEPARACIÓN POR SKU EN CASO DE PRODUCTOS CON + DE 1 SKU
df_ventas = pd.merge(
    df_ventas,
    df_costos_limpio,
    how='left',
    left_on='SKU_MAYUSC',
    right_on='SKU'
)

df_ventas = df_ventas.rename(columns={'Costo': 'Costo_full', 'SKU_x': 'SKU', 'SKU_y': 'SKU_costo'})

df_ventas = df_ventas.drop(columns=['SKU_costo'])
"""

# A continuación, un método similar al del paso 8, que considera costos para sku individuales
sku_a_costo = df_costos_limpio.set_index('SKU')['PRECIO CONFIRMADO'].to_dict()

sku_cols = [col for col in df_ventas.columns if re.match(r"SKU_\d+$", col)]

for col in sku_cols:
    df_ventas[f'Costo_full_{col}'] = df_ventas[col].map(sku_a_costo)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/7.Cruzar_costos_full/Paso7_listo.xlsx'
df_ventas.to_excel(output_path, index=False)

