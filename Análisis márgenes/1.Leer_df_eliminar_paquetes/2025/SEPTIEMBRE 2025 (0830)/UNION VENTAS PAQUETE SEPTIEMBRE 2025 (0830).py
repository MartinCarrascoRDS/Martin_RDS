"""
UNIÓN DE VENTAS EN PAQUETE
"""

import pandas as pd

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) AUTOSOL VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) BICISOL VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) BLACKPARTS VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
hyundai = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) HYUNDAI VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) INDUSOL VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) MERCADOREPUESTOS VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) RDS1 VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) RDS3 VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) REICARS VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) TRIANA VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) TYC VENTAS PAQUETE.xlsx', dtype = {'# de venta': str})

dfs = [autosol, bicisol, blackparts, hyundai, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)

df_consolidado['Ingresos por productos (CLP) Neto'] = df_consolidado['Ingresos por productos (CLP)'] / 1.19

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) CONSOLIDADO VENTAS PAQUETE.xlsx'
df_consolidado.to_excel(output_path, index = False)