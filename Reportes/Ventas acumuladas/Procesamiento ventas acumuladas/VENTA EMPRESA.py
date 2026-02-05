"""
VENTA EMPRESA

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTA EMPRESA

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="VENTA EMPRESA", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer desde la columna C hasta la columna AC
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTA EMPRESA', header = fila_inicio_2025, usecols = 'C:AC')

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO",
    "CANTIDAD DE NOTAS DE CRÉDITO", "MONTO DE NOTAS DE CRÉDITO", "ORIGEN"
]

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]

# BLoques
rdsempresa_2025 = ventas_2025.iloc[:, 0:14].copy()
rdsempresa_2025['ORIGEN'] = 'RDS EMPRESA'
rdsempresa_2025.columns = columnas

ferresolempresa_2025 = ventas_2025.iloc[:, 14:27].copy()
ferresolempresa_2025.insert(0, "FECHA", rdsempresa_2025["FECHA"])
ferresolempresa_2025['ORIGEN'] = 'FERRESOL EMPRESA'
ferresolempresa_2025.columns = columnas

# Unir
final_2025 = pd.concat([rdsempresa_2025, ferresolempresa_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)

for col in ['MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO', 'MONTO DE NOTAS DE CRÉDITO']:
    if col in final_2025.columns:
        final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')
        final_2025[col] = (final_2025[col]).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA EMPRESA'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTA EMPRESA {fecha_anterior}.xlsx', index = False)

# 2026

# Leer desde la columna C hasta la columna AC
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'VENTA EMPRESA', header = fila_inicio_2026, usecols = "C:AC")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
rdsempresa_2026 = ventas_2026.iloc[:, 0:14].copy()
rdsempresa_2026['ORIGEN'] = 'RDS EMPRESA'
rdsempresa_2026.columns = columnas

ferresolempresa_2026 = ventas_2026.iloc[:, 14:27].copy()
ferresolempresa_2026.insert(0, 'FECHA', rdsempresa_2026['FECHA'])
ferresolempresa_2026['ORIGEN'] = 'FERRESOL EMPRESA'
ferresolempresa_2026.columns = columnas


# Unir
final_2026 = pd.concat([rdsempresa_2026, ferresolempresa_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_acumulados, axis = 1)

for col in ['MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO', 'MONTO DE NOTAS DE CRÉDITO']:
    if col in final_2026.columns:
        final_2026[col] = pd.to_numeric(final_2026[col], errors = 'coerce')
        final_2026[col] = (final_2026[col]).round(0).fillna(0).astype(int)

# Guardar
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTA EMPRESA {fecha}.xlsx', index = False)
