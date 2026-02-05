"""
Paso 4:
Forzar formato fecha en columna Fecha de venta
Forzar formato numérico en columnas numéricas
"""

import pandas as pd
from pipeline.procesamiento.funciones_para_analisis_margen import extraer_año_desde_fecha

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = extraer_año_desde_fecha(fecha)

archivo_venta = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/{año}/{fecha}/{fecha} {cuenta_meli} VENTAS CLASIFICADAS.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, hoja_venta, dtype = {'# de venta': str, 'No. Proveedor': str})
    
df = df[df['SKU'].notna() & df['Cargo por venta e impuestos (CLP)'].notna() & df['Ingresos por productos (CLP)'].notna()]

columnas_numericas = [
    'Unidades', 'Ingresos por productos (CLP)', 'Cargo por venta e impuestos (CLP)',
    'Ingresos por envío (CLP)', 'Costos de envío (CLP)'
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors = 'coerce')
    if col in ['Ingresos por envío (CLP)', 'Costos de envío (CLP)']:
        df[col] = df[col].fillna(0)
    if col in ['Ingresos por productos (CLP)', 'Cargo por venta e impuestos (CLP)',
               'Ingresos por envío (CLP)', 'Costos de envío (CLP)']:
        df[f"{col} Neto"] = df[col] / 1.19

df['Costo Flex'] = 0

costo_flex_neto = 3500 / 1.19
mask_flex_unitaria = (
    (df['Forma de entrega'] == 'Mercado Envíos Flex') &
    (df['Tipo de venta'] == 'Unitaria')
)
df.loc[mask_flex_unitaria, 'Costo Flex'] = costo_flex_neto

mask_flex_paquete = (
    (df['Forma de entrega'] == 'Mercado Envíos Flex') &
    (df['Tipo de venta'] == 'Paquete') &
    (df['No. Paquete'].notna())
)

for paquete_id, grupo in df[mask_flex_paquete].groupby('No. Paquete'):
    ingresos = grupo['Ingresos por productos (CLP) Neto']
    total_ingresos = ingresos.sum()

    df.loc[grupo.index, 'Costo Flex'] = ingresos / total_ingresos * costo_flex_neto

# df['Costo final envío (CLP) Neto'] = df.apply(
#     lambda row: row['Costo Flex'] - row['Ingresos por envío (CLP) Neto']
#     if row['Forma de entrega'] == 'Mercado Envíos Flex'
#     else - (row['Costos de envío (CLP) Neto'] + row['Ingresos por envío (CLP) Neto']),
#     axis=1
# )

df['Costo final envío (CLP) Neto'] = df.apply(
    lambda row:
        # Caso 1: Flex
        row['Costo Flex'] - row['Ingresos por envío (CLP) Neto']
        if row['Forma de entrega'] == 'Mercado Envíos Flex'
        else (
            # Caso 2: No Flex y venta < 19990
            0
            if row['Ingresos por productos (CLP)'] < 19990
            else
            # Caso 3: No Flex y venta >= 19990
            -(row['Costos de envío (CLP) Neto'] + row['Ingresos por envío (CLP) Neto'])
        ),
    axis=1
)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/4.Forzar_formatos/Paso4_listo.xlsx'

df.to_excel(output_path, index = False)