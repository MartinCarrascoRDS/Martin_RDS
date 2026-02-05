"""
RDS

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja RDS

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# Detectar dinámicamente filas de inicio de 2025 y 2026
raw = pd.read_excel(path_ventas, sheet_name="RDS", header=None, dtype=str)
filas_fecha = raw.index[raw.apply(lambda row: row.astype(str).str.contains("FECHA").any(), axis=1)].tolist()

# 2025

# Leer hasta la columna FN
fila_inicio_2025 = filas_fecha[0]
ventas_2025 = pd.read_excel(path_ventas, sheet_name="RDS", header=fila_inicio_2025, usecols="A:HG")

# Limpiar fechas
ventas_2025['FECHA'] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ["FECHA"])
ventas_2025 = ventas_2025[ventas_2025['FECHA'].dt.year == 2025]

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
rds1_2025 = ventas_2025.iloc[:, 0:23].copy()
rds1_2025['ORIGEN'] = 'RDS1'
rds1_2025.columns = columnas

rds3_2025 = ventas_2025.iloc[:, 23:39].copy()
rds3_2025.insert(0, "FECHA", rds1_2025["FECHA"])
rds3_2025['ORIGEN'] = 'RDS3'
rds3_2025.columns = columnas2

triana_2025 = ventas_2025.iloc[:, 39:55].copy()
triana_2025.insert(0, "FECHA", rds1_2025["FECHA"])
triana_2025["ORIGEN"] = "TRIANA"
triana_2025.columns = columnas2

reicars_2025 = ventas_2025.iloc[:, 55:71].copy()
reicars_2025.insert(0, "FECHA", rds1_2025["FECHA"])
reicars_2025['ORIGEN'] = 'REICARS'
reicars_2025.columns = columnas2

tyc_2025 = ventas_2025.iloc[:, 71:87].copy()
tyc_2025.insert(0, "FECHA", rds1_2025["FECHA"])
tyc_2025['ORIGEN'] = 'TYC'
tyc_2025.columns = columnas2

mr_2025 = ventas_2025.iloc[:, 87:103].copy()
mr_2025.insert(0, "FECHA", rds1_2025["FECHA"])
mr_2025['ORIGEN'] = 'MERCADOREPUESTOS'
mr_2025.columns = columnas2

black_2025 = ventas_2025.iloc[:, 103:119].copy()
black_2025.insert(0, "FECHA", rds1_2025["FECHA"])
black_2025['ORIGEN'] = 'BLACKPARTS'
black_2025.columns = columnas2

bici_2025 = ventas_2025.iloc[:, 119:135].copy()
bici_2025.insert(0, "FECHA", rds1_2025["FECHA"])
bici_2025['ORIGEN'] = 'BICISOL'
bici_2025.columns = columnas2

indusol_2025 = ventas_2025.iloc[:, 135:151].copy()
indusol_2025.insert(0, "FECHA", rds1_2025["FECHA"])
indusol_2025['ORIGEN'] = 'INDUSOL'
indusol_2025.columns = columnas2

hyundai_2025 = ventas_2025.iloc[:, 151:167].copy()
hyundai_2025.insert(0, "FECHA", rds1_2025["FECHA"])
hyundai_2025['ORIGEN'] = 'HYUNDAI'
hyundai_2025.columns = columnas2

mahindra_2025 = ventas_2025.iloc[:, 167:183].copy()
mahindra_2025.insert(0, "FECHA", rds1_2025["FECHA"])
mahindra_2025['ORIGEN'] = 'MAHINDRA'
mahindra_2025.columns = columnas2

neumasol_2025 = ventas_2025.iloc[:, 183:199].copy()
neumasol_2025.insert(0, 'FECHA', rds1_2025['FECHA'])
neumasol_2025['ORIGEN'] = 'AUTOSOL'
neumasol_2025.columns = columnas2

impacsol_2025 = ventas_2025.iloc[:, 199:215].copy()
impacsol_2025.insert(0, 'FECHA', rds1_2025['FECHA'])
impacsol_2025['ORIGEN'] = 'IMPACSOL'
impacsol_2025.columns = columnas2

# Unir
final_2025 = pd.concat([rds1_2025, rds3_2025, triana_2025, reicars_2025, tyc_2025, mr_2025, black_2025, bici_2025, indusol_2025, hyundai_2025, mahindra_2025, neumasol_2025, impacsol_2025], ignore_index = True)

columnas_eliminar = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES",
    "CANTIDAD DE VENTAS PRE CASTIGO", "MONTO DE VENTAS BRUTO PRE CASTIGO", "UNIDADES PRE CASTIGO"
]
final_2025 = final_2025.drop(columns = columnas_eliminar, axis = 1)

for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES', 'VISITAS']:
    final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')

final_2025['CANTIDAD DE VENTAS'] = (final_2025['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
final_2025['MONTO DE VENTAS'] = (final_2025['MONTO DE VENTAS']).round(0).fillna(0).astype(int)
final_2025['UNIDADES'] = (final_2025['UNIDADES']).round(0).fillna(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/RDS'
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS RDS {fecha_anterior}.xlsx', index=False)


# 2026

# Leer hasta la columna FN
# Desde el reporte del 2026-10-16 en adelante, con la adición de las columnas "PRE CASTIGO", leer hasta la columna HA
fila_inicio_2026 = filas_fecha[1]
ventas_2026 = pd.read_excel(path_ventas, sheet_name="RDS", header=fila_inicio_2026, usecols="A:HG")

# Limpiar fechas
ventas_2026["FECHA"] = pd.to_datetime(ventas_2026['FECHA'], errors = 'coerce')
ventas_2026 = ventas_2026.dropna(subset = ['FECHA'])
ventas_2026 = ventas_2026[
    (ventas_2026['FECHA'].dt.year == 2026) &
    (ventas_2026['FECHA'] <= fecha_limite)
]

# Bloques
rds1_2026 = ventas_2026.iloc[:, 0:23].copy()
rds1_2026['ORIGEN'] = 'RDS1'
rds1_2026.columns = columnas

rds3_2026 = ventas_2026.iloc[:, 23:39].copy()
rds3_2026.insert(0, "FECHA", rds1_2026["FECHA"])
rds3_2026['ORIGEN'] = 'RDS3'
rds3_2026.columns = columnas2

triana_2026 = ventas_2026.iloc[:, 39:55].copy()
triana_2026.insert(0, "FECHA", rds1_2026["FECHA"])
triana_2026["ORIGEN"] = "TRIANA"
triana_2026.columns = columnas2

reicars_2026 = ventas_2026.iloc[:, 55:71].copy()
reicars_2026.insert(0, "FECHA", rds1_2026["FECHA"])
reicars_2026['ORIGEN'] = 'REICARS'
reicars_2026.columns = columnas2

tyc_2026 = ventas_2026.iloc[:, 71:87].copy()
tyc_2026.insert(0, "FECHA", rds1_2026["FECHA"])
tyc_2026['ORIGEN'] = 'TYC'
tyc_2026.columns = columnas2

mr_2026 = ventas_2026.iloc[:, 87:103].copy()
mr_2026.insert(0, "FECHA", rds1_2026["FECHA"])
mr_2026['ORIGEN'] = 'MERCADOREPUESTOS'
mr_2026.columns = columnas2

black_2026 = ventas_2026.iloc[:, 103:119].copy()
black_2026.insert(0, "FECHA", rds1_2026["FECHA"])
black_2026['ORIGEN'] = 'BLACKPARTS'
black_2026.columns = columnas2

bici_2026 = ventas_2026.iloc[:, 119:135].copy()
bici_2026.insert(0, "FECHA", rds1_2026["FECHA"])
bici_2026['ORIGEN'] = 'BICISOL'
bici_2026.columns = columnas2

indusol_2026 = ventas_2026.iloc[:, 135:151].copy()
indusol_2026.insert(0, "FECHA", rds1_2026["FECHA"])
indusol_2026['ORIGEN'] = 'INDUSOL'
indusol_2026.columns = columnas2

hyundai_2026 = ventas_2026.iloc[:, 151:167].copy()
hyundai_2026.insert(0, "FECHA", rds1_2026["FECHA"])
hyundai_2026['ORIGEN'] = 'HYUNDAI'
hyundai_2026.columns = columnas2

mahindra_2026 = ventas_2026.iloc[:, 167:183].copy()
mahindra_2026.insert(0, "FECHA", rds1_2026["FECHA"])
mahindra_2026['ORIGEN'] = 'MAHINDRA'
mahindra_2026.columns = columnas2

neumasol_2026 = ventas_2026.iloc[:, 183:199].copy()
neumasol_2026.insert(0, 'FECHA', rds1_2026['FECHA'])
neumasol_2026['ORIGEN'] = 'AUTOSOL'
neumasol_2026.columns = columnas2

impacsol_2026 = ventas_2026.iloc[:, 199:215].copy()
impacsol_2026.insert(0, 'FECHA', rds1_2026['FECHA'])
impacsol_2026['ORIGEN'] = 'IMPACSOL'
impacsol_2026.columns = columnas2

# Unir
final_2026 = pd.concat([rds1_2026, rds3_2026, triana_2026, reicars_2026, tyc_2026, mr_2026, black_2026, bici_2026, indusol_2026, hyundai_2026, mahindra_2026, neumasol_2026, impacsol_2026], ignore_index = True)
final_2026 = final_2026.drop(columns = columnas_eliminar, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES', 'VISITAS']:
    final_2026[col] = pd.to_numeric(final_2026[col], errors = 'coerce')

final_2026['CANTIDAD DE VENTAS'] = (final_2026['CANTIDAD DE VENTAS']).round(0).fillna(0).astype(int)
final_2026['MONTO DE VENTAS'] = (final_2026['MONTO DE VENTAS']).round(0).fillna(0).astype(int)
final_2026['UNIDADES'] = (final_2026['UNIDADES']).round(0).fillna(0).astype(int)

# Guardar
final_2026.to_excel(f'{output_folder}/VENTAS ACUMULADAS RDS {fecha}.xlsx', index = False)