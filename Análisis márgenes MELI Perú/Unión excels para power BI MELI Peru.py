"""
En este archivo se unirán los archivos que contienen VENTAS TOTALES, VENTAS, VENTAS ESF y MÁRGENES
para la generación de los archivos necesarios para los archivos de Power BI de cierre de mes.
"""

import pandas as pd
from pathlib import Path

cuentas = ['RDS PERU']
fechas = ['SEPTIEMBRE 2025', 'OCTUBRE 2025', 'NOVIEMBRE 2025', 'DICIEMBRE 2025',
          'ENERO 2026']
año = 2025

# VENTAS ESF
path_vesf = Path('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/5.Limpieza_sku')

archivos_validos_vesf = []

for year_folder in path_vesf.iterdir():
    if year_folder.is_dir() and year_folder.name.isdigit() and int(year_folder.name) >= 2025:
        año = year_folder.name
        print(f'Procesando año {año}...')

        for month_folder in year_folder.iterdir():
            if month_folder.is_dir() and month_folder.name in fechas:
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
                        columnas_eliminar = ['Ingresos por productos (PEN)', 'Cargo por venta e impuestos (PEN)', 'Ingresos por envío (PEN)',
                             'Costos de envío (PEN)', 'Canal de venta', 'Ingresos por envío (PEN) Neto', 'Costos de envío (PEN) Neto',
                             'Tienda Oficial', 'Costo Flex']
                        for col in columnas_eliminar:
                            if col in df.columns:
                                df.drop(columns = col, inplace = True)
                        archivos_validos_vesf.append(df)
                    except Exception as e:
                        print(f'Error al leer {file}: {e}')

if archivos_validos_vesf:
    df_final_vesf = pd.concat(archivos_validos_vesf, ignore_index = True)

    fecha_inicio = fechas[0]
    fecha_fin = fechas[-1]
    output_dir = path_vesf / 'Multimes'
    output_dir.mkdir(parents = True, exist_ok = True)
    output_path = output_dir / f'{fecha_inicio} - {fecha_fin} MELI PERÚ VENTAS TOTALES.xlsx'

    df_final_vesf.to_excel(output_path, index = False)
    print(f'Dataframe consolidado guardado en {output_path}')
else:
    print('No se encontraron archivos válidos de VENTAS ESF para procesar.')

# MÁRGENES
path_m = Path('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/11.Margenes')

archivos_validos_m =[]

for year_folder in path_m.iterdir():
    if year_folder.is_dir() and year_folder.name.isdigit() and int(year_folder.name) >= 2025:
        año = year_folder.name
        print(f'Procesando año {año}...')

        for month_folder in year_folder.iterdir():
            if month_folder.is_dir() and month_folder.name in fechas:
                mes = month_folder.name
                print(f'Procesando mes {mes}...')

                for file in month_folder.iterdir():
                    nombre = file.name.upper()

                    if not nombre.endswith('.XLSX'):
                        continue

                    if 'MÁRGENES' not in nombre:
                        continue

                    if not any(cuenta_meli.upper() in nombre for cuenta_meli in cuentas):
                        continue

                    if 'Utilidades' in nombre:
                        continue

                    if ' - ' in file.name:
                        continue

                    print(f'Leyendo archivo {file}')
                    try:
                        df = pd.read_excel(file, dtype = {'# de venta': str, '# de publicación': str})
                        columnas_eliminar1 = columnas_a_eliminar = [col for col in df.columns if (
                            (col.startswith('SKU_') or
                            col.startswith('Costo_SKU_') or
                            col.startswith('Costo_full_SKU_') or
                            col.startswith('Costo_post_dcto_SKU_'))
                            and col[-1].isdigit()
                        )]
                        for col in columnas_eliminar1:
                            if col in df.columns:
                                df.drop(columns = col, inplace = True)
                        columnas_eliminar2 = ['Ingresos por productos (PEN)', 'Cargo por venta e impuestos (PEN)', 'Ingresos por envío (PEN)', 'Costos de envío (PEN)',
                            'Canal de venta', 'Ingresos por envío (PEN) Neto', 'Costos de envío (PEN) Neto', 'Costo Flex', 'SKU_faltante',
                            'Margen x Ponderado', 'Ponderado', 'Tienda Oficial', 'Clasificación Estado', 'Cantidad SKUs', 'Tipo de venta', 'No. Paquete',
                            'Calle', 'DNI', 'Provincia']
                        for col in columnas_eliminar2:
                            if col in df.columns:
                                df.drop(columns = col, inplace = True)
                        archivos_validos_m.append(df)
                    except Exception as e:
                        print(f'Error al leer {file}: {e}')

if archivos_validos_m:
    df_final_m = pd.concat(archivos_validos_m, ignore_index = True)

    fecha_inicio = fechas[0]
    fecha_fin = fechas[-1]
    output_dir = path_m / 'Multimes'
    output_dir.mkdir(parents = True, exist_ok = True)
    output_path = output_dir / f'{fecha_inicio} - {fecha_fin} MELI PERÚ MÁRGENES.xlsx'

    df_final_m.to_excel(output_path, index = False)
    print(f'Dataframe consolidado guardado en {output_path}')
else:
    print('No se encontraron archivos válidos de MÁRGENES para procesar.')