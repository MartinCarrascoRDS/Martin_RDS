"""
Unión de ventas totales de enero a julio 2024 y 2025.

Recordar que algunas de las ventas en este ejercicio tienen solo ventas full, por lo que el excel resultante de este script debe ser usado solamente para análisis de ventas full.
"""

import pandas as pd

ventas2024 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2024/VENTAS_TOTALES_CONSOLIDADO_ENERO_JULIO_2024.xlsx', dtype = {"# de venta": str})
ventas2025 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/VENTAS_TOTALES_CONSOLIDADO_ENERO_JULIO_2025.xlsx', dtype = {"# de venta": str})

ventas_enero_julio_2024_y_2025 = pd.concat([ventas2024, ventas2025], ignore_index = True)

print(f"\nDataFrame final: {ventas_enero_julio_2024_y_2025.shape[0]} filas y {ventas_enero_julio_2024_y_2025.shape[1]} columnas")

ventas_enero_julio_2024_y_2025.to_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/Multimes/VENTAS_TOTALES_CONSOLIDADO_ENERO_JULIO_2024_Y_2025.xlsx', index = False)