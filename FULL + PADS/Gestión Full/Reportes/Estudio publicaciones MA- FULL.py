"""
Comparación de ventas de un conjunto de MLC entre octubre y noviembre 2025
"""

import pandas as pd

path_mlc = '/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión Full/Reportes/listado ventas man.xlsx'
ventas_octubre = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/OCTUBRE 2025/OCTUBRE 2025 CONSOLIDADO VENTAS TOTALES.xlsx'
ventas_noviembre = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/2025/NOVIEMBRE 2025/NOVIEMBRE 2025 CONSOLIDADO VENTAS ESF.xlsx'

mlc = pd.read_excel(path_mlc, sheet_name = 'MA- FULL', dtype = {"PUBLICACIÓN": str, 'MLC': str})
octubre = pd.read_excel(ventas_octubre, sheet_name = 'Sheet1', usecols = ['Fecha de venta', '# de publicación', 'Título de la publicación', 'Forma de entrega', 'Ingresos por venta (CLP) Neto', 'Cuenta Meli'], dtype = {'# de publicación': str})
noviembre = pd.read_excel(ventas_noviembre, sheet_name = 'Sheet1', usecols = ['Fecha de venta', 'Ingresos por productos (CLP)', '# de publicación', 'Título de la publicación', 'Forma de entrega', 'Cuenta Meli'], dtype = {'# de publicación': str})

noviembre['Ingresos por venta (CLP) Neto'] = noviembre['Ingresos por productos (CLP)'] / 1.19

estudio = pd.concat([octubre, noviembre], ignore_index = True)
estudio.drop(columns = ['Ingresos por productos (CLP)'], inplace = True)

estudio = estudio.merge(
    mlc[['MLC']],
    how='left',
    left_on='# de publicación',
    right_on='MLC'
)

estudio['MLC de estudio'] = estudio['MLC'].fillna('MLC no estudiado')

estudio.to_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Gestión Full/Reportes/Estudio Octubre 2025 - Noviembre 2025 MA- FULL.xlsx', index = False)