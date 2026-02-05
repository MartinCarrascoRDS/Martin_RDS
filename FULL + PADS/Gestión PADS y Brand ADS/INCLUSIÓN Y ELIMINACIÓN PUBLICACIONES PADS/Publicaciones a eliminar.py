"""
De los archivos que actualmente se encuentran en PADS, se evalua cuáles deben ser eliminados por bajo rendimiento en ventas.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from pathlib import Path

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: 20250821, formato añomesdia): ')
fecha_dt = pd.to_datetime(str(fecha), format = '%Y%m%d')

print('RECORDAR ACTUALIZAR EL PATH DEL REPORTE DE VENTAS RDS ANTES DE EJECUTAR EL CÓDIGO\n' \
'(El reporte de venta se encuentra en computador windows, con el que se hacen los reportes de ventas acumulados desde enero de RDS)')

path_anuncios = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/FULL + PADS/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios actuales/ANUNCIOS PADS {cuenta_meli} {fecha}.xlsx')
path_ventas_rds = Path('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/CONSOLIDADO/ENERO 2025 - OCTUBRE 2025 VENTAS TOTALES.xlsx') # ACTUALIZAR ESTE PATH CUANDO CORRESPONDA
path_publicaciones = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/{cuenta_meli}/PUBLICACIONES {cuenta_meli} {fecha}.xlsx')

anuncios = pd.read_excel(path_anuncios, sheet_name = 'Planilla de Anuncios', skiprows = 1)
ventas_rds = pd.read_excel(path_ventas_rds, usecols = ['# de publicación', '# de venta', 'Fecha de venta', 'Cuenta Meli',
                                                       'Estado', 'Venta por publicidad', 'Unidades', 'Título de la publicación',
                                                       'SKU_limpio', 'Ingresos por venta (CLP) Neto', 'Clasificación Estado'],
                           dtype = {'# de publicación': str, '# de venta': str, 'SKU_limpio': str})
publicaciones = pd.read_excel(path_publicaciones, dtype = {'SellerCustomSKU': str, 'Att_SellerSKU': str})

publicaciones['Número de publicación'] = "MLC" + publicaciones['ID'].astype(str)
publicaciones.rename(columns = {'Att_SellerSKU': 'SKU'}, inplace = True)
publicaciones = publicaciones[['Número de publicación', 'SKU', 'Titulo', 'Status', 'Precio', 'CantVendida', 'TipoEnvio', 'FechaDeCreacion']]
publicaciones['FechaDeCreacion'] = (
    pd.to_datetime(publicaciones['FechaDeCreacion'], utc=True)
      .dt.tz_convert(None)
)
publicaciones['TipoEnvio'] = publicaciones['TipoEnvio'].fillna('Acuerdo de entrega')

anuncios = anuncios.iloc[2:].reset_index(drop = True)
anuncios = anuncios[['ITEM_ID', 'ITEM_TITLE', 'CAMPAIGN_NAME', 'AD_STATUS']]
pads_id = set(anuncios['ITEM_ID'].unique())

ventas_rds = ventas_rds[ventas_rds['Cuenta Meli'] == cuenta_meli]
ventas_rds.columns = (
    ventas_rds.columns
    .astype(str)
    .str.strip()                           # elimina espacios al inicio y final
    .str.replace("\u00A0", " ", regex=False)  # elimina NBSP
    .str.replace("\u2007", " ", regex=False)  # espacio figura
    .str.replace("\u202F", " ", regex=False)  # espacio estrecho
    .str.replace("\t", "", regex=False)       # elimina tabs
)
ventas_rds['YearMonth'] = ventas_rds['Fecha de venta'].dt.to_period('M').astype(str)
ventas_rds = ventas_rds[ventas_rds['Clasificación Estado'] == 'Venta']
ventas_rds = ventas_rds[ventas_rds['Venta por publicidad'] == 'Sí']
ventas_rds = ventas_rds.merge(
    publicaciones[['Número de publicación', 'FechaDeCreacion']],
    left_on = '# de publicación',
    right_on = 'Número de publicación',
    how = 'left'
)

meses_ordenados = sorted(ventas_rds['YearMonth'].unique())
ultimos_2_meses = meses_ordenados[-2:] if len(meses_ordenados) >= 2 else []
print("Últimos 2 meses detectados: ", ultimos_2_meses)

publicaciones_en_pads = publicaciones[publicaciones['Número de publicación'].isin(pads_id)]
publicaciones_en_pads['EsFull'] = publicaciones_en_pads['TipoEnvio'] == 'Fulfillment'
full_ids = set(publicaciones_en_pads[publicaciones_en_pads['EsFull']]['Número de publicación'])

ventas_por_mlc = ventas_rds.groupby('# de publicación')['Unidades'].sum().to_dict()

malos = []
detalles = []

umbral_4m = fecha_dt - pd.DateOffset(months = 4)

for mlc, grupo in ventas_rds.groupby('# de publicación'):

    detalle = {
        'ITEM_MLC': mlc,
        'Meses_con_venta': None,
        'Pendiente': None,
        'Unidades vendidas': ventas_por_mlc.get(mlc, 0),
        'Motivo': None
    }

    meses_producto = grupo['YearMonth'].unique()
    ventas_totales = grupo['Unidades'].sum()
    meses_con_ventas = len(meses_producto)
    detalle['Meses_con_venta'] = ", ".join(meses_producto)

    fecha_creacion = grupo['FechaDeCreacion'].iloc[0]
    
    if fecha_creacion >= umbral_4m:
        detalle['Motivo'] = 'Producto creado hace menos de 4 meses'
        detalles.append(detalle)
        continue

    if mlc in full_ids:
        malos.append(mlc)
        detalle['Motivo'] = 'Producto en Full'
        detalles.append(detalle)
        continue

    if ventas_totales < 10:
        malos.append(mlc)
        detalle['Motivo'] = 'Menos de 10 unidades vendidas'
        detalles.append(detalle)
        continue
    
    if meses_con_ventas < 3:
        malos.append(mlc)
        detalle['Motivo'] = 'Menos de 3 meses con ventas'
        detalles.append(detalle)
        continue

    if not any(m in meses_producto for m in ultimos_2_meses):
        malos.append(mlc)
        detalle['Motivo'] = 'No tiene ventas en los últimos 2 meses'
        detalles.append(detalle)
        continue

    tmp = (
        grupo.groupby('YearMonth')['Ingresos por venta (CLP) Neto']
        .sum()
        .reset_index()
        .sort_values('YearMonth')
    )

    if len(tmp) < 2:
        malos.append(mlc)
        detalle['Motivo'] = 'Insuficientes meses para tendencia'
        detalles.append(detalle)
        continue

    tmp['mes_idx'] = np.arange(len(tmp))

    X = tmp[['mes_idx']].values
    y = tmp['Ingresos por venta (CLP) Neto'].values

    modelo = LinearRegression().fit(X, y)
    pendiente = modelo.coef_[0]
    detalle['Pendiente'] = pendiente

    if pendiente < 0:
        malos.append(mlc)
        detalle['Motivo'] = 'Tendencia de ventas negativa'
        detalles.append(detalle)
        continue

    detalle['Motivo'] = 'Buen rendimiento'
    detalles.append(detalle)

anuncios_eliminar = anuncios[anuncios['ITEM_ID'].isin(malos)]
dups = anuncios_eliminar['ITEM_ID'].value_counts()
print("ITEM_ID duplicados en la planilla de anuncios:")
print(dups[dups > 1])
anuncios_eliminar = anuncios_eliminar.merge(
    publicaciones[['Número de publicación', 'SKU', 'TipoEnvio', 'FechaDeCreacion']],
    left_on = 'ITEM_ID',
    right_on = 'Número de publicación',
    how = 'left'
)
anuncios_eliminar = anuncios_eliminar.merge(
    ventas_rds.groupby('# de publicación').agg({'Ingresos por venta (CLP) Neto': 'sum'}).reset_index(),
    left_on = 'ITEM_ID',
    right_on = '# de publicación',
    how = 'left'
)
anuncios_eliminar.rename(columns = {
    'Unidades': 'Unidades vendidas con publicidad',
    'Ingresos por venta (CLP) Neto': 'Ingresos netos con publicidad'
}, inplace = True)
anuncios_eliminar = anuncios_eliminar.merge(
    pd.DataFrame(detalles)[['ITEM_MLC', 'Meses_con_venta', 'Pendiente', 'Unidades vendidas', 'Motivo']],
    left_on = 'ITEM_ID',
    right_on = 'ITEM_MLC',
    how = 'left'
)
anuncios_eliminar.drop(columns = ['Número de publicación', '# de publicación', 'ITEM_MLC'], inplace = True)

output_folder = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/FULL + PADS/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a eliminar')
output_folder.mkdir(parents = True, exist_ok = True)
output_path = output_folder / f'ANUNCIOS A ELIMINAR PADS {cuenta_meli} {fecha}.xlsx'
anuncios_eliminar.to_excel(output_path, index = False)