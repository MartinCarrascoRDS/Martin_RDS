"""
UNIÓN DE ARCHIVOS DE VENTAS RDS1 E INDUSOL PARA ANÁLISIS AUTOMARCO, AUTOTEC Y GABTEC JULIO 2025 (HASTA 24-07)
"""

import pandas as pd
import re

indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/JULIO 2025 (HASTA 24-07)/Paso3_INDUSOL_JULIO 2025 (HASTA 24-07)_listo.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/JULIO 2025 (HASTA 24-07)/Paso3_RDS1_JULIO 2025 (HASTA 24-07)_listo.xlsx', dtype = {"# de venta": str})

meses_es = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

def convertir_fechas(fecha_str):
    """
    Junto con meses_es, fue directamente obtenida del paso 4.
    """
    if pd.isna(fecha_str):
        return pd.NaT
    try:
        fecha_str = str(fecha_str).lower()
        fecha_str = re.sub(r"\s*hs\.?", "", fecha_str)
        partes = fecha_str.split(' de ')
        if len(partes) < 3:
            return pd.NaT
        dia = partes[0].strip().zfill(2)
        mes = meses_es.get(partes[1].strip(), '01')
        año_hora = partes[2].strip()
        año = año_hora.split()[0]
        return pd.to_datetime(f"{año}/{mes}/{dia}", format="%Y/%m/%d")
    except Exception:
        return pd.NaT

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

dfs = [indusol, rds1]
df_consolidado = pd.concat(dfs, ignore_index = True)
df_consolidado = df_consolidado.fillna(0)

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

if 'Fecha de venta' in df_consolidado.columns:
    df_consolidado['Fecha de venta'] = df_consolidado['Fecha de venta'].apply(convertir_fechas)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/JULIO 2025 (HASTA 24-07)/VENTAS_INDUSOL_RDS1_JULIO_2025_HASTA_24.xlsx'
df_consolidado.to_excel(output_path, index = False)