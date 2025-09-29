"""
UNIÓN DE VENTAS TOTALES AGOSTO 2025
"""

import pandas as pd

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_AUTOSOL_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_BICISOL_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_BLACKPARTS_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
hyundai = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_HYUNDAI_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_INDUSOL_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_MERCADOREPUESTOS_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_RDS1_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_RDS3_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_REICARS_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_TRIANA_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/Paso1.2_TYC_AGOSTO 2025_listo.xlsx', dtype = {"# de venta": str})

dfs = [autosol, bicisol, blackparts, hyundai, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025/VENTAS_TOTALES_CONSOLIDADO_AGOSTO_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)