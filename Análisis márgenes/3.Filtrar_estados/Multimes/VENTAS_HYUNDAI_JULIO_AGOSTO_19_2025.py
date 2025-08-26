"""
UNIÓN DE VENTAS HYUNDAI JULIO - AGOSTO (19) 2025
"""

import os
import glob
import pandas as pd

ruta_base = "/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025"

meses = [
    "JULIO 2025",
    "AGOSTO 2025 (HASTA 19-08)"
]

dfs_meses = []

for mes in meses:
    carpeta_mes = os.path.join(ruta_base, mes)

    archivos_mes = [
        f for f in glob.glob(os.path.join(carpeta_mes, "*HYUNDAI*listo.xlsx"))
        if os.path.isfile(f)
    ]

    if archivos_mes:
        df_mes = pd.concat([pd.read_excel(f, dtype = {"# de venta": str}) for f in archivos_mes], ignore_index=True)
        dfs_meses.append(df_mes)
        print(f"Se concatenaron {len(archivos_mes)} archivos excel de ventas en {mes}")
    else:
        print(f"No se encontraron archivos con Paso 3 listo en {mes}")

ventas_enero_julio = pd.concat(dfs_meses, ignore_index=True)

print(f"\nDataFrame final: {ventas_enero_julio.shape[0]} filas y {ventas_enero_julio.shape[1]} columnas")

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/VENTAS_HYUNDAI_JULIO_AGOSTO_19_2025.xlsx'
ventas_enero_julio.to_excel(output_path, index = False)