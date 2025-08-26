"""
UNIÓN DE VENTAS EN PAQUETE
"""

import pandas as pd

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_AUTOSOL_JULIO 2025.xlsx', dtype = {'# de venta': str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_BICISOL_JULIO 2025.xlsx', dtype = {'# de venta': str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_BLACKPARTS_JULIO 2025.xlsx', dtype = {'# de venta': str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_INDUSOL_JULIO 2025.xlsx', dtype = {'# de venta': str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_MERCADOREPUESTOS_JULIO 2025.xlsx', dtype = {'# de venta': str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_RDS1_JULIO 2025.xlsx', dtype = {'# de venta': str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_RDS3_JULIO 2025.xlsx', dtype = {'# de venta': str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_REICARS_JULIO 2025.xlsx', dtype = {'# de venta': str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_TRIANA_JULIO 2025.xlsx', dtype = {'# de venta': str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_TYC_JULIO 2025.xlsx', dtype = {'# de venta': str})

dfs = [autosol, bicisol, blackparts, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)

df_consolidado['Ingresos por productos (CLP) Neto'] = df_consolidado['Ingresos por productos (CLP)'] / 1.19

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/VENTAS_PAQUETE_CONSOLIDADO_JULIO_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)