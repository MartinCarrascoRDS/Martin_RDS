"""
UNIÓN DE VENTAS TOTALES ENERO 2024 - JULIO 2025

Existen datos faltantes.
- Enero 2024: falta Autosol, Hyundai, Indusol y RDS1.
- Febrero 2024: faltan todas las cuentas. 
- Marzo 2024: falta Autosol e Indusol.
- Abril 2024: falta Autosol, RDS3 tiene muchos datos faltantes.
- Mayo 2024: falta Autosol, Blackparts tiene muchos datos faltantes.
- Junio 2024: falta Autosol.
- Julio 2024: falta Autosol.
- Agosto 2024: faltan todas las cuentas.
"""

import os
import glob
import pandas as pd

ruta_base = "/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados"

años_meses = {
    "2024": ["ENERO 2024", "FEBRERO 2024", "MARZO 2024", "ABRIL 2024", "MAYO 2024", "JUNIO 2024", "JULIO 2024", "AGOSTO 2024", "SEPTIEMBRE 2024", "OCTUBRE 2024", "NOVIEMBRE 2024", "DICIEMBRE 2024"],
    "2025": ["ENERO 2025", "FEBRERO 2025", "MARZO 2025", "ABRIL 2025", "MAYO 2025", "JUNIO 2025", "JULIO 2025"]
}

dfs_meses = []

for año, meses in años_meses.items():
    carpeta_año = os.path.join(ruta_base, año)

    for mes in meses:
        carpeta_mes = os.path.join(carpeta_año, mes)

        if not os.path.exists(carpeta_mes):
            print(f"La carpeta {mes} no existe, se omite.")
            continue
        
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

ventas_enero_2024_julio_2025 = pd.concat(dfs_meses, ignore_index=True)

print(f"\nDataFrame final: {ventas_enero_2024_julio_2025.shape[0]} filas y {ventas_enero_2024_julio_2025.shape[1]} columnas")

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/Multimes/VENTAS_TOTALES_CONSOLIDADO_ENERO_2024_JULIO_2025.xlsx'
ventas_enero_2024_julio_2025.to_excel(output_path, index = False)