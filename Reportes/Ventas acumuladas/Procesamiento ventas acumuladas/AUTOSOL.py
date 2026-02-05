"""
AUTOSOL

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja AUTOSOL

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="AUTOSOL", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'AUTOSOL', header = fila_inicio_2025, usecols = "B:O")

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "CANTIDAD DE NOTAS DE CRÉDITO", "MONTO DE NOTAS DE CRÉDITO", "ORIGEN"
]

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]

serviteca_2025 = ventas_2025.copy()
serviteca_2025['ORIGEN'] = 'SERVITECA'
serviteca_2025.columns = columnas
serviteca_2025 = serviteca_2025.drop(columns = columnas_acumulados, axis = 1)

for col in ['MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO', 'MONTO DE NOTAS DE CRÉDITO']:
    if col in serviteca_2025.columns:
        serviteca_2025[col] = pd.to_numeric(serviteca_2025[col], errors = 'coerce')
        serviteca_2025[col] = (serviteca_2025[col]).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/AUTOSOL'
serviteca_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS AUTOSOL {fecha_anterior}.xlsx', index = False)

# 2026

fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'AUTOSOL', header = fila_inicio_2026, usecols = "B:O")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

serviteca_2026 = ventas_2026.copy()
serviteca_2026['ORIGEN'] = 'SERVITECA'
serviteca_2026.columns = columnas
serviteca_2026 = serviteca_2026.drop(columns = columnas_acumulados, axis = 1)

for col in ['MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO', 'MONTO DE NOTAS DE CRÉDITO']:
    if col in serviteca_2026.columns:
        serviteca_2026[col] = pd.to_numeric(serviteca_2026[col], errors = 'coerce')
        serviteca_2026[col] = (serviteca_2026[col]).round(0).fillna(0).astype(int)

# Guardar
serviteca_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS AUTOSOL {fecha}.xlsx', index = False)