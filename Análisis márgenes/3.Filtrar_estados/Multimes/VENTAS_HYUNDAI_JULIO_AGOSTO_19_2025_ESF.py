"""
UNIÓN DE VENTAS HYUNDAI JULIO - AGOSTO (19) 2025
"""

import os
import glob
import re
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
        f for f in glob.glob(os.path.join(carpeta_mes, "*HYUNDAI*omitido.xlsx"))
        if os.path.isfile(f)
    ]

    if archivos_mes:
        df_mes = pd.concat([pd.read_excel(f, dtype = {"# de venta": str}) for f in archivos_mes], ignore_index=True)
        dfs_meses.append(df_mes)
        print(f"Se concatenaron {len(archivos_mes)} archivos excel de ventas en {mes}")
    else:
        print(f"No se encontraron archivos con Paso 3 omitido en {mes}")

ventas_enero_julio = pd.concat(dfs_meses, ignore_index=True)

print(f"\nDataFrame final: {ventas_enero_julio.shape[0]} filas y {ventas_enero_julio.shape[1]} columnas")

def limpiar_sku(sku):
    """
    Directamente obtenida del paso 5.
    Limpia prefijos F-, XX- al inicio de cada fragmento separado por '/'. 
    """
    if pd.isna(sku):
        return sku
    sku = str(sku).upper()
    partes = re.split(r"\s*/\s*", sku)
    partes_limpias = [
        re.sub(r"^(F-\s*|XX-\s*)+", "", parte).strip()
        for parte in partes
    ]
    return " / ".join(partes_limpias)

def obtener_proveedores(sku_limpio):
    """
    Directamente obtenido del paso 5.
    """
    partes = str(sku_limpio).split(" / ")
    siglas = set()

    for parte in partes:
        match = re.match(r"([A-Z]{2,3})-", parte.strip())
        if match:
            siglas.add(match.group(1))

    return sorted(siglas)

ventas_enero_julio["SKU_limpio"] = ventas_enero_julio["SKU"].apply(limpiar_sku)
ventas_enero_julio['SKU_limpio'] = ventas_enero_julio['SKU_limpio'].str.replace(r'\(\s*[Xx]\s*(\d{1,3})\s*\)', r' X\1', regex=True)
ventas_enero_julio["SKU_limpio"] = ventas_enero_julio["SKU_limpio"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()
ventas_enero_julio["SKU_limpio"] = ventas_enero_julio["SKU_limpio"].str.replace(r"\s*/\s*", " / ", regex=True)
ventas_enero_julio["SKU_limpio"] = ventas_enero_julio["SKU_limpio"].str.replace(r"X\s+(\d+)", r"X\1", regex=True)
ventas_enero_julio["SKU_limpio"] = ventas_enero_julio["SKU_limpio"].str.replace(
    r"(?<!/)\s(?=[A-Z]{2,3}-\s)", 
    " / ", 
    regex=True
)
ventas_enero_julio["SKU_limpio"] = ventas_enero_julio["SKU_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()

ventas_enero_julio["Proveedor_siglas"] = ventas_enero_julio["SKU_limpio"].apply(obtener_proveedores)
ventas_enero_julio["Proveedor único"] = ventas_enero_julio["Proveedor_siglas"].apply(lambda x: "Sí" if len(x) == 1 else "No")
ventas_enero_julio["Proveedor"] = ventas_enero_julio["Proveedor_siglas"].apply(lambda x: " / ".join(x))

ventas_enero_julio = ventas_enero_julio.drop(columns = ['Proveedor_siglas'])

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/VENTAS_HYUNDAI_JULIO_AGOSTO_19_2025_ESF.xlsx'
ventas_enero_julio.to_excel(output_path, index = False)