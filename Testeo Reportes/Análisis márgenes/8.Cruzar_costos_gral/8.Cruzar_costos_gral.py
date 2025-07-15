"""
Paso 8:
Cruzar los costos del resto de los productos, generando una columna "Costo_SKU_{i}" por cada columna SKU_{i} 
que se haya generado en el paso 6.
"""

import pandas as pd
import re

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/7.Cruzar_costos_full/Paso7_listo.xlsx'
hoja_venta = 'Sheet1'
archivo_costo = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/Costos para cruce.xlsx'
hoja_costo = 'Costos'

df_ventas = pd.read_excel(archivo_venta, sheet_name=hoja_venta, dtype={'# de venta': str})
df_costos = pd.read_excel(archivo_costo, sheet_name=hoja_costo, usecols = ['SKU', 'PRECIO'])

df_costos['SKU'] = df_costos['SKU'].astype(str).str.upper().str.strip()
duplicados_costos = df_costos.duplicated(subset=['SKU'], keep=False)
if duplicados_costos.any():
    df_costos_limpio = df_costos[~duplicados_costos]
    print(f"Se eliminaron {duplicados_costos.sum()} filas duplicadas en el DataFrame de costos.")

sku_a_costo = df_costos_limpio.set_index('SKU')['PRECIO'].to_dict()

sku_cols = [col for col in df_ventas.columns if re.match(r"SKU_\d+$", col)]

for col in sku_cols:
    #df_ventas[f'Costo_{col}'] = df_ventas[col].apply(lambda x: sku_a_costo.get(x.strip().upper(), None))
    df_ventas[f'Costo_{col}'] = df_ventas[col].map(sku_a_costo)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/8.Cruzar_costos_gral/Paso8_listo.xlsx'
df_ventas.to_excel(output_path, index=False)