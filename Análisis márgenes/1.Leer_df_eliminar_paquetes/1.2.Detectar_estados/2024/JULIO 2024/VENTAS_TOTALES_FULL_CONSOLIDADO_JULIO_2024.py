"""
Unión de las ventas full de Julio 2024 de todas las cuentas
"""

import pandas as pd

carpeta = "/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2024/JULIO 2024"

bicisol = pd.read_excel(f'{carpeta}/Paso1.2_FULL BICISOL_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
blackparts = pd.read_excel(f'{carpeta}/Paso1.2_FULL BLACKPARTS_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
hyundai = pd.read_excel(f'{carpeta}/Paso1.2_FULL INDUSOL_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
indusol = pd.read_excel(f'{carpeta}/Paso1.2_FULL BLACKPARTS_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
mercadorepuestos = pd.read_excel(f'{carpeta}/Paso1.2_FULL MERCADOREPUESTOS_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel(f'{carpeta}/Paso1.2_FULL RDS1_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
rds3 = pd.read_excel(f'{carpeta}/Paso1.2_FULL RDS3_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
reicars = pd.read_excel(f'{carpeta}/Paso1.2_FULL REICARS_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
triana = pd.read_excel(f'{carpeta}/Paso1.2_FULL TRIANA_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})
tyc = pd.read_excel(f'{carpeta}/Paso1.2_FULL TYC_JULIO 2024_listo.xlsx', dtype = {"# de venta": str})

dfs = [bicisol, blackparts, hyundai, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)

df_consolidado.to_excel(f'{carpeta}/VENTAS_TOTALES_FULL_CONSOLIDADO_JULIO_2024.xlsx', index = False)