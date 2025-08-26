"""
UNIÓN DE VENTAS CON ESTADOS FILTRADOS
"""

import pandas as pd
import re

mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/AGOSTO 2025 (HASTA 12-08)/Paso3_MERCADOREPUESTOS_AGOSTO 2025 (HASTA 12-08)_listo.xlsx', dtype = {"# de venta": str})

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

mercadorepuestos["SKU_limpio"] = mercadorepuestos["SKU"].apply(limpiar_sku)
mercadorepuestos['SKU_limpio'] = mercadorepuestos['SKU_limpio'].str.replace(r'\(\s*[Xx]\s*(\d{1,3})\s*\)', r' X\1', regex=True)
mercadorepuestos["SKU_limpio"] = mercadorepuestos["SKU_limpio"].str.replace(r"\([^)]*\)", "", regex=True).str.strip()
mercadorepuestos["SKU_limpio"] = mercadorepuestos["SKU_limpio"].str.replace(r"\s*/\s*", " / ", regex=True)
mercadorepuestos["SKU_limpio"] = mercadorepuestos["SKU_limpio"].str.replace(r"X\s+(\d+)", r"X\1", regex=True)
mercadorepuestos["SKU_limpio"] = mercadorepuestos["SKU_limpio"].str.replace(
    r"(?<!/)\s(?=[A-Z]{2,3}-\s)", 
    " / ", 
    regex=True
)
mercadorepuestos["SKU_limpio"] = mercadorepuestos["SKU_limpio"].str.replace(r"\s{2,}", " ", regex=True).str.strip()

mercadorepuestos["Proveedor_siglas"] = mercadorepuestos["SKU_limpio"].apply(obtener_proveedores)
mercadorepuestos["Proveedor único"] = mercadorepuestos["Proveedor_siglas"].apply(lambda x: "Sí" if len(x) == 1 else "No")
mercadorepuestos["Proveedor"] = mercadorepuestos["Proveedor_siglas"].apply(lambda x: " / ".join(x))

mercadorepuestos = mercadorepuestos.drop(columns = ['Proveedor_siglas'])

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/AGOSTO 2025 (HASTA 12-08)/VENTAS_MERCADOREPUESTOS_AGOSTO_2025_HASTA_12.xlsx'
mercadorepuestos.to_excel(output_path, index = False)