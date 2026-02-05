"""
UNIÓN DE VENTAS TOTALES AGOSTO 2025
"""

import pandas as pd

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) AUTOSOL VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) BICISOL VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) BLACKPARTS VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
hyundai = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) HYUNDAI VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) INDUSOL VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) MERCADOREPUESTOS VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) RDS1 VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) RDS3 VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) REICARS VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) TRIANA VENTAS TOTALES.xlsx', dtype = {"# de venta": str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) TYC VENTAS TOTALES.xlsx', dtype = {"# de venta": str})

dfs = [autosol, bicisol, blackparts, hyundai, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) CONSOLIDADO VENTAS TOTALES.xlsx'
df_consolidado.to_excel(output_path, index = False)