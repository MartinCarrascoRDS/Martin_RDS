"""
VENTAS RIPLEY

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTAS RIPLEY

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# Leer desde la columna C hasta la columna N
ventas_2024 = pd.read_excel(path_ventas, sheet_name = 'VENTAS RIPLEY', header = 4, usecols = "C:N")

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

ripley_2024 = ventas_2024.copy()
ripley_2024['ORIGEN'] = 'RIPLEY'
ripley_2024.columns = columnas

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]
ripley_2024 = ripley_2024.drop(columns = columnas_acumulados, axis = 1)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS RIPLEY'
ripley_2024.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS RIPLEY {fecha_anterior}.xlsx', index = False)


# 2025

# Leer desde la columna C hasta la columna N
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTAS RIPLEY', header = 40, usecols = "C:N")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

ripley_2025 = ventas_2025.copy()
ripley_2025['ORIGEN'] = 'RIPLEY'
ripley_2025.columns = columnas
ripley_2025 = ripley_2025.drop(columns = columnas_acumulados, axis = 1)

# Guardar
ripley_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTAS RIPLEY {fecha}.xlsx', index = False)
