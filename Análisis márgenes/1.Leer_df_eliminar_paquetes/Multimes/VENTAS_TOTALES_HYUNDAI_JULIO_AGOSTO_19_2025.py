"""
Unión de ventas totales de Indusol y RDS1 en junio y julio 2025
"""

import pandas as pd

julio = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/JULIO 2025/Paso1.2_HYUNDAI_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
agosto = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025 (HASTA 19-08)/Paso1.2_HYUNDAI_AGOSTO 2025 (HASTA 19-08)_listo.xlsx', dtype = {"# de venta": str})

dfs = [julio, agosto]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/VENTAS_TOTALES_HYUNDAI_JULIO_AGOSTO_19_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)