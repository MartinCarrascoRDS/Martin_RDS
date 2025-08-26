"""
A partir de este código, se decide qué productos pueden ser incluidos en los anuncios de Mercado Libre.
"""

import pandas as pd
import os

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: 20252108, formato añomesdia): ')

anuncios_actuales = pd.read_excel(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios actuales/ANUNCIOS PADS {cuenta_meli} {fecha}.xlsx', sheet_name = "Planilla de Anuncios", skiprows = 3)
publicaciones = pd.read_excel(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/{cuenta_meli}/PUBLICACIONES {cuenta_meli} {fecha}.xlsx', dtype = {'SellerCustomSKU': str, 'Att_SellerSKU': str})

publicaciones['Número de publicación'] = "MLC" + publicaciones['ID'].astype(str)

publicaciones.rename(columns = {'SellerCustomSKU': 'SKU1', 'Att_SellerSKU': 'SKU2'}, inplace = True)

publicaciones = publicaciones[['Número de publicación', 'SKU1', 'SKU2', 'Titulo', 'Status', 'Precio', 'CantVendida']]
anuncios_actuales = anuncios_actuales[['Número de publicación', 'Título']]

pads_id = set(anuncios_actuales['Número de publicación'].unique())

anuncios_nuevos = publicaciones[
    (~publicaciones['SKU1'].astype(str).str.contains(r"XX-\s*", na = False)) & # No contiene "XX- " en SKU
    (~publicaciones['SKU1'].astype(str).str.contains(r"F-\s*", na = False)) & # No contiene "F- " en SKU
    (~publicaciones['SKU1'].astype(str).str.contains(r"Z-\s*", na = False)) & # No contiene "Z- " en SKU
    (~publicaciones['SKU2'].astype(str).str.contains(r"XX-\s*", na = False)) & # No contiene "XX- " en SKU
    (~publicaciones['SKU2'].astype(str).str.contains(r"F-\s*", na = False)) & # No contiene "F- " en SKU
    (~publicaciones['SKU2'].astype(str).str.contains(r"Z-\s*", na = False)) & # No contiene "Z- " en SKU
    (publicaciones['Status'] == 'ACTIVO') &
    (publicaciones['Precio'] > 20000) &
    (~publicaciones['Número de publicación'].isin(pads_id)) # No está en los anuncios actuales
]

print(f"Existen {anuncios_nuevos.shape[0]} anuncios nuevos para incluir en la cuenta {cuenta_meli}.")

anuncios_nuevos = anuncios_nuevos.drop_duplicates(
    subset = 'Número de publicación',
    keep = 'first'
)

anuncios_nuevos = anuncios_nuevos.sort_values(by = 'CantVendida', ascending = False)

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir/'
os.makedirs(output_folder, exist_ok = True)
output_path = f'{output_folder}/ANUNCIOS A INCLUIR {cuenta_meli} {fecha}.xlsx'
anuncios_nuevos.to_excel(output_path, index = False)