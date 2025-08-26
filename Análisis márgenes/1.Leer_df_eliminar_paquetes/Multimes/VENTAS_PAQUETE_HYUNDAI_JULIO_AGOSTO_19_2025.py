"""
Unión de ventas en paquete de Hyundai de julio y agosto (hasta el 19 de agosto) de 2025.
"""

import pandas as pd

julio = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/JULIO 2025/Paso1_ventas_paquete_HYUNDAI_JULIO 2025.xlsx', dtype = {"# de venta": str})
agosto = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/AGOSTO 2025 (HASTA 19-08)/Paso1_ventas_paquete_HYUNDAI_AGOSTO 2025 (HASTA 19-08).xlsx', dtype = {"# de venta": str})

dfs = [julio, agosto]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/VENTAS_PAQUETE_HYUNDAI_JULIO_AGOSTO_19_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)