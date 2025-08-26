"""
UNIÓN DE VENTAS EN PAQUETE
"""

import pandas as pd


mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/AGOSTO 2025 (HASTA 12-08)/Paso1_ventas_paquete_MERCADOREPUESTOS_AGOSTO 2025 (HASTA 12-08).xlsx', dtype = {'# de venta': str})

mercadorepuestos['Ingresos por productos (CLP) Neto'] = mercadorepuestos['Ingresos por productos (CLP)'] / 1.19

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/2025/AGOSTO 2025 (HASTA 12-08)/VENTAS_PAQUETE_MERCADOREPUESTOS_AGOSTO_2025_HASTA_12.xlsx'
mercadorepuestos.to_excel(output_path, index = False)