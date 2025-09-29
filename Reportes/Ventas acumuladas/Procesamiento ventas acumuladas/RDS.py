"""
RDS

Script para el procesamiento de la base de datos de ventas acumuladas que se encuentra en la hoja RDS

El excel actualmente tiene la información en formato presentación, por lo que ahora se va a dejar en formato base, para poder trabajar con ella en Power BI.
"""

import pandas as pd

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/VENTAS ACUMULADAS 09-SEPTIEMBRE-25 {fecha}.xlsx'
fecha_limite = pd.to_datetime(fecha)

# 2024

# Leer hasta la columna FN
ventas_2024 = pd.read_excel(path_ventas, sheet_name = 'RDS', header = 4, usecols = "A:FN")

# Limpiar fechas
ventas_2024['FECHA'] = pd.to_datetime(ventas_2024['FECHA'], errors = 'coerce')
ventas_2024 = ventas_2024.dropna(subset = ["FECHA"])
ventas_2024 = ventas_2024[ventas_2024['FECHA'].dt.year == 2024]

# Renombrar
columnas = [
    "FECHA", "CANTIDAD DE VENTAS", "ACUMULADO DE VENTAS", "VAR % CANTIDAD DE VENTAS",
    "MONTO DE VENTAS", "ACUMULADO DE MONTO", "VAR % MONTO DE VENTAS",
    "UNIDADES", "ACUMULADO DE UNIDADES", "VAR % UNIDADES",
    "TICKET PROMEDIO", "VAR % TICKET PROMEDIO",
    "VISITAS", "CONVERSIÓN", "ORIGEN"
]

# Bloques
rds1_2024 = ventas_2024.iloc[:, 0:14].copy()
rds1_2024['ORIGEN'] = 'RDS1'
rds1_2024.columns = columnas

rds3_2024 = ventas_2024.iloc[:, 14:27].copy()
rds3_2024.insert(0, "FECHA", rds1_2024["FECHA"])
rds3_2024['ORIGEN'] = 'RDS3'
rds3_2024.columns = columnas

triana_2024 = ventas_2024.iloc[:, 27:40].copy()
triana_2024.insert(0, "FECHA", rds1_2024["FECHA"])
triana_2024["ORIGEN"] = "TRIANA"
triana_2024.columns = columnas

reicars_2024 = ventas_2024.iloc[:, 40:53].copy()
reicars_2024.insert(0, "FECHA", rds1_2024["FECHA"])
reicars_2024['ORIGEN'] = 'REICARS'
reicars_2024.columns = columnas

tyc_2024 = ventas_2024.iloc[:, 53:66].copy()
tyc_2024.insert(0, "FECHA", rds1_2024["FECHA"])
tyc_2024['ORIGEN'] = 'TYC'
tyc_2024.columns = columnas

mr_2024 = ventas_2024.iloc[:, 66:79].copy()
mr_2024.insert(0, "FECHA", rds1_2024["FECHA"])
mr_2024['ORIGEN'] = 'MERCADOREPUESTOS'
mr_2024.columns = columnas

black_2024 = ventas_2024.iloc[:, 79:92].copy()
black_2024.insert(0, "FECHA", rds1_2024["FECHA"])
black_2024['ORIGEN'] = 'BLACKPARTS'
black_2024.columns = columnas

bici_2024 = ventas_2024.iloc[:, 92:105].copy()
bici_2024.insert(0, "FECHA", rds1_2024["FECHA"])
bici_2024['ORIGEN'] = 'BICISOL'
bici_2024.columns = columnas

indusol_2024 = ventas_2024.iloc[:, 105:118].copy()
indusol_2024.insert(0, "FECHA", rds1_2024["FECHA"])
indusol_2024['ORIGEN'] = 'INDUSOL'
indusol_2024.columns = columnas

hyundai_2024 = ventas_2024.iloc[:, 118:131].copy()
hyundai_2024.insert(0, "FECHA", rds1_2024["FECHA"])
hyundai_2024['ORIGEN'] = 'HYUNDAI'
hyundai_2024.columns = columnas

mahindra_2024 = ventas_2024.iloc[:, 131:144].copy()
mahindra_2024.insert(0, "FECHA", rds1_2024["FECHA"])
mahindra_2024['ORIGEN'] = 'MAHINDRA'
mahindra_2024.columns = columnas

neumasol_2024 = ventas_2024.iloc[:, 144:157].copy()
neumasol_2024.insert(0, 'FECHA', rds1_2024['FECHA'])
neumasol_2024['ORIGEN'] = 'AUTOSOL'
neumasol_2024.columns = columnas

impacsol_2024 = ventas_2024.iloc[:, 157:170].copy()
impacsol_2024.insert(0, 'FECHA', rds1_2024['FECHA'])
impacsol_2024['ORIGEN'] = 'IMPACSOL'
impacsol_2024.columns = columnas

# Unir
final_2024 = pd.concat([rds1_2024, rds3_2024, triana_2024, reicars_2024, tyc_2024, mr_2024, black_2024, bici_2024, indusol_2024, hyundai_2024, mahindra_2024, neumasol_2024, impacsol_2024], ignore_index = True)

columnas_acumulados = [
    "ACUMULADO DE VENTAS", "ACUMULADO DE MONTO", "ACUMULADO DE UNIDADES"
]
final_2024 = final_2024.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2024[col] = pd.to_numeric(final_2024[col], errors = 'coerce')

final_2024['CANTIDAD DE VENTAS'] = (final_2024['CANTIDAD DE VENTAS'] * 0.90).round(0).astype(int)
final_2024['MONTO DE VENTAS'] = final_2024['MONTO DE VENTAS'] * 0.90
final_2024['UNIDADES'] = (final_2024['UNIDADES'] * 0.90).round(0).astype(int)

# Guardar
output_folder = '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/RDS'
final_2024.to_excel(f'{output_folder}/VENTAS ACUMULADAS RDS {fecha_anterior}.xlsx', index=False)


# 2025

# Leer hasta la columna FN
ventas_2025 = pd.read_excel(path_ventas, sheet_name = 'RDS', header = 41, usecols = "A:FN")

# Limpiar fechas
ventas_2025["FECHA"] = pd.to_datetime(ventas_2025['FECHA'], errors = 'coerce')
ventas_2025 = ventas_2025.dropna(subset = ['FECHA'])
ventas_2025 = ventas_2025[
    (ventas_2025['FECHA'].dt.year == 2025) &
    (ventas_2025['FECHA'] <= fecha_limite)
]

# Bloques
rds1_2025 = ventas_2025.iloc[:, 0:14].copy()
rds1_2025['ORIGEN'] = 'RDS1'
rds1_2025.columns = columnas

rds3_2025 = ventas_2025.iloc[:, 14:27].copy()
rds3_2025.insert(0, "FECHA", rds1_2025["FECHA"])
rds3_2025['ORIGEN'] = 'RDS3'
rds3_2025.columns = columnas

triana_2025 = ventas_2025.iloc[:, 27:40].copy()
triana_2025.insert(0, "FECHA", rds1_2025["FECHA"])
triana_2025["ORIGEN"] = "TRIANA"
triana_2025.columns = columnas

reicars_2025 = ventas_2025.iloc[:, 40:53].copy()
reicars_2025.insert(0, "FECHA", rds1_2025["FECHA"])
reicars_2025['ORIGEN'] = 'REICARS'
reicars_2025.columns = columnas

tyc_2025 = ventas_2025.iloc[:, 53:66].copy()
tyc_2025.insert(0, "FECHA", rds1_2025["FECHA"])
tyc_2025['ORIGEN'] = 'TYC'
tyc_2025.columns = columnas

mr_2025 = ventas_2025.iloc[:, 66:79].copy()
mr_2025.insert(0, "FECHA", rds1_2025["FECHA"])
mr_2025['ORIGEN'] = 'MERCADOREPUESTOS'
mr_2025.columns = columnas

black_2025 = ventas_2025.iloc[:, 79:92].copy()
black_2025.insert(0, "FECHA", rds1_2025["FECHA"])
black_2025['ORIGEN'] = 'BLACKPARTS'
black_2025.columns = columnas

bici_2025 = ventas_2025.iloc[:, 92:105].copy()
bici_2025.insert(0, "FECHA", rds1_2025["FECHA"])
bici_2025['ORIGEN'] = 'BICISOL'
bici_2025.columns = columnas

indusol_2025 = ventas_2025.iloc[:, 105:118].copy()
indusol_2025.insert(0, "FECHA", rds1_2025["FECHA"])
indusol_2025['ORIGEN'] = 'INDUSOL'
indusol_2025.columns = columnas

hyundai_2025 = ventas_2025.iloc[:, 118:131].copy()
hyundai_2025.insert(0, "FECHA", rds1_2025["FECHA"])
hyundai_2025['ORIGEN'] = 'HYUNDAI'
hyundai_2025.columns = columnas

mahindra_2025 = ventas_2025.iloc[:, 131:144].copy()
mahindra_2025.insert(0, "FECHA", rds1_2025["FECHA"])
mahindra_2025['ORIGEN'] = 'MAHINDRA'
mahindra_2025.columns = columnas

neumasol_2025 = ventas_2025.iloc[:, 144:157].copy()
neumasol_2025.insert(0, 'FECHA', rds1_2025['FECHA'])
neumasol_2025['ORIGEN'] = 'AUTOSOL'
neumasol_2025.columns = columnas

impacsol_2025 = ventas_2025.iloc[:, 157:170].copy()
impacsol_2025.insert(0, 'FECHA', rds1_2025['FECHA'])
impacsol_2025['ORIGEN'] = 'IMPACSOL'
impacsol_2025.columns = columnas

# Unir
final_2025 = pd.concat([rds1_2025, rds3_2025, triana_2025, reicars_2025, tyc_2025, mr_2025, black_2025, bici_2025, indusol_2025, hyundai_2025, mahindra_2025, neumasol_2025, impacsol_2025], ignore_index = True)
final_2025 = final_2025.drop(columns = columnas_acumulados, axis = 1)
# Castigos por devolución, cancelación y reclamo
for col in ['CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES']:
    final_2025[col] = pd.to_numeric(final_2025[col], errors = 'coerce')

final_2025['CANTIDAD DE VENTAS'] = (final_2025['CANTIDAD DE VENTAS'] * 0.90).round(0).astype(int)
final_2025['MONTO DE VENTAS'] = final_2025['MONTO DE VENTAS'] * 0.90
final_2025['UNIDADES'] = (final_2025['UNIDADES'] * 0.90).round(0).astype(int)

# Guardar
final_2025.to_excel(f'{output_folder}/VENTAS ACUMULADAS RDS {fecha}.xlsx', index = False)