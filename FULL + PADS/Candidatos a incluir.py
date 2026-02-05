"""
A partir de este código, se decide qué productos pueden ser incluidos en los anuncios de Mercado Libre.
"""

import pandas as pd
import os

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: 20250821, formato añomesdia): ')
fecha_dt = pd.to_datetime(str(fecha), format = '%Y%m%d')

anuncios_actuales = pd.read_excel(f'/Users/martincarrasco/Desktop/Martín_Carrasco/FULL + PADS/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios actuales/ANUNCIOS PADS {cuenta_meli} {fecha}.xlsx', sheet_name = "Planilla de Anuncios", skiprows = 1)
publicaciones = pd.read_excel(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/{cuenta_meli}/PUBLICACIONES {cuenta_meli} {fecha}.xlsx', dtype = {'SellerCustomSKU': str, 'Att_SellerSKU': str})

publicaciones['Número de publicación'] = "MLC" + publicaciones['ID'].astype(str)
publicaciones.rename(columns = {'Att_SellerSKU': 'SKU'}, inplace = True)
publicaciones = publicaciones[['Número de publicación', 'SKU', 'Titulo', 'Status', 'Precio', 'CantVendida', 'TipoEnvio', 'FechaDeCreacion']]

anuncios_actuales = anuncios_actuales.iloc[2:].reset_index(drop = True)
anuncios_actuales = anuncios_actuales[['ITEM_ID', 'ITEM_TITLE', 'CAMPAIGN_NAME', 'AD_STATUS']]

pads_id = set(anuncios_actuales['ITEM_ID'].unique())

publicaciones['FechaDeCreacion'] = (
    pd.to_datetime(publicaciones['FechaDeCreacion'], utc=True)
      .dt.tz_convert(None)
)
publicaciones['TipoEnvio'] = publicaciones['TipoEnvio'].fillna('Acuerdo de entrega')

limite_fecha = fecha_dt - pd.DateOffset(months = 3)

publicaciones = publicaciones[publicaciones['FechaDeCreacion'] <= limite_fecha]

anuncios_nuevos = publicaciones[
    (~publicaciones['SKU'].astype(str).str.contains(r"XX-\s*", na = False)) & # No contiene "XX- " en SKU
    (~publicaciones['SKU'].astype(str).str.contains(r"F-\s*", na = False)) & # No contiene "F- " en SKU
    (~publicaciones['SKU'].astype(str).str.contains(r"Z-\s*", na = False)) & # No contiene "Z- " en SKU
    (publicaciones['Status'] == 'ACTIVO') &
    (publicaciones['Precio'] > 20000) &
    (~publicaciones['Número de publicación'].isin(pads_id)) & # No está en los anuncios actuales
    (publicaciones['TipoEnvio'] != 'Fulfillment') # No es Fulfillment
]

print(f"Existen {anuncios_nuevos.shape[0]} anuncios que pueden ser incluidos en la cuenta {cuenta_meli}")

anuncios_nuevos = anuncios_nuevos.drop_duplicates(
    subset = 'Número de publicación',
    keep = 'first'
)
anuncios_nuevos = anuncios_nuevos.sort_values(by = 'CantVendida', ascending = False)

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/FULL + PADS/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir'
os.makedirs(output_folder, exist_ok = True)
output_path = f'{output_folder}/CANDIDATOS A INCLUIR {cuenta_meli} {fecha}.xlsx'
anuncios_nuevos.to_excel(output_path, index = False)

print(f"Fecha de análisis (fecha_dt): {fecha_dt.date()}")
print(f"Limite (3 meses atrás): {limite_fecha.date()}")
print(f"Total publicaciones después del filtro de 3 meses: {publicaciones.shape[0]}")
print(f"Total anuncios candidatos (aplicadas otras reglas): {anuncios_nuevos.shape[0]}")
print(f"Archivo guardado en: {output_path}")