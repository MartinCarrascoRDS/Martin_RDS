"""
Cruce de base de datos de ventas con base de datos PADS
"""

import pandas as pd
import os

cuenta_meli = input('Indique el nombre de la cuenta a la que corresponde este cruce (ejemplo: BICISOL): ')
fecha = input('Indique la fecha a la que corresponden las publicaciones en PADS (ejemplo: 20250910): ')


# Archivo de ventas se obtiene a partir del reporte de Power BI sobre las ventas correspondientes al análisis que se desee realizar
ventas = pd.read_excel(
    f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir/ANUNCIOS A INCLUIR {cuenta_meli} {fecha}.xlsx', # RECORDAR CAMBIAR PATH DE ACUERDO A QUE ARCHIVO SE QUIERE CRUZAR
    sheet_name = 'Sheet1'
)

pads = pd.read_excel(
    f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios actuales/ANUNCIOS PADS {cuenta_meli} {fecha}.xlsx',
    sheet_name = 'Planilla de Anuncios',
    skiprows = 1,
    usecols = ['ITEM_ID', 'CAMPAIGN_NAME', 'AD_STATUS']
)
pads = pads.iloc[2:].reset_index(drop = True)

campaign_a_mlc = pads.set_index('ITEM_ID')['CAMPAIGN_NAME'].to_dict()

ventas['Nombre Campaña PADS'] = ventas['# de publicación'].map(campaign_a_mlc)
ventas['Nombre Campaña PADS'] = ventas['Nombre Campaña PADS'].fillna('Sin PADS')

estado_a_mlc = pads.set_index('ITEM_ID')['AD_STATUS'].to_dict()

ventas['Estado PADS'] = ventas['# de publicación'].map(estado_a_mlc)
ventas['Estado PADS'] = ventas['Estado PADS'].fillna('Sin PADS')

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir'
os.makedirs(output_folder, exist_ok = True)
output_path = f'{output_folder}/ANUNCIOS A INCLUIR {cuenta_meli} {fecha}.xlsx'
ventas.to_excel(output_path, index = False)


"""
12/09/2025: ARREGLO MOMENTÁNEO CON ARCHIVOS DE ANUNCIOS A INCLUIR YA HECHOS, PORQUE NO SE HIZO LA COLUMNA DE NOMBRE DE CAMPAÑA

anuncios = pd.read_excel(
    f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir/ANUNCIOS A INCLUIR {cuenta_meli} {fecha}.xlsx'
)

campaign_a_mlc = pads.set_index('ITEM_ID')['CAMPAIGN_NAME'].to_dict()

anuncios['Nombre Campaña PADS'] = anuncios['# de publicación'].map(campaign_a_mlc)
anuncios['Nombre Campaña PADS'] = anuncios['Nombre Campaña PADS'].fillna('Sin PADS')

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir'
os.makedirs(output_folder, exist_ok = True)
output_path = f'{output_folder}/ANUNCIOS A INCLUIR {cuenta_meli} {fecha}.xlsx'
anuncios.to_excel(output_path, index = False)
"""