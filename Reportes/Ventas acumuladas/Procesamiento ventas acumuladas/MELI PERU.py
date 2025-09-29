"""
MELI PERU

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja MELI PERU

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# Leer desde la columna B hasta la columna P
ventas_2024 = pd.read_excel(path_ventas, sheet_name = 'MELI PERÙ', header = 3, usecols = 'B:P')

# Limpiar fechas
ventas_2024['FECHA'] = pd.to_datetime(ventas_2024['FECHA'], errors = 'coerce')
ventas_2024 = ventas_2024.dropna(subset = ["FECHA"])
ventas_2024 = ventas_2024[ventas_2024['FECHA'].dt.year == 2024]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS (PEN)", "ACUMULADO DE MONTO (PEN)", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO (PEN)", "VISITAS", "CONVERSIÓN", "MONTO DE VENTAS",
    "TICKET PROMEDIO", "ORIGEN"
]

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO (PEN)", "ACUMULADO DE UNIDADES"
]

peru_2024 = ventas_2024.copy()
peru_2024['ORIGEN'] = 'MELI PERU'
peru_2024.columns = columnas

peru_2024 = peru_2024.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    peru_2024[col] = pd.to_numeric(peru_2024[col], errors = 'coerce')

peru_2024['CANTIDAD DE VENTAS'] = (peru_2024['CANTIDAD DE VENTAS'] * 0.9).round(0).astype(int)
peru_2024['MONTO DE VENTAS'] = peru_2024['MONTO DE VENTAS'] * 0.9
peru_2024['UNIDADES'] = (peru_2024['UNIDADES'] * 0.9).round(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU'
peru_2024.to_excel(f'{output_folder}/VENTAS ACUMULADAS MELI PERU {fecha_anterior}.xlsx', index = False)


# 2025

# Leer desde la columna B hasta la columna P
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'MELI PERÙ', header = 40, usecols = 'B:P')

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

peru_2025 = ventas_2025.copy()
peru_2025['ORIGEN'] = 'MELI PERU'
peru_2025.columns = columnas

peru_2025 = peru_2025.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    peru_2024[col] = pd.to_numeric(peru_2024[col], errors = 'coerce')

peru_2025['CANTIDAD DE VENTAS'] = (peru_2025['CANTIDAD DE VENTAS'] * 0.9).round(0).astype(int)
peru_2025['MONTO DE VENTAS'] = peru_2025['MONTO DE VENTAS'] * 0.9
peru_2025['UNIDADES'] = (peru_2025['UNIDADES'] * 0.9).round(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU'
peru_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS MELI PERU {fecha}.xlsx', index = False)