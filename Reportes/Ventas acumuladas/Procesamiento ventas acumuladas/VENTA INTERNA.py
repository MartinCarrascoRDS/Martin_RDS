"""
VENTA INTERNA

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja VENTA INTERNA

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# No hubo ventas internas en 2024


# 2025

# Leer desde la columna C hasta la columna U
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'VENTA INTERNA ', header = 6, usecols = "C:U")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

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

# Bloques
rdsinterna_2025 = ventas_2025.iloc[:, 0:10].copy()
rdsinterna_2025['ORIGEN'] = 'RDS INTERNA'
rdsinterna_2025.columns = columnas

ferresolinterna_2025 = ventas_2025.iloc[:, 10:19].copy()
ferresolinterna_2025.insert(0, 'FECHA', rdsinterna_2025['FECHA'])
ferresolinterna_2025['ORIGEN'] = 'FERRESOL INTERNA'
ferresolinterna_2025.columns = columnas

# Unir
final_2025 = pd.concat([rdsinterna_2025, ferresolinterna_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA INTERNA'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS VENTA INTERNA {fecha}.xlsx', index = False)