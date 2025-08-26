"""
UNIÓN DE VENTAS CON ESTADOS SIN FILTRAR
"""

import pandas as pd
import re

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_AUTOSOL_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_BICISOL_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_BLACKPARTS_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_INDUSOL_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_MERCADOREPUESTOS_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_RDS1_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_RDS3_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_REICARS_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_TRIANA_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/Paso3_TYC_JULIO 2025_omitido.xlsx', dtype = {"# de venta": str})

dfs = [autosol, bicisol, blackparts, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)
df_consolidado = df_consolidado.fillna(0)

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
    partes = sku_limpio.split(" / ")
    siglas = set()

    for parte in partes:
        match = re.match(r"([A-Z]{2,3})-", parte.strip())
        if match:
            siglas.add(match.group(1))

    return sorted(siglas)

df_consolidado["SKU_limpio"] = df_consolidado["SKU"].apply(limpiar_sku)
df_consolidado['SKU_limpio'] = df_consolidado['SKU_limpio'].str.replace(r'\(\s*[Xx]\s*(\d{1,3})\s*\)', r' X\1', regex=True)
df_consolidado["SKU_limpio"] = df_consolidado["SKU_limpio"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()
df_consolidado["SKU_limpio"] = df_consolidado["SKU_limpio"].str.replace(r"\s*/\s*", " / ", regex=True)
df_consolidado["SKU_limpio"] = df_consolidado["SKU_limpio"].str.replace(r"X\s+(\d+)", r"X\1", regex=True)
df_consolidado["SKU_limpio"] = df_consolidado["SKU_limpio"].str.replace(
    r"(?<!/)\s(?=[A-Z]{2,3}-\s)", 
    " / ", 
    regex=True
)
df_consolidado["SKU_limpio"] = df_consolidado["SKU_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()

df_consolidado["Proveedor_siglas"] = df_consolidado["SKU_limpio"].apply(obtener_proveedores)
df_consolidado["Proveedor único"] = df_consolidado["Proveedor_siglas"].apply(lambda x: "Sí" if len(x) == 1 else "No")
df_consolidado["Proveedor"] = df_consolidado["Proveedor_siglas"].apply(lambda x: " / ".join(x))

df_consolidado = df_consolidado.drop(columns = ['Proveedor_siglas'])

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/JULIO 2025/VENTAS_CONSOLIDADO_JULIO_2025_ESF.xlsx'
df_consolidado.to_excel(output_path, index = False)