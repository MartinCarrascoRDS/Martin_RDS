"""
Paso 1.1
Limpieza de sku para ingresos totales
Valores netos donde corresponda
"""

import pandas as pd
import numpy as np
import re
import os

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = 2024 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS

archivo_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_{cuenta_meli}_{fecha}_listo.xlsx'
hoja_ventas = 'Sheet1'

df = pd.read_excel(archivo_ventas, sheet_name = hoja_ventas, dtype = {"# de venta": str})

# def limpiar_sku(sku):
#     if pd.isna(sku):
#         return sku
#     sku = str(sku).upper().strip()
#     partes = re.split(r"\s*/\s*", sku)
#     partes_limpias = [
#         re.sub(r"^(?:F-\s*|XX-\s*)+", "", p).strip()
#         for p in partes
#     ]
#     return " / ".join(partes_limpias)

df = df[df['SKU'].notna()]

def limpiar_sku(sku):
    """Limpia prefijos 'F- ' y  'XX- ' al inicio de cada fragmento separado por '/'. """
    if pd.isna(sku):
        return sku
    sku = str(sku).upper()
    partes = re.split(r"\s*/\s*", sku)
    partes_limpias = [
        re.sub(r"^(F-\s*|XX-\s*)+", "", parte).strip()
        for parte in partes
    ]
    return " / ".join(partes_limpias)

def limpiar_sku2(sku):
    """Limpia 'F- ', 'XX- ' y 'Z- ' en cualquier parte de cada fragmento separado por '/'. """
    if pd.isna(sku):
        return sku
    sku = str(sku).upper()
    partes = re.split(r"\s*/\s*", sku)
    partes_limpias = [
        re.sub(r"(F-\s*|XX-\s*|Z-\s*)+", "", parte).strip()
        for parte in partes
    ]
    return " / ".join(partes_limpias)

# 19/08/2025: PARA LOS PRÓXIMOS ANÁLISIS, DECIDIR USAR limpiar_sku o limpiar_sku2 (creo que limpiar_sku2 es más completo)

df["SKU_MAYUSC"] = (
    df["SKU"]
    .astype(str)
    .str.upper()
    .str.strip()
)

# Eliminar filas que tengan SKU vacío
df = df[df["SKU_MAYUSC"].notna() & (df["SKU_MAYUSC"] != "")]
# Aplicar limpieza básica y de prefijos
df["SKU_limpio"] = df["SKU"].apply(limpiar_sku)

# Detectar multiplicadores como (X2), (X 2), etc., y convertirlos a "X2"
df['SKU_limpio'] = df['SKU_limpio'].str.replace(r'\(\s*[Xx]\s*(\d{1,3})\s*\)', r' X\1', regex=True)

# Eliminar contenido entre paréntesis
df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()

# Corregir espacios alrededor de "/"
df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\s*/\s*", " / ", regex=True)

# Asegurar que "X 2", "X   10", etc. pasen a "X2", "X10"
df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"X\s+(\d+)", r"X\1", regex=True)

# Arreglar espacios antes de BI-, IT-, etc. sin barra, agregando " / "
df["SKU_limpio"] = df["SKU_limpio"].str.replace(
    r"(?<!/)\s(?=[A-Z]{2,3}-\s)", 
    " / ", 
    regex=True
)

# Limpiar espacios dobles restantes
df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()

def obtener_proveedores(sku_limpio):
    partes = str(sku_limpio).split(" / ")
    siglas = set()

    for parte in partes:
        match = re.match(r"([A-Z]{2,3})-", parte.strip())
        if match:
            siglas.add(match.group(1))

    return sorted(siglas)

df["Proveedor_siglas"] = df["SKU_limpio"].apply(obtener_proveedores)
df["Proveedor único"] = df["Proveedor_siglas"].apply(lambda x: "Sí" if len(x) == 1 else "No")
df["Proveedor"] = df["Proveedor_siglas"].apply(lambda x: " / ".join(x))

df = df.drop(columns = ['Proveedor_siglas'])

# Calcular ingresos netos
df['Ingresos por venta (CLP)'] = df['Unidades'] * df['Precio unitario de venta de la publicación (CLP)']
df['Ingresos por venta (CLP) Neto'] = df['Ingresos por venta (CLP)'] / 1.19

# Guardar archivo
output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/{año}/{fecha}'
os.makedirs(output_folder, exist_ok=True)
output_path = f'{output_folder}/Paso1.1_{cuenta_meli}_{fecha}_listo.xlsx'
df.to_excel(output_path, index=False)