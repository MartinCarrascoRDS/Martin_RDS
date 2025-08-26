"""
UNIÓN DE MÁRGENES JULIO - AGOSTO (19) 2025
"""

import pandas as pd

julio = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/JULIO 2025/MÁRGENES HYUNDAI JULIO 2025.xlsx', dtype = {"# de venta": str})
agosto = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/AGOSTO 2025 (HASTA 19-08)/MÁRGENES HYUNDAI AGOSTO 2025 (HASTA 19-08).xlsx', dtype = {"# de venta": str})

dfs = [julio, agosto]

df_consolidado = pd.concat(dfs, ignore_index = True)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/MÁRGENES_HYUNDAI_JULIO_AGOSTO_19_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)