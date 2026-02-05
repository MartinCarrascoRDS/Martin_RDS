"""
En este archivo se unirán los archivos que contienen VENTAS TOTALES, VENTAS, VENTAS ESF y MÁRGENES
para la generación de los archivos necesarios para los archivos de Power BI de cierre de mes.
"""

import pandas as pd
import numpy as np
from pathlib import Path

cuentas = ['AUTOSOL', 'BICISOL', 'BLACKPARTS', 'HYUNDAI', 'INDUSOL', 'MERCADOREPUESTOS', 'RDS1', 'RDS3', 'REICARS', 'TRIANA', 'TYC']
fechas1 = ['ENERO 2025', 'FEBRERO 2025', 'MARZO 2025', 'ABRIL 2025', 'MAYO 2025', 'JUNIO 2025',
           'JULIO 2025', 'AGOSTO 2025', 'SEPTIEMBRE 2025 (HASTA 07-09)', 'SEPTIEMBRE 2025 (0830)', 'OCTUBRE 2025', 'NOVIEMBRE 2025', 'DICIEMBRE 2025',
           'ENERO 2026']
fechas2 = ['JUNIO 2025', 'JULIO 2025', 'AGOSTO 2025', 'SEPTIEMBRE 2025 (HASTA 07-09)', 'SEPTIEMBRE 2025 (0830)', 'OCTUBRE 2025', 'NOVIEMBRE 2025', 'DICIEMBRE 2025',
           'ENERO 2026']

path_categorias = Path(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2026/Cuentas RDS/CATEGORÍAS PARA CRUCE/MLC Cat y Sub Cat {fechas1[-1]}.csv')
categorias = pd.read_csv(path_categorias, dtype = {"ITE_ITEM_ID": str})
categorias['ITE_ITEM_ID'] = 'MLC' + categorias['ITE_ITEM_ID'].astype(str)
mlc_a_categoria = categorias.set_index('ITE_ITEM_ID')['DOM_DOMAIN_AGG3'].to_dict()
mlc_a_subcategoria = categorias.set_index('ITE_ITEM_ID')['ITE_DOMAIN_ID'].to_dict()

# VENTAS ESF
path_vesf = Path('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/5.Limpieza_sku')

archivos_validos_vesf = []

for year_folder in path_vesf.iterdir():
    if year_folder.is_dir() and year_folder.name.isdigit() and int(year_folder.name) >= 2025:
        año = year_folder.name
        print(f'Procesando año {año}...')

        for month_folder in year_folder.iterdir():
            if month_folder.is_dir() and month_folder.name in fechas1:
                fecha = month_folder.name
                print(f'Procesando mes {fecha}...')

                for file in month_folder.iterdir():
                    nombre = file.name.upper()
                    if not nombre.endswith('VENTAS.XLSX'):
                        continue
                    if not any(cuenta_meli.upper() in nombre for cuenta_meli in cuentas):
                        continue
                    if ' - ' in nombre:
                        continue
                    print(f'Leyendo archivo {file}')

                    try:
                        df = pd.read_excel(file, dtype = {'# de venta': str, '# de publicación': str})
                        columnas_eliminar = ['Ingresos por productos (CLP)', 'Cargo por venta e impuestos (CLP)', 'Ingresos por envío (CLP)',
                             'Costos de envío (CLP)', 'Canal de venta', 'Ingresos por envío (CLP) Neto', 'Costos de envío (CLP) Neto',
                             'Tienda Oficial', 'Costo Flex']
                        for col in columnas_eliminar:
                            if col in df.columns:
                                df.drop(columns = col, inplace = True)
                        archivos_validos_vesf.append(df)
                    except Exception as e:
                        print(f'Error al leer {file}: {e}')

if archivos_validos_vesf:
    df_final_vesf = pd.concat(archivos_validos_vesf, ignore_index = True)

    df_final_vesf['Categoría'] = df_final_vesf['# de publicación'].map(mlc_a_categoria)
    df_final_vesf['Subcategoría'] = df_final_vesf['# de publicación'].map(mlc_a_subcategoria)

    fecha_inicio = fechas1[0]
    fecha_fin = fechas1[-1]
    output_dir = path_vesf / 'Multimes'
    output_dir.mkdir(parents = True, exist_ok = True)
    output_path = output_dir / f'{fecha_inicio} - {fecha_fin} CONSOLIDADO VENTAS TOTALES.xlsx'

    df_final_vesf.to_excel(output_path, index = False)
    print(f'Dataframe consolidado guardado en {output_path}')
else:
    print('No se encontraron archivos válidos de VENTAS para procesar.')

# MÁRGENES
path_m = Path('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes')

archivos_validos_m =[]

for year_folder in path_m.iterdir():
    if year_folder.is_dir() and year_folder.name.isdigit() and int(year_folder.name) >= 2025:
        año = year_folder.name
        print(f'Procesando año {año}...')

        for month_folder in year_folder.iterdir():
            if month_folder.is_dir() and month_folder.name in fechas2:
                mes = month_folder.name
                print(f'Procesando mes {mes}...')

                for file in month_folder.iterdir():
                    nombre = file.name.upper()

                    if not nombre.endswith('XLSX'):
                        continue

                    if 'MÁRGENES' not in nombre:
                        continue

                    if not any(cuenta_meli.upper() in nombre for cuenta_meli in cuentas):
                        continue

                    if 'Utilidades' in file.name:
                        continue

                    if mes == 'JULIO 2025':
                        if 'ESF' not in nombre:
                            continue

                    print(f'Leyendo archivo {file}')
                    try:
                        df = pd.read_excel(file, dtype = {'# de venta': str, '# de publicación': str})
                        columnas_eliminar1 = [col for col in df.columns if (
                            (col.startswith('SKU_') or
                            col.startswith('Costo_SKU_') or
                            col.startswith('Costo_full_SKU_') or
                            col.startswith('Costo_post_dcto_SKU_'))
                            and col[-1].isdigit()
                        )]
                        for col in columnas_eliminar1:
                            if col in df.columns:
                                df.drop(columns = col, inplace = True)
                        columnas_eliminar2 = ['Ingresos por productos (CLP)', 'Cargo por venta e impuestos (CLP)', 'Ingresos por envío (CLP)', 'Costos de envío (CLP)',
                            'Canal de venta', 'Ingresos por envío (CLP) Neto', 'Costos de envío (CLP) Neto', 'Costo Flex', 'SKU_faltante',
                            'Margen x Ponderado', 'Ponderado', 'Tienda Oficial', 'Cantidad SKUs', 'Tipo de venta', 'No. Paquete', 'Costo_full', 'Depósito',
                            'Estrategia Princing', 'Estrategia Pricing', 'Clasificación Estado']
                        for col in columnas_eliminar2:
                            if col in df.columns:
                                df.drop(columns = col, inplace = True)
                        archivos_validos_m.append(df)
                    except Exception as e:
                        print(f'Error al leer {file}: {e}')

if archivos_validos_m:
    df_final_m = pd.concat(archivos_validos_m, ignore_index = True)

    condiciones_estrategias = [
        df_final_m['SKU_MAYUSC'].str.contains('XX- ', na = False),
        df_final_m['SKU_MAYUSC'].str.contains('Z- ', na = False)
    ]

    estrategias = [
        'Killer',
        'Liquidación'
    ]

    df_final_m["Estrategia Pricing"] = np.select(condiciones_estrategias, estrategias, default = 'Normal')

    df_final_m['Categoría'] = df_final_m['# de publicación'].map(mlc_a_categoria)
    df_final_m['Subcategoría'] = df_final_m['# de publicación'].map(mlc_a_subcategoria)

    fecha_inicio = fechas2[0]
    fecha_fin = fechas2[-1]
    output_dir = path_m / 'Multimes'
    output_dir.mkdir(parents = True, exist_ok = True)
    output_path = output_dir / f'{fecha_inicio} - {fecha_fin} CONSOLIDADO MÁRGENES.xlsx'

    df_final_m.to_excel(output_path, index = False)
    print(f'Dataframe consolidado guardado en {output_path}')
else:
    print('No se encontraron archivos válidos de MÁRGENES para procesar.')