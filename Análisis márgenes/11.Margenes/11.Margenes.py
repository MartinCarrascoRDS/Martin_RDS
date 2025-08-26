"""
Paso 11:
Calcular los márgenes obtenidos por cada una de las ventas, generando una columna "Utilidad" que representa la diferencia entre el precio de venta y el costo final del producto.
Con esta columna, se genera la columna "Margen" que es el resultado de dividir la utilidad por el precio de venta, y se obtienen los ponderados de cada margen por la utilidad.
Este ejercicio será hecho solo con las utilidades positivas, las utilidades negativas serán eliminadas, pero se generará un archivo con las utilidades negativas para su revisión.
"""

import pandas as pd
import os
import numpy as np

cuenta_meli = input("Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ")
fecha = input("Indique la fecha del análisis (ejemplo: JUNIO 2025): ")
estados = input('¿Filtraste los estados? (True si lo hiciste, False si no): ').strip()
año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS

if estados.lower() == 'true':
    estados_filtrados = True
elif estados.lower() =='false':
    estados_filtrados = False
else:
    raise ValueError('Por favor ingresa un valor válido de estados filtrados (TRUE O FALSE)')

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/{año}/{fecha}/'
os.makedirs(output_folder, exist_ok=True)

def clasificar_precio(valor):
    if 0 <= valor <= 19989:
        return '01 - $0-$19989'
    elif 19990 <= valor <= 79999:
        return '02 - $19990-$79999'
    elif 80000 <= valor <= 149999:
        return '03 - $80000-$149999'
    elif valor >= 150000:
        return '04 - $150000 o más'

if estados_filtrados:
    archivo_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/10.Eliminar_sin_costos/{año}/{fecha}/Paso10_{cuenta_meli}_{fecha}_sin_sku_faltantes.xlsx'
    hoja_ventas = 'Sheet1'

    df = pd.read_excel(archivo_ventas, sheet_name=hoja_ventas, dtype={'# de venta': str})

    df['Rango de precio'] = df['Ingresos por productos (CLP)'].apply(clasificar_precio)

    df['Total costo'] = (
        df["Costo_final_producto"] -
        df["Cargo por venta e impuestos (CLP) Neto"] +
        df["Costo final envío (CLP) Neto"]
    )
    df["Utilidad"] = df["Ingresos por productos (CLP) Neto"] - df["Total costo"]

    df["Margen"] = df["Utilidad"] / df["Ingresos por productos (CLP) Neto"]

    df["Estrategia Princing"] = np.where(df['SKU_MAYUSC'].str.contains('XX', na=False), 'Killer', 'Normal')

    df_negativos = df[df["Utilidad"] < 0].copy()
    print(f"Hay {df_negativos.shape[0]} registros con utilidades negativas.")
    df_positivos = df[df["Utilidad"] >= 0].copy()
    print(f"Hay {df_positivos.shape[0]} registros con utilidades positivas.")

    utilidad_total = df["Utilidad"].sum()
    df["Ponderado"] = df["Utilidad"] / utilidad_total
    df["Margen x Ponderado"] = df["Margen"] * df["Ponderado"]

    utilidad_positiva_total = df_positivos["Utilidad"].sum()
    df_positivos["Ponderado"] = df_positivos["Utilidad"] / utilidad_positiva_total
    df_positivos["Margen x Ponderado"] = df_positivos["Margen"] * df_positivos["Ponderado"]

    utilidad_negativa_total = df_negativos["Utilidad"].sum()
    df_negativos["Ponderado"] = df_negativos["Utilidad"] / utilidad_negativa_total
    df_negativos["Margen x Ponderado"] = df_negativos["Margen"] * df_negativos["Ponderado"]

    # df["Cuenta Meli"] = cuenta_meli
    # df_positivos["Cuenta Meli"] = cuenta_meli
    # df_negativos["Cuenta Meli"] = cuenta_meli

    sku_cols = [col for col in df.columns if col.startswith("SKU_") and col[-1].isdigit()]
    df["Cantidad SKUs"] = df[sku_cols].notna().sum(axis=1)
    df_positivos["Cantidad SKUs"] = df_positivos[sku_cols].notna().sum(axis=1)
    df_negativos["Cantidad SKUs"] = df_negativos[sku_cols].notna().sum(axis=1)

    output_path = f'{output_folder}MÁRGENES {cuenta_meli} {fecha}.xlsx'
    df.to_excel(output_path, index=False)
    output_path_negativos = f'{output_folder}MÁRGENES {cuenta_meli} {fecha} - Utilidades negativas.xlsx'
    df_negativos.to_excel(output_path_negativos, index=False)
    output_path_positivos = f'{output_folder}MÁRGENES {cuenta_meli} {fecha} - Utilidades positivas.xlsx'
    df_positivos.to_excel(output_path_positivos, index=False)

    print(f"Entre las utilidades totales, se obtuvo un margen promedio simple de: {df['Margen'].mean() * 100:.2f}%")
    print(f"Entre las utilidades totales, se obtuvo un margen ponderado total de: {df['Margen x Ponderado'].sum() * 100:.2f}%")

    print(f"Entre las utilidades positivas, se obtuvo un margen promedio simple de: {df_positivos['Margen'].mean() * 100:.2f}%")
    print(f"Entre las utilidades positivas, se obtuvo un margen ponderado total de: {df_positivos['Margen x Ponderado'].sum() * 100:.2f}%")



else:
    archivo_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/10.Eliminar_sin_costos/{año}/{fecha}/Paso10_{cuenta_meli}_{fecha}_sin_sku_faltantes_ESF.xlsx'
    hoja_ventas = 'Sheet1'

    df = pd.read_excel(archivo_ventas, sheet_name=hoja_ventas, dtype={'# de venta': str})

    df['Rango de precio'] = df['Ingresos por productos (CLP)'].apply(clasificar_precio)

    df['Total costo'] = (
        df["Costo_final_producto"] -
        df["Cargo por venta e impuestos (CLP) Neto"] +
        df["Costo final envío (CLP) Neto"]
    )
    df["Utilidad"] = df["Ingresos por productos (CLP) Neto"] - df["Total costo"]

    df["Margen"] = df["Utilidad"] / df["Ingresos por productos (CLP) Neto"]

    df["Estrategia Princing"] = np.where(df['SKU_MAYUSC'].str.contains('XX', na=False), 'Killer', 'Normal')

    df_negativos = df[df["Utilidad"] < 0].copy()
    print(f"Hay {df_negativos.shape[0]} registros con utilidades negativas.")
    df_positivos = df[df["Utilidad"] >= 0].copy()
    print(f"Hay {df_positivos.shape[0]} registros con utilidades positivas.")

    utilidad_total = df["Utilidad"].sum()
    df["Ponderado"] = df["Utilidad"] / utilidad_total
    df["Margen x Ponderado"] = df["Margen"] * df["Ponderado"]

    utilidad_positiva_total = df_positivos["Utilidad"].sum()
    df_positivos["Ponderado"] = df_positivos["Utilidad"] / utilidad_positiva_total
    df_positivos["Margen x Ponderado"] = df_positivos["Margen"] * df_positivos["Ponderado"]

    utilidad_negativa_total = df_negativos["Utilidad"].sum()
    df_negativos["Ponderado"] = df_negativos["Utilidad"] / utilidad_negativa_total
    df_negativos["Margen x Ponderado"] = df_negativos["Margen"] * df_negativos["Ponderado"]

    # df["Cuenta Meli"] = cuenta_meli
    # df_positivos["Cuenta Meli"] = cuenta_meli
    # df_negativos["Cuenta Meli"] = cuenta_meli

    sku_cols = [col for col in df.columns if col.startswith("SKU_") and col[-1].isdigit()]
    df["Cantidad SKUs"] = df[sku_cols].notna().sum(axis=1)
    df_positivos["Cantidad SKUs"] = df_positivos[sku_cols].notna().sum(axis=1)
    df_negativos["Cantidad SKUs"] = df_negativos[sku_cols].notna().sum(axis=1)

    output_path = f'{output_folder}MÁRGENES {cuenta_meli} {fecha} - ESF.xlsx'
    df.to_excel(output_path, index=False)
    output_path_negativos = f'{output_folder}MÁRGENES {cuenta_meli} {fecha} - Utilidades negativas - ESF.xlsx'
    df_negativos.to_excel(output_path_negativos, index=False)
    output_path_positivos = f'{output_folder}MÁRGENES {cuenta_meli} {fecha} - Utilidades positivas - ESF.xlsx'
    df_positivos.to_excel(output_path_positivos, index=False)

    print(f"Entre las utilidades totales, considerando todos los estados, se obtuvo un margen promedio simple de: {df['Margen'].mean() * 100:.2f}%")
    print(f"Entre las utilidades totales, considerando todos los estados, se obtuvo un margen ponderado total de: {df['Margen x Ponderado'].sum() * 100:.2f}%")

    print(f"Entre las utilidades positivas, considerando todos los estados, se obtuvo un margen promedio simple de: {df_positivos['Margen'].mean() * 100:.2f}%")
    print(f"Entre las utilidades positivas, considerando todos los estados, se obtuvo un margen ponderado total de: {df_positivos['Margen x Ponderado'].sum() * 100:.2f}%")

