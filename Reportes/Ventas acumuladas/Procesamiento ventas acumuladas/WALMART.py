"""
WALMART

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja WALMART

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# Leer desde la columna B hasta la columna M
ventas_2024 = pd.read_excel(path_ventas, sheet_name = 'WALMART', header = 6, usecols = "B:M")

# Limpiar fechas
ventas_2024['FECHA'] = pd.to_datetime(ventas_2024['FECHA'], errors = 'coerce')
ventas_2024 = ventas_2024.dropna(subset = ["FECHA"])
ventas_2024 = ventas_2024[ventas_2024['FECHA'].dt.year == 2024]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "ORIGEN"
]

columnas2 = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "ORIGEN"
]

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]

walmart_2024 = ventas_2024.copy()
walmart_2024['ORIGEN'] = 'WALMART'
walmart_2024.columns = columnas
walmart_2024 = walmart_2024.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    walmart_2024[col] = pd.to_numeric(walmart_2024[col], errors = 'coerce')

walmart_2024['CANTIDAD DE VENTAS'] = (walmart_2024['CANTIDAD DE VENTAS'] * 0.9).round(0).astype(int)
walmart_2024['MONTO DE VENTAS'] = walmart_2024['MONTO DE VENTAS'] * 0.9
walmart_2024['UNIDADES'] = (walmart_2024['UNIDADES'] * 0.9).round(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/WALMART'
walmart_2024.to_excel(f'{output_folder}/VENTAS ACUMULADAS WALMART {fecha_anterior}.xlsx', index = False)

# 2025

# Leer desde la columna B hasta la columna W
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'WALMART', header = 42, usecols = "B:W")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

# Bloques
walmart_2025 = ventas_2025.iloc[:, 0:12].copy()
walmart_2025['ORIGEN'] = 'WALMART'
walmart_2025.columns = columnas

walmartneuma_2025 = ventas_2025.iloc[:, 12:22].copy()
walmartneuma_2025.insert(0, 'FECHA', walmart_2025['FECHA'])
walmartneuma_2025['ORIGEN'] = 'WALMART NEUMA'
walmartneuma_2025.columns = columnas2

# Unir
walmart_2025 = pd.concat([walmart_2025, walmartneuma_2025], ignore_index = True)
walmart_2025 = walmart_2025.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    walmart_2024[col] = pd.to_numeric(walmart_2024[col], errors = 'coerce')

walmart_2025['CANTIDAD DE VENTAS'] = (walmart_2025['CANTIDAD DE VENTAS'] * 0.90).round(0).astype(int)
walmart_2025['MONTO DE VENTAS'] = walmart_2025['MONTO DE VENTAS'] * 0.90
walmart_2025['UNIDADES'] = (walmart_2025['UNIDADES'] * 0.90).round(0).astype(int)

# Guardar
walmart_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS WALMART {fecha}.xlsx', index = False)