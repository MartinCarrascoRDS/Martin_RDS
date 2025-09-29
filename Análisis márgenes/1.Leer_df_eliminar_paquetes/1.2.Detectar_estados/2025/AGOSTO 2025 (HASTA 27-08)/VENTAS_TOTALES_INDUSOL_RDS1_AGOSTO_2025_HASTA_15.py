"""
Unión de ventas totales de Indusol y RDS1 para agosto de 2025 (hasta 27-08).
"""

import pandas as pd

indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025 (HASTA 27-08)/Paso1.2_INDUSOL_AGOSTO 2025 (HASTA 27-08)_listo.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025 (HASTA 27-08)/Paso1.2_RDS1_AGOSTO 2025 (HASTA 27-08)_listo.xlsx', dtype = {"# de venta": str})

dfs = [indusol, rds1]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/AGOSTO 2025 (HASTA 27-08)/VENTAS_TOTALES_INDUSOL_RDS1_AGOSTO_2025_HASTA_27.xlsx'
df_consolidado.to_excel(output_path, index = False)