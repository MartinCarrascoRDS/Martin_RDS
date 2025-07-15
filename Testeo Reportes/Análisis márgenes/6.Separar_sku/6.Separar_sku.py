"""
Paso 6:
Separar los SKU de cada uno de los productos en distintas columnas según el separador " / ".
"""

import pandas as pd
import re

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/5.Limpieza_sku/Paso5_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str})

def expand_sku(sku):
    if pd.isna(sku):
        return []
    sku = str(sku).strip()
    if sku == "":
        return []

    parts = [s.strip() for s in sku.split(" / ")]
    expanded = []
    i = 0
    while i < len(parts):
        item = parts[i]

        # CASO 1: es un multiplicador suelto tipo X2
        match_mult = re.fullmatch(r"x(\d+)", item.lower())
        if match_mult and expanded:
            count = int(match_mult.group(1))
            expanded.extend([expanded[-1]] * (count - 1))  # ya hay una, agrega el resto

        else:
            # CASO 2: SKU con multiplicador pegado al final (ejemplo "AL- 2352 X2")
            match_embedded = re.fullmatch(r"(.*)\s+X(\d+)", item, re.IGNORECASE)
            if match_embedded:
                sku_base = match_embedded.group(1).strip()
                count = int(match_embedded.group(2))
                expanded.extend([sku_base] * count)
            else:
                # CASO 3: SKU normal
                expanded.append(item)

        i += 1
    return expanded

sku_expanded = df['SKU_limpio'].apply(expand_sku)

max_length = sku_expanded.apply(len).max()

sku_df = pd.DataFrame(sku_expanded.tolist(), columns=[f'SKU_{i+1}' for i in range(max_length)])

df_final = pd.concat([df, sku_df], axis=1)

output_file = '/Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/6.Separar_sku/Paso6_listo.xlsx'
df_final.to_excel(output_file, index=False)