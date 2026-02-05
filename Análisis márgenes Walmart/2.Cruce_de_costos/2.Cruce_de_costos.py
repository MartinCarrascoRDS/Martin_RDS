"""
Paso 2: Separar ventas de devoluciones del df de ventas totales
Determinar el % en $ de devoluciones del total de transacciones
Al df de ventas (sin devoluciones) incorporar descuentos, costos del producto y costos logísticos (por venta, no por sku)
"""

import pandas as pd
import os
from pipeline.procesamiento.funciones_para_analisis_margen import limpiar_sku_walmart
import re

año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS
cuenta_walmart = input('Indique la cuenta de Walmart a la que corresponde este análisis (WALMART REPUESTOS O WALMART NEUMA): ')
fecha = input('Indique la fecha del análisis (ejemplo: OCTUBRE 2025): ')

def extraer_multiplicador(sku):
    if not isinstance(sku, str):
        return 1
    match = re.search(r'X(\d+)\s*$', sku.strip().upper())
    if match:
        return int(match.group(1))
    else:
        return 1

def eliminar_multiplicador_final(sku):
    if not isinstance(sku, str):
        return sku
    # Elimina " X2", " X10", etc. al final del SKU
    return re.sub(r'\s*X\d+\s*$', '', sku.strip().upper())

direc_ventas_totales = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes Walmart/1.Leer_df_y_subdivisiones/{año}/{fecha}/{fecha} {cuenta_walmart} VENTAS TOTALES.xlsx'
direc_envios = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes Walmart/1.Leer_df_y_subdivisiones/{año}/{fecha}/{fecha} {cuenta_walmart} COSTOS DE ENVÍO.xlsx'
direc_costos_sku = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Walmart/COSTOS PARA CRUCE/Costos para cruce al 2025-12-01.xlsx'

walmart = pd.read_excel(direc_ventas_totales, dtype = {"SG": str, "Orden": str})
envios = pd.read_excel(direc_envios, dtype = {"SG": str, "Orden": str})
costos_sku = pd.read_excel(direc_costos_sku, usecols = ['SKU', 'PRECIO'], sheet_name = 'Costos')
for df in [walmart, envios, costos_sku]:
    df.drop(columns=[col for col in df.columns if "Unnamed" in col], inplace=True)

ventas = walmart.loc[walmart['Ingreso por venta neto'] > 0, "Ingreso por venta neto"].sum()
devoluciones = walmart.loc[walmart['Ingreso por venta neto'] < 0, "Ingreso por venta neto"].abs().sum()
porcentaje_devol = (devoluciones / ventas) * 100

print(f"Ventas totales: {ventas:,.0f}")
print(f"Devoluciones totales: {devoluciones:,.0f}")
print(f"Porcentaje de devoluciones: {porcentaje_devol:.2f}%")

walmart_ventas = walmart[walmart['Estado'] == 'Enviado']
walmart_envios = envios[envios['Estado'] == 'Enviado']

walmart_ventas['SKU_limpio'] = walmart_ventas['SKU'].apply(limpiar_sku_walmart)
walmart_ventas['Multiplicador'] = walmart_ventas['SKU_limpio'].apply(extraer_multiplicador)
walmart_ventas['SKU_limpio2'] = walmart_ventas['SKU_limpio'].apply(eliminar_multiplicador_final)
costos_sku['SKU'] = costos_sku['SKU'].apply(limpiar_sku_walmart)
duplicados_costos = costos_sku.duplicated(subset=['SKU'], keep='first')
print(f'cantidad de costos duplicados: {duplicados_costos.sum()}')
if duplicados_costos.any():
    costos_sku = costos_sku[~duplicados_costos]
    print(f"Se eliminaron {duplicados_costos.sum()} filas duplicadas en el DataFrame de costos.")

sku_a_costo = costos_sku.set_index('SKU')['PRECIO'].to_dict()
walmart_ventas['Costo SKU neto'] = walmart_ventas['SKU_limpio2'].map(sku_a_costo) * walmart_ventas['Multiplicador']

walmart_ventas = walmart_ventas.merge(
    walmart_envios[['SG', 'Orden', 'Costo logístico neto']],
    on = ['SG', 'Orden'],
    how = 'left'
)

"""walmart_ventas['Costo logístico neto'] = walmart_ventas['Costo logístico neto'].fillna(walmart_ventas['Costo logístico neto'].mean())"""
walmart_ventas['Costo logístico neto'] = walmart_ventas['Costo logístico neto'].fillna(0)

walmart_ventas['Total venta por SG'] = walmart_ventas.groupby(['SG', 'Orden'])['Ingreso por venta neto'].transform('sum')
walmart_ventas['Prop_venta'] = walmart_ventas['Ingreso por venta neto']/walmart_ventas['Total venta por SG']

walmart_ventas['Costo logístico neto prorrateado'] = walmart_ventas['Prop_venta'] * walmart_ventas['Costo logístico neto']

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes Walmart/2.Cruce_de_costos/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)

output_path_walmart_ventas = f'{output_folder}/{fecha} {cuenta_walmart} VENTAS SIN DEVOLUCIÓN.xlsx'
output_path_walmart_envios = f'{output_folder}/{fecha} {cuenta_walmart} ENVIOS SIN DEVOLUCIÓN.xlsx'
walmart_ventas.to_excel(output_path_walmart_ventas, index = False)
walmart_envios.to_excel(output_path_walmart_envios, index = False)