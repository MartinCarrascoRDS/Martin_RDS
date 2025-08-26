"""
UNIÓN DE VENTAS TOTALES ENERO - JULIO 2025
"""

import os
import glob
import pandas as pd
from pipeline.procesamiento.procesamiento_bases import convertir_fechas

ruta_base = "/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025"

meses = [
    "ENERO 2025",
    "FEBRERO 2025",
    "MARZO 2025",
    "ABRIL 2025",
    "MAYO 2025",
    "JUNIO 2025",
    "JULIO 2025"
]

dfs_meses = []

for mes in meses:
    carpeta_mes = os.path.join(ruta_base, mes)

    archivos_mes = [
        f for f in glob.glob(os.path.join(carpeta_mes, "Paso1.2*.xlsx"))
        if os.path.isfile(f)
    ]

    if archivos_mes:
        df_mes = pd.concat([pd.read_excel(f, dtype = {"# de venta": str}) for f in archivos_mes], ignore_index=True)
        dfs_meses.append(df_mes)
        print(f"Se concatenaron {len(archivos_mes)} archivos excel de ventas en {mes}")
    else:
        print(f"No se encontraron archivos Paso1.2 en {mes}")

ventas_enero_julio = pd.concat(dfs_meses, ignore_index=True)

print(f"\nDataFrame final: {ventas_enero_julio.shape[0]} filas y {ventas_enero_julio.shape[1]} columnas")

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/VENTAS_TOTALES_CONSOLIDADO_ENERO_JULIO_2025.xlsx'
ventas_enero_julio.to_excel(output_path, index = False)