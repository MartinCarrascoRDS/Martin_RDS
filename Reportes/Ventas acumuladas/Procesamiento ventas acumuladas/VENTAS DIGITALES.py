"""
VENTAS DIGITALES

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTAS DIGITALES

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name = 'VENTAS DIGITALES', header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer desde la columna B hasta la columna Z
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTAS DIGITALES', header = fila_inicio_2025, usecols = 'B:AB')

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

# Bloques
rds_2025 = ventas_2025.iloc[:, 0:14].copy()
rds_2025['ORIGEN'] = 'RDS DIGITAL'
rds_2025.columns = columnas
rds_2025['MONTO DE NOTAS DE CRÉDITO'] = rds_2025['MONTO DE NOTAS DE CRÉDITO'].fillna(0)

ferresol_2025 = ventas_2025.iloc[:, 14:27].copy()
ferresol_2025.insert(0, "FECHA", rds_2025["FECHA"])
ferresol_2025['ORIGEN'] = 'FERRESOL DIGITAL'
ferresol_2025.columns = columnas
ferresol_2025['MONTO DE NOTAS DE CRÉDITO'] = ferresol_2025['MONTO DE NOTAS DE CRÉDITO'].fillna(0)

# Unir
final_2025 = pd.concat([rds_2025, ferresol_2025], ignore_index = True)

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS DIGITALES'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS DIGITALES {fecha_anterior}.xlsx', index=False)


# 2026
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'VENTAS DIGITALES', header = fila_inicio_2026, usecols = 'B:AB')

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
rds_2026 = ventas_2026.iloc[:, 0:14].copy()
rds_2026['ORIGEN'] = 'RDS DIGITAL'
rds_2026.columns = columnas

ferresol_2026 = ventas_2026.iloc[:, 14:27].copy()
ferresol_2026.insert(0, "FECHA", rds_2026["FECHA"])
ferresol_2026['ORIGEN'] = 'FERRESOL DIGITAL'
ferresol_2026.columns = columnas

# Unir
final_2026 = pd.concat([rds_2026, ferresol_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_acumulados, axis = 1)

# Guardar
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS DIGITALES {fecha}.xlsx', index=False)