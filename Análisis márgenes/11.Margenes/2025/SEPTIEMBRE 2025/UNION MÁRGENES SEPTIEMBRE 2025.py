"""
CASO ESPECIAL: Unión de archivos 01/09 - 07/09 y 08/09 - 30/09
"""

import pandas as pd

sept1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/SEPTIEMBRE 2025 (HASTA 07-09)/SEPTIEMBRE 2025 (HASTA 07-09) CONSOLIDADO MÁRGENES.xlsx', dtype = {"# de venta": str})
sept2 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/SEPTIEMBRE 2025 (0830)/SEPTIEMBRE 2025 (0830) CONSOLIDADO MÁRGENES.xlsx', dtype = {"# de venta": str})

dfs = [sept1, sept2]

sept = pd.concat(dfs, ignore_index = True)
print(sept.shape)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/SEPTIEMBRE 2025/SEPTIEMBRE 2025 CONSOLIDADO MÁRGENES.xlsx'
sept.to_excel(output_path, index = False)