"""
FERRE

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja FERRE

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# Leer hasta la columna AN
ventas_2024 = pd.read_excel(path_ventas, sheet_name='FERRE', header=4, usecols="A:AN")

# Limpiar fechas
ventas_2024["FECHA"] = pd.to_datetime(ventas_2024["FECHA"], errors="coerce")
ventas_2024 = ventas_2024.dropna(subset=["FECHA"])
ventas_2024 = ventas_2024[ventas_2024["FECHA"].dt.year == 2024]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO",
    "VISITAS", "CONVERSIÓN", "ORIGEN"
]

# Bloques
ferremaq_2024 = ventas_2024.iloc[:, 0:14].copy()
ferremaq_2024["ORIGEN"] = "FERREMAQ"
ferremaq_2024.columns = columnas

santaelba_2024 = ventas_2024.iloc[:, 14:27].copy()
santaelba_2024.insert(0, "FECHA", ferremaq_2024["FECHA"])
santaelba_2024["ORIGEN"] = "SANTA ELBA"
santaelba_2024.columns = columnas

coco_2024 = ventas_2024.iloc[:, 27:40].copy()
coco_2024.insert(0, "FECHA", ferremaq_2024["FECHA"])
coco_2024["ORIGEN"] = "COCO"
coco_2024.columns = columnas

# Unir
final_2024 = pd.concat([ferremaq_2024, santaelba_2024, coco_2024], ignore_index=True)

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]
final_2024 = final_2024.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2024[col] = pd.to_numeric(final_2024[col], errors = 'coerce')

final_2024['CANTIDAD DE VENTAS'] = (final_2024['CANTIDAD DE VENTAS'] * 0.95).round(0).astype(int)
final_2024['MONTO DE VENTAS'] = final_2024['MONTO DE VENTAS'] * 0.95
final_2024['UNIDADES'] = (final_2024['UNIDADES'] * 0.95).round(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/FERRE'
final_2024.to_excel(f'{output_folder}/VENTAS ACUMULADAS FERRE {fecha_anterior}.xlsx', index=False)


# 2025

# Leer hasta la columna AN
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'FERRE', header = 42, usecols = "A:AN")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

# Bloques
ferremaq_2025 = ventas_2025.iloc[:, 0:14].copy()
ferremaq_2025["ORIGEN"] = "FERREMAQ"
ferremaq_2025.columns = columnas

santaelba_2025 = ventas_2025.iloc[:, 14:27].copy()
santaelba_2025.insert(0, "FECHA", ferremaq_2025["FECHA"])
santaelba_2025["ORIGEN"] = "SANTA ELBA"
santaelba_2025.columns = columnas

coco_2025 = ventas_2025.iloc[:, 27:40].copy()
coco_2025.insert(0, "FECHA", ferremaq_2025["FECHA"])
coco_2025["ORIGEN"] = "COCO"
coco_2025.columns = columnas

# Unir
final_2025 = pd.concat([ferremaq_2025, santaelba_2025, coco_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')

final_2025['CANTIDAD DE VENTAS'] = (final_2025['CANTIDAD DE VENTAS'] * 0.95).round(0).astype(int)
final_2025['MONTO DE VENTAS'] = final_2025['MONTO DE VENTAS'] * 0.95
final_2025['UNIDADES'] = (final_2025['UNIDADES'] * 0.95).round(0).astype(int)

# Guardar
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS FERRE {fecha}.xlsx', index = False)