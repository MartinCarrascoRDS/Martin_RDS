"""
VENTA EMPRESA

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTA EMPRESA

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# No hubo ventas empresa en 2024


# 2025

# Leer desde la columna B hasta la columna V
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTA EMPRESA ', header = 5, usecols = "B:V")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "ORIGEN"
]

columnas2 = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO",
    "UNIDADES", "ACUMULADO DE UNIDADES",
    "TICKET PROMEDIO",  "CANTIDAD DE NOTAS DE CRÉDITO", "MONTO DE NOTAS DE CRÉDITO", "ORIGEN"
]

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]

# Bloques
rdsempresa_2025 = ventas_2025.iloc[:, 0:12].copy()
rdsempresa_2025['ORIGEN'] = 'RDS EMPRESA'
rdsempresa_2025.columns = columnas

ferresolempresa_2025 = ventas_2025.iloc[:, 12:21].copy()
ferresolempresa_2025.insert(0, 'FECHA', rdsempresa_2025['FECHA'])
ferresolempresa_2025['ORIGEN'] = 'FERRESOL EMPRESA'
ferresolempresa_2025.columns = columnas2

# Unir
final_2025 = pd.concat([rdsempresa_2025, ferresolempresa_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA EMPRESA'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTA EMPRESA {fecha}.xlsx', index = False)
