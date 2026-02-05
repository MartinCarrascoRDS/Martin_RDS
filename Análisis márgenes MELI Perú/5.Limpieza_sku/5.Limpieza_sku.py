"""
Paso 5:
Limpiar el SKU, eliminando "XX- ", "F- ", y eliminando espacios antes y después, para poder
hacer el cruce con las bases de costo
"""

import pandas as pd
import re
import os
from pipeline.procesamiento.funciones_para_analisis_margen import limpiar_sku, extraer_año_desde_fecha

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = extraer_año_desde_fecha(fecha)

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/4.Forzar_formatos/Paso4_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str, 'No. Paquete': str})

"""df["SKU_MAYUSC"] = (
    df["SKU"]
    .astype(str)
    .str.upper()
    .str.strip()
)

df["SKU_limpio"] = (
    df["SKU"]
    .astype(str)
    .str.upper()
    .str.replace(r"^((F- ?)|(XX- ?))+", "", regex=True)
    .str.strip()
)

df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()

df["SKU_limpio"] = df["SKU_limpio"].str.replace(
    r"(?<!/)\s(?=[A-Z]{2,3}-\s)", 
    " / ", 
    regex=True
)

df["SKU_limpio"] = df["SKU_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/5.Limpieza_sku/Paso5_listo.xlsx'
df.to_excel(output_path, index = False)"""

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

"""
PASOS QUE AHORA ESTÁN INCLUIDOS EN LA FUNCIÓN DE LIMPIEZA DE SKU
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
"""
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

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/5.Limpieza_sku/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)
output_path = f'{output_folder}/{fecha} {cuenta_meli} VENTAS.xlsx'
df.to_excel(output_path, index = False)