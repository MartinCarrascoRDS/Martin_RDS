"""
Paso 10:
Eliminar registros sin costos de las bases de datos de ventas.
Este paso es crucial para asegurar que los análisis posteriores se realicen sobre datos relevantes y completos, evitando distorsiones en los resultados (márgenes inflados).
También se generará un archivo con los registros que fueron eliminados, para su revisión.
"""

import pandas as pd
import os

cuenta_meli = input("Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ")
fecha = input("Indique la fecha del análisis (ejemplo: JUNIO 2025): ")

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/9.Descuentos/Paso9_listo.xlsx'
hoja_venta = 'Sheet1'
df = pd.read_excel(archivo_venta, sheet_name=hoja_venta, dtype={'# de venta': str})

columnas_sku = [col for col in df.columns if col.startswith("SKU_") and col[-1].isdigit()]
columnas_costo = [f"Costo_SKU_{col.split('_')[-1]}" for col in columnas_sku]

def detectar_sku_faltante(row):
    if row['Forma de entrega'] == 'Mercado Envíos Full':
        return "Sin SKU faltante" if pd.notna(row['Costo_full']) else "SKU faltante"
    else:
        for sku_col, costo_col in zip(columnas_sku, columnas_costo):
            sku = row.get(sku_col)
            costo = row.get(costo_col)
            if pd.notna(sku) and pd.isna(costo):
                return "SKU faltante"
        return "Sin SKU faltante"    

df['SKU_faltante'] = df.apply(detectar_sku_faltante, axis=1)

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/10.Eliminar_sin_costos/{fecha}'
os.makedirs(output_folder, exist_ok=True)

output_path = f'{output_folder}/Paso10_{cuenta_meli}_{fecha}_completo.xlsx'
df.to_excel(output_path, index=False)

df_filtrado = df[df['SKU_faltante'] == "Sin SKU faltante"].copy()
df_faltantes = df[df['SKU_faltante'] == "SKU faltante"].copy()

print(f"Existen {df_filtrado.shape[0]} registros sin SKU faltante.")

output_path1 = f'{output_folder}/Paso10_{cuenta_meli}_{fecha}_sin_sku_faltantes.xlsx'
df_filtrado.to_excel(output_path1, index=False)

output_path2 = f'{output_folder}/Paso10_{cuenta_meli}_{fecha}_sku_faltantes.xlsx'
df_faltantes.to_excel(output_path2, index=False)