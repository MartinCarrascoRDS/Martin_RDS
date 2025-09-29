"""
VENTAS DIGITALES

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTAS DIGITALES

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# Leer desde la columna B hasta la columna Z
ventas_2024 = pd.read_excel(path_ventas, sheet_name = 'VENTAS DIGITALES ', header = 7, usecols = 'B:Z')

# Limpiar fechas
ventas_2024['FECHA'] = pd.to_datetime(ventas_2024['FECHA'], errors = 'coerce')
ventas_2024 = ventas_2024.dropna(subset = ["FECHA"])
ventas_2024 = ventas_2024[ventas_2024['FECHA'].dt.year == 2024]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO",
    "CANTIDAD DE NOTAS DE CRÉDITO", "MONTO DE NOTAS DE CRÉDITO", "ORIGEN"
]

columnas2 = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "ORIGEN"
]

# Bloques
rds_2024 = ventas_2024.iloc[:, 0:14].copy()
rds_2024['ORIGEN'] = 'RDS DIGITAL'
rds_2024.columns = columnas

ferresol_2024 = ventas_2024.iloc[:, 14:25].copy()
ferresol_2024.insert(0, "FECHA", rds_2024["FECHA"])
ferresol_2024['ORIGEN'] = 'FERRESOL DIGITAL'
ferresol_2024.columns = columnas2

# Unir
final_2024 = pd.concat([rds_2024, ferresol_2024], ignore_index = True)

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]
final_2024 = final_2024.drop(columns = columnas_acumulados, axis = 1)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS DIGITALES'
final_2024.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS DIGITALES {fecha_anterior}.xlsx', index=False)


# 2025

# Leer desde la columna B hasta la columna AB
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTAS DIGITALES ', header = 45, usecols = 'B:AB')

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

# Bloques
rds_2025 = ventas_2025.iloc[:, 0:14].copy()
rds_2025['ORIGEN'] = 'RDS DIGITAL'
rds_2025.columns = columnas

ferresol_2025 = ventas_2025.iloc[:, 14:27].copy()
ferresol_2025.insert(0, "FECHA", rds_2025["FECHA"])
ferresol_2025['ORIGEN'] = 'FERRESOL DIGITAL'
ferresol_2025.columns = columnas

# Unir
final_2025 = pd.concat([rds_2025, ferresol_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)

# Guardar
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS DIGITALES {fecha}.xlsx', index=False)