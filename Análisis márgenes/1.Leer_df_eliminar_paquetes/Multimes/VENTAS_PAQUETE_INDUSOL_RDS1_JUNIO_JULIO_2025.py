"""
Unión de ventas en paquete de Indusol y RDS1 para junio y julio 2025
"""

import pandas as pd

junio = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JUNIO 2025/Paso1_ventas_paquete_INDUSOL_JUNIO 2025.xlsx', dtype = {"# de venta": str})
julio = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_INDUSOL_JULIO 2025.xlsx', dtype = {"# de venta": str})

dfs = [junio, julio]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/VENTAS_PAQUETE_CONSOLIDADO_JUNIO_JULIO_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)