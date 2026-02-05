"""
VENTAS RIPLEY

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTAS RIPLEY

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="VENTAS RIPLEY", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer desde la columna C hasta la columna N
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTAS RIPLEY', header = fila_inicio_2025, usecols = "C:N")

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "ORIGEN"
]

ripley_2025 = ventas_2025.copy()
ripley_2025['ORIGEN'] = 'RIPLEY'
ripley_2025.columns = columnas

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]
ripley_2025 = ripley_2025.drop(columns = columnas_acumulados, axis = 1)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS RIPLEY'
ripley_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS RIPLEY {fecha_anterior}.xlsx', index = False)


# 2026

# Leer desde la columna C hasta la columna N
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'VENTAS RIPLEY', header = fila_inicio_2026, usecols = "C:N")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

ripley_2026 = ventas_2026.copy()
ripley_2026['ORIGEN'] = 'RIPLEY'
ripley_2026.columns = columnas
ripley_2026 = ripley_2026.drop(columns = columnas_acumulados, axis = 1)

# Guardar
ripley_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS RIPLEY {fecha}.xlsx', index = False)
