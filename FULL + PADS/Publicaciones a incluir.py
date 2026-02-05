"""
Una vez generados los candidatos a incluir, este código selecciona los mejores productos en venta dentro de las ventas RDS de los últimos meses.
Se cruzará la información entre los candidatos a incluir y el último reporte de ventas RDS disponible.
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

path_candidatos = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/FULL + PADS/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir/CANDIDATOS A INCLUIR {cuenta_meli} {fecha}.xlsx')
path_ventas_rds = Path('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/CONSOLIDADO/ENERO 2025 - OCTUBRE 2025 VENTAS TOTALES.xlsx') # ACTUALIZAR ESTE PATH CUANDO CORRESPONDA
path_publicaciones = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Cuentas RDS/{cuenta_meli}/PUBLICACIONES {cuenta_meli} {fecha}.xlsx')
candidatos = pd.read_excel(path_candidatos, dtype = {'Número de publicación': str, 'SKU': str})
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
ventas_rds = ventas_rds[ventas_rds['Venta por publicidad'] != 'Sí']
ventas_rds = ventas_rds.merge(
    publicaciones[['Número de publicación', 'FechaDeCreacion']],
    left_on = '# de publicación',
    right_on = 'Número de publicación',
    how = 'left'
)

candidatos_ids = set(candidatos['Número de publicación'])

meses_ordenados = sorted(ventas_rds['YearMonth'].unique())
ultimos_2_meses = meses_ordenados[-2:] if len(meses_ordenados) >= 2 else []
print("Últimos 2 meses detectados: ", ultimos_2_meses)

ventas_por_mlc = ventas_rds.groupby('# de publicación')['Unidades'].sum().to_dict()

buenos = []
detalles = []

for mlc, grupo in ventas_rds.groupby('# de publicación'):

    total_ingresos = grupo['Ingresos por venta (CLP) Neto'].sum()
    fecha_creacion = grupo['FechaDeCreacion'].iloc[0]

    detalle = {
        '# de publicación': mlc,
        'Meses_con_venta': None,
        'Pendiente': None,
        'Unidades vendidas': ventas_por_mlc.get(mlc, 0),
        'Ingresos netos totales': total_ingresos,
        'Fecha de creación publicación': fecha_creacion,
        'Motivo': None
    }

    meses_producto = grupo['YearMonth'].unique()
    ventas_totales = grupo['Unidades'].sum()
    meses_con_ventas = len(meses_producto)
    detalle['Meses_con_venta'] = ", ".join(meses_producto)
    
    if ventas_totales <= 10:
        detalle['Motivo'] = '10 o menos unidades vendidas'
        detalles.append(detalle)
        continue

    if meses_con_ventas < 2:
        detalle['Motivo'] = 'Menos de 2 meses con venta'
        detalles.append(detalle)
        continue

    if not all(m in meses_producto for m in ultimos_2_meses):
        detalle['Motivo'] = '2 últimos meses sin venta'
        detalles.append(detalle)
        continue

    tmp = (
        grupo.groupby("YearMonth")['Ingresos por venta (CLP) Neto']
        .sum()
        .reset_index()
        .sort_values('YearMonth')
    )

    tmp['mes_idx'] = np.arange(len(tmp))

    X = tmp[['mes_idx']].values
    y = tmp['Ingresos por venta (CLP) Neto'].values

    modelo = LinearRegression().fit(X, y)
    pendiente = modelo.coef_[0]

    if pendiente <= 0:
        detalle['Motivo'] = 'Pendiente negativa o 0'
        detalles.append(detalle)
        continue
    
    detalle['Motivo'] = 'Cumple todos los criterios'
    detalles.append(detalle)
    buenos.append(mlc)

print(f'Se encontraron {len(buenos)} anuncios buenos para incluir en la cuenta {cuenta_meli}')

df_resultados = candidatos[candidatos['Número de publicación'].isin(buenos)]

df_detalles = pd.DataFrame(detalles)
df_detalles = df_detalles.merge(
    publicaciones[['Número de publicación', 'TipoEnvio']],
    left_on = '# de publicación',
    right_on = 'Número de publicación',
    how = 'left'
)
df_detalles.drop(columns = ['Número de publicación'], inplace = True)

print(f'Finalmente, para la cuenta {cuenta_meli}, se generaron {df_resultados.shape[0]} anuncios buenos a incluir en FULL o PADS, que ademas de cumplir con los critrerios de venta, \n'
      'cumplen con ser publicaciones activas, que no están actualmente en Fulfillment y que no tengan publicidad (PADS).')

output_folder = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/FULL + PADS/Gestión PADS y Brand ADS/{cuenta_meli}/Anuncios a incluir')
output_folder.mkdir(parents = True, exist_ok = True)
output_path = output_folder / f'PUBLICACIONES A INCLUIR {cuenta_meli} {fecha}.xlsx'
df_resultados.to_excel(output_path, index = False)
output_path2 = output_folder / f'DETALLE CANDIDATOS {cuenta_meli} {fecha}.xlsx'
df_detalles.to_excel(output_path2, index = False)