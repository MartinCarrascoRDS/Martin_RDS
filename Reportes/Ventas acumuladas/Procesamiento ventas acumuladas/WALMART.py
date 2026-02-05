"""
WALMART

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja WALMART

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="WALMART", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'WALMART', header = fila_inicio_2025, usecols = "B:AD")

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS PRE CASTIGO", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS BRUTO PRE CASTIGO", "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES PRE CASTIGO", "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "ORIGEN"
]

columnas_eliminar = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES",
    "CANTIDAD DE VENTAS PRE CASTIGO", "MONTO DE VENTAS BRUTO PRE CASTIGO", "UNIDADES PRE CASTIGO"
]

# Bloques
walmartrep_2025 = ventas_2025.iloc[:, 0:15].copy()
walmartrep_2025['ORIGEN'] = 'WALMART'
walmartrep_2025.columns = columnas

walmartneuma_2025 = ventas_2025.iloc[:, 15:29].copy()
walmartneuma_2025.insert(0, 'FECHA', walmartrep_2025['FECHA'])
walmartneuma_2025['ORIGEN'] = 'WALMART NEUMA'
walmartneuma_2025.columns = columnas

# Unir
final_2025 = pd.concat([walmartrep_2025, walmartneuma_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_eliminar, axis = 1)
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')
    final_2025[col] = (final_2025[col]).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/WALMART'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS WALMART {fecha_anterior}.xlsx', index = False)

# 2026
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'WALMART', header = fila_inicio_2026, usecols = "B:AD")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
walmart_2026 = ventas_2026.iloc[:, 0:15].copy()
walmart_2026['ORIGEN'] = 'WALMART'
walmart_2026.columns = columnas

walmartneuma_2026 = ventas_2026.iloc[:, 15:29].copy()
walmartneuma_2026.insert(0, 'FECHA', walmart_2026['FECHA'])
walmartneuma_2026['ORIGEN'] = 'WALMART NEUMA'
walmartneuma_2026.columns = columnas

# Unir
final_2026 = pd.concat([walmart_2026, walmartneuma_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_eliminar, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2026[col] = pd.to_numeric(final_2026[col], errors = 'coerce')

final_2026['CANTIDAD DE VENTAS'] = (final_2026['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
final_2026['MONTO DE VENTAS'] = (final_2026['MONTO DE VENTAS']).round(0).fillna(0)
final_2026['UNIDADES'] = (final_2026['UNIDADES']).round(0).fillna(0).astype(int)

# Guardar
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS WALMART {fecha}.xlsx', index = False)