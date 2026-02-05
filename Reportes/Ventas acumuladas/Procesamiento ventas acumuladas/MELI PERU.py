"""
MELI PERU

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja MELI PERU

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd
import numpy as np

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="MELI PERÙ", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer desde la columna B hasta la columna P
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'MELI PERÙ', header = fila_inicio_2025, usecols = 'B:U')

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS PRE CASTIGO", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS (PEN) BRUTO PRE CASTIGO", "MONTO DE VENTAS (PEN)", "ACUMULADO DE MONTO (PEN)", "VAR % MONTO DE VENTAS (PEN)",
    "UNIDADES PRE CASTIGO", "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO (PEN)", "VAR % TICKET PROMEDIO", "VISITAS", "CONVERSIÓN",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "TICKET PROMEDIO", "ORIGEN"
]

columnas_eliminar = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO (PEN)", "ACUMULADO DE UNIDADES", "ACUMULADO DE MONTO",
    "CANTIDAD DE VENTAS PRE CASTIGO", "MONTO DE VENTAS (PEN) BRUTO PRE CASTIGO", "UNIDADES PRE CASTIGO"
]

peru_2025 = ventas_2025.copy()
peru_2025['ORIGEN'] = 'MELI PERU'
peru_2025.columns = columnas

peru_2025 = peru_2025.drop(columns = columnas_eliminar, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS (PEN)', 'UNIDADES', 'MONTO DE VENTAS', 'VISITAS']:
    if col in peru_2025.columns:
        peru_2025[col] = pd.to_numeric(peru_2025[col], errors = 'coerce')

peru_2025['CANTIDAD DE VENTAS'] = (peru_2025['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
peru_2025['MONTO DE VENTAS (PEN)'] = (peru_2025['MONTO DE VENTAS (PEN)']).round(0).fillna(0).astype(int)
peru_2025['UNIDADES'] = (peru_2025['UNIDADES']).round(0).fillna(0).astype(int)
"""peru_2025['TICKET PROMEDIO (PEN)'] = peru_2025['MONTO DE VENTAS (PEN)'] / peru_2025['UNIDADES']
peru_2025['MONTO DE VENTAS'] = peru_2025['MONTO DE VENTAS (PEN)'] * 250
peru_2025['MONTO DE VENTAS'] = peru_2025['MONTO DE VENTAS'].round(0).fillna(0)
peru_2025['CONVERSIÓN'] = np.divide(
    peru_2025['CANTIDAD DE VENTAS'].to_numpy(),
    peru_2025['VISITAS'].to_numpy(),
    out=np.zeros_like(peru_2025['CANTIDAD DE VENTAS'].to_numpy(), dtype=float),
    where=peru_2025['VISITAS'].to_numpy() != 0
)"""

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU'
peru_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS MELI PERU {fecha_anterior}.xlsx', index = False)


# 2026

fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name = 'MELI PERÙ', header = fila_inicio_2026, usecols = 'B:U')

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

peru_2026 = ventas_2026.copy()
peru_2026['ORIGEN'] = 'MELI PERU'
peru_2026.columns = columnas

peru_2026 = peru_2026.drop(columns = columnas_eliminar, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS (PEN)', 'UNIDADES', 'MONTO DE VENTAS', 'VISITAS']:
    peru_2026[col] = pd.to_numeric(peru_2026[col], errors = 'coerce')

peru_2026['CANTIDAD DE VENTAS'] = (peru_2026['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
peru_2026['MONTO DE VENTAS (PEN)'] = (peru_2026['MONTO DE VENTAS (PEN)']).round(0).fillna(0)
peru_2026['UNIDADES'] = (peru_2026['UNIDADES']).round(0).fillna(0).astype(int)
"""peru_2026['TICKET PROMEDIO (PEN)'] = peru_2026['MONTO DE VENTAS (PEN)'] / peru_2026['UNIDADES']
peru_2026['MONTO DE VENTAS'] = peru_2026['MONTO DE VENTAS (PEN)'] * 250
peru_2026['MONTO DE VENTAS'] = (peru_2026['MONTO DE VENTAS']).round(0).fillna(0)
peru_2026['TICKET PROMEDIO'] = peru_2026['TICKET PROMEDIO (PEN)'] * 250
peru_2026['CONVERSIÓN'] = np.divide(
    peru_2026['CANTIDAD DE VENTAS'].to_numpy(),
    peru_2026['VISITAS'].to_numpy(),
    out=np.zeros_like(peru_2026['CANTIDAD DE VENTAS'].to_numpy(), dtype=float),
    where=peru_2026['VISITAS'].to_numpy() != 0
)"""

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU'
peru_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS MELI PERU {fecha}.xlsx', index = False)