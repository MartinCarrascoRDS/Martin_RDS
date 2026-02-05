"""
FERRE

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja FERRE

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="FERRE", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer hasta la columna AN
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name="FERRE", header=fila_inicio_2025, usecols="A:BC")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025["FECHA"], errors="coerce")
ventas_2025 = ventas_2025.dropna(subset=["FECHA"])
ventas_2025 = ventas_2025[ventas_2025["FECHA"].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS PRE CASTIGO", "CANTIDAD DE VENTAS CON SHOP", "CANTIDAD DE VENTAS SHOP", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS BRUTO PRE CASTIGO", "MONTO DE VENTAS CON SHOP", "MONTO DE VENTAS SHOP", "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES PRE CASTIGO", "UNIDADES CON SHOP", "UNIDADES VENDIDAS SHOP", "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO",
    "VISITAS", "CONVERSIÓN", "ORIGEN"
]

columnas2 = [
    "FECHA", "CANTIDAD DE VENTAS PRE CASTIGO", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS BRUTO PRE CASTIGO", "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES PRE CASTIGO", "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO",
    "VISITAS", "CONVERSIÓN", "ORIGEN"
]

# Bloques
ferremaq_2025 = ventas_2025.iloc[:, 0:23].copy()
ferremaq_2025["ORIGEN"] = "FERREMAQ"
ferremaq_2025.columns = columnas

santaelba_2025 = ventas_2025.iloc[:, 23:39].copy()
santaelba_2025.insert(0, "FECHA", ferremaq_2025["FECHA"])
santaelba_2025["ORIGEN"] = "SANTA ELBA"
santaelba_2025.columns = columnas2

coco_2025 = ventas_2025.iloc[:, 39:55].copy()
coco_2025.insert(0, "FECHA", ferremaq_2025["FECHA"])
coco_2025["ORIGEN"] = "COCO"
coco_2025.columns = columnas2

# Unir
final_2025 = pd.concat([ferremaq_2025, santaelba_2025, coco_2025], ignore_index=True)

columnas_eliminar = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES",
    "CANTIDAD DE VENTAS PRE CASTIGO", "MONTO DE VENTAS BRUTO PRE CASTIGO", "UNIDADES PRE CASTIGO"
]
final_2025 = final_2025.drop(columns = columnas_eliminar, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')

final_2025['CANTIDAD DE VENTAS'] = (final_2025['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
final_2025['MONTO DE VENTAS'] = (final_2025['MONTO DE VENTAS']).round(0).fillna(0).astype(int)
final_2025['UNIDADES'] = (final_2025['UNIDADES']).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/FERRE'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS FERRE {fecha_anterior}.xlsx', index=False)


# 2026

# Leer hasta la columna AN
# Desde el reporte del 2026-10-16 en adelante, con la adición de columnas "PRE CASTIGO", leer hasta la columna AW
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name="FERRE", header=fila_inicio_2026, usecols="A:BC")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
ferremaq_2026 = ventas_2026.iloc[:, 0:23].copy()
ferremaq_2026["ORIGEN"] = "FERREMAQ"
ferremaq_2026.columns = columnas

santaelba_2026 = ventas_2026.iloc[:, 23:39].copy()
santaelba_2026.insert(0, "FECHA", ferremaq_2026["FECHA"])
santaelba_2026["ORIGEN"] = "SANTA ELBA"
santaelba_2026.columns = columnas2

coco_2026 = ventas_2026.iloc[:, 39:55].copy()
coco_2026.insert(0, "FECHA", ferremaq_2026["FECHA"])
coco_2026["ORIGEN"] = "COCO"
coco_2026.columns = columnas2

# Unir
final_2026 = pd.concat([ferremaq_2026, santaelba_2026, coco_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_eliminar, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2026[col] = pd.to_numeric(final_2026[col], errors = 'coerce')

final_2026['CANTIDAD DE VENTAS'] = (final_2026['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
final_2026['MONTO DE VENTAS'] = (final_2026['MONTO DE VENTAS']).round(0).fillna(0).astype(int)
final_2026['UNIDADES'] = (final_2026['UNIDADES']).round(0).fillna(0).astype(int)

# Guardar
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS FERRE {fecha}.xlsx', index = False)