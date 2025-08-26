"""
Unión de ventas en paquete
"""

import pandas as pd

indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/JULIO 2025 (HASTA 24-07)/Paso1_ventas_paquete_INDUSOL_JULIO 2025 (HASTA 24-07).xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/JULIO 2025 (HASTA 24-07)/Paso1_ventas_paquete_RDS1_JULIO 2025 (HASTA 24-07).xlsx', dtype = {"# de venta": str})

dfs = [indusol, rds1]

df_consolidado = pd.concat(dfs, ignore_index = True)

df_consolidado['Ingresos por productos (CLP) Neto'] = df_consolidado['Ingresos por productos (CLP)'] / 1.19

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/JULIO 2025 (HASTA 24-07)/VENTAS_PAQUETE_INDUSOL_RDS1_JULIO_2025_HASTA_24.xlsx'
df_consolidado.to_excel(output_path, index = False)