"""
Paso 9:
Aplicar descuentos a los costos de productos según un rango de fechas y un diccionario de descuentos por importadora.
Se generará una nueva columna "Costo_post_dcto_SKU_{i}" por cada columna SKU_{i} que se haya generado en el paso 6.
La función 'aplicar_descuentos', junto con el diccionario 'descuentos_importadoras' se encargarán de este proceso.
Ambos se encuentran en recursos_proyectos/pipeline/finanzas/descuentos.py.
"""

import pandas as pd
import numpy as np
from pipeline.finanzas.descuentos import aplicar_descuentos, descuentos_importadoras

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/8.Cruzar_costos_gral/Paso8_listo.xlsx'
hoja_venta = 'Sheet1'

df_ventas = pd.read_excel(archivo_venta, sheet_name=hoja_venta, dtype={'# de venta': str})

ACTIVAR_DESCUENTOS = True  # Cambia a False si no quieres aplicar descuentos

fecha_inicio = pd.Timestamp('2025-06-02')
fecha_fin = pd.Timestamp('2025-06-08')

df_ventas = aplicar_descuentos(
    df_ventas,
    fecha_col='Fecha de venta',
    fecha_inicio=fecha_inicio,
    fecha_fin=fecha_fin,
    descuentos_dict=descuentos_importadoras,
    activar = ACTIVAR_DESCUENTOS
)

sku_cols = [col for col in df_ventas.columns if col.startswith("SKU_") and col[-1].isdigit()]

if ACTIVAR_DESCUENTOS:
    columnas_costos = [f"Costo_post_dcto_{col}" for col in sku_cols]
else:
    columnas_costos = [f"Costo_{col}" for col in sku_cols]

def calcular_costo_final(row):
    if row['Forma de entrega'] == 'Mercado Envíos Full':
        return row['Costo_full']
    else:
        valores = [row[col] for col in columnas_costos if col in row and pd.notna(row[col])]
        if len(valores) == 0:
            return np.nan
        return sum(valores)

df_ventas['Costo_final_producto'] = df_ventas.apply(calcular_costo_final, axis=1)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/9.Descuentos/Paso9_listo.xlsx'
df_ventas.to_excel(output_path, index=False)