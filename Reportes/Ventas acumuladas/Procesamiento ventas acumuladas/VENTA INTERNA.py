"""
VENTA INTERNA

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTA INTERNA

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="VENTA INTERNA", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer desde la columna B hasta la columna AB
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTA INTERNA', header = fila_inicio_2025, usecols = 'C:U')

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO",
    "UNIDADES", "ACUMULADO DE UNIDADES",
    "TICKET PROMEDIO", "CANTIDAD DE NOTAS DE CRÉDITO", "MONTO DE NOTAS DE CRÉDITO", "ORIGEN"
]

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]

# BLoques
rdsinterna_2025 = ventas_2025.iloc[:, 0:10].copy()
rdsinterna_2025['ORIGEN'] = 'RDS INTERNA'
rdsinterna_2025.columns = columnas

ferresolinterna_2025 = ventas_2025.iloc[:, 10:19].copy()
ferresolinterna_2025.insert(0, "FECHA", rdsinterna_2025["FECHA"])
ferresolinterna_2025['ORIGEN'] = 'FERRESOL INTERNA'
ferresolinterna_2025.columns = columnas

# Unir
final_2025 = pd.concat([rdsinterna_2025, ferresolinterna_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)

for col in ['MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO', 'MONTO DE NOTAS DE CRÉDITO']:
    if col in final_2025.columns:
        final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')
        final_2025[col] = (final_2025[col]).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA INTERNA'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTA INTERNA {fecha_anterior}.xlsx', index = False)

# 2026
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'VENTA INTERNA', header = fila_inicio_2026, usecols = "C:U")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
rdsinterna_2026 = ventas_2026.iloc[:, 0:10].copy()
rdsinterna_2026['ORIGEN'] = 'RDS INTERNA'
rdsinterna_2026.columns = columnas

ferresolinterna_2026 = ventas_2026.iloc[:, 10:19].copy()
ferresolinterna_2026.insert(0, 'FECHA', rdsinterna_2026['FECHA'])
ferresolinterna_2026['ORIGEN'] = 'FERRESOL INTERNA'
ferresolinterna_2026.columns = columnas

# Unir
final_2026 = pd.concat([rdsinterna_2026, ferresolinterna_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_acumulados, axis = 1)

for col in ['MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO', 'MONTO DE NOTAS DE CRÉDITO']:
    if col in final_2026.columns:
        final_2026[col] = pd.to_numeric(final_2026[col], errors = 'coerce')
        final_2026[col] = (final_2026[col]).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA INTERNA'
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTA INTERNA {fecha}.xlsx', index = False)