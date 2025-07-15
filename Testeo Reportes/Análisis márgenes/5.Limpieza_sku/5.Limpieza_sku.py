"""
Paso 5:
Limpiar el SKU, eliminando "XX- ", "F- ", y eliminando espacios antes y después, para poder
hacer el cruce con las bases de costo
"""

import pandas as pd
import re

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/4.Forzar_formatos/Paso4_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str})

df["SKU_MAYUSC"] = (
    df["SKU"]
    .astype(str)
    .str.upper()
    .str.strip()
)

df["SKU_limpio"] = (
    df["SKU"]
    .astype(str)
    .str.upper()
    .str.replace(r"(XX-|F-)\s*", "", regex=True)
    .str.strip()
)

df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()

df["SKU_limpio"] = df["SKU_limpio"].str.replace(
    r"(?<!/)\s(?=[A-Z]{2,3}-\s)", 
    " / ", 
    regex=True
)

df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/5.Limpieza_sku/Paso5_listo.xlsx'
df.to_excel(output_path, index = False)