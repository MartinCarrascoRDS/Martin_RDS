"""
KIA Y POMPEYO

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja KIA Y POMPEYO

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="KIA Y POMPEYO", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025
# Por la inclusión de columnas "PRE CASTIGO", leer hasta la columna AM
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'KIA Y POMPEYO', header = fila_inicio_2025, usecols = "C:AM")

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS PRE CASTIGO", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS BRUTO PRE CASTIGO", "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES PRE CASTIGO", "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES", "TICKET PROMEDIO BRUTO PRE CASTIGO",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO", "VISITAS", "CONVERSIÓN PRE CASTIGO", "CONVERSIÓN", "ORIGEN"
]

columnas_eliminar = [
    "CANTIDAD DE VENTAS PRE CASTIGO", "ACUMULADO DE VENTAS",
    "MONTO DE VENTAS BRUTO PRE CASTIGO", "ACUMULADO DE MONTO",
    "UNIDADES PRE CASTIGO", "ACUMULADO DE UNIDADES",
    "TICKET PROMEDIO BRUTO PRE CASTIGO", "CONVERSIÓN PRE CASTIGO"
]

# Bloques
kia_2025 = ventas_2025.iloc[:, 0:19].copy()
kia_2025['ORIGEN'] = 'KIA'
kia_2025.columns = columnas

pompeyo_2025 = ventas_2025.iloc[:, 19:37].copy()
pompeyo_2025.insert(0, 'FECHA', kia_2025['FECHA'])
pompeyo_2025['ORIGEN'] = 'POMPEYO'
pompeyo_2025.columns = columnas

# Unir
final_2025 = pd.concat([kia_2025, pompeyo_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_eliminar, axis = 1)

for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES', 'VISITAS']:
    final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')

final_2025['CANTIDAD DE VENTAS'] = (final_2025['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
final_2025['MONTO DE VENTAS'] = (final_2025['MONTO DE VENTAS']).round(0).fillna(0).astype(int)
final_2025['UNIDADES'] = (final_2025['UNIDADES']).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/KIA Y POMPEYO'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS KIA Y POMPEYO {fecha_anterior}.xlsx', index = False)

# 2026

# Por la inclusión de columnas "PRE CASTIGO", leer hasta la columna AM
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'KIA Y POMPEYO', header = fila_inicio_2026, usecols = "C:AM")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
kia_2026 = ventas_2026.iloc[:, 0:19].copy()
kia_2026['ORIGEN'] = 'KIA'
kia_2026.columns = columnas

pompeyo_2026 = ventas_2026.iloc[:, 19:37].copy()
pompeyo_2026.insert(0, 'FECHA', kia_2026['FECHA'])
pompeyo_2026['ORIGEN'] = 'POMPEYO'
pompeyo_2026.columns = columnas

# Unir
final_2026 = pd.concat([kia_2026, pompeyo_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_eliminar, axis = 1)

for col in 'CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES', 'TICKET PROMEDIO':
    final_2026[col] = pd.to_numeric(final_2026[col], errors = 'coerce')
    final_2026[col] = (final_2026[col]).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/KIA Y POMPEYO'
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS KIA Y POMPEYO {fecha}.xlsx', index = False)