"""
Contiene la función descuentos, que sirve para aplicar descuentos a los costos de productos
según un rango de fechas y un diccionario de descuentos por importadora.

Pensado especialmente para el paso 9, que se encuentra en /Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/9.Descuentos/9.Descuentos.py
"""

import pandas as pd

descuentos_importadoras = {
    'MA': 0.05,
    'RX': 0.10,
    'CR': 0.03,
    'AL': 0.04,
    'NC': 0.04
}

def aplicar_descuentos(df, fecha_col, fecha_inicio, fecha_fin, descuentos_dict, activar = True):
    if not activar:
        print("Descuentos no aplicados, devolviendo el DataFrame original.")
        return df
    
    # Asegurarse de que la fecha esté en formato datetime
    df[fecha_col] = pd.to_datetime(df[fecha_col])

    # Verificar si la fila está dentro del rango de fechas
    en_rango = (df[fecha_col] >= fecha_inicio) & (df[fecha_col] <= fecha_fin)

    # Identificar todas las columnas SKU_i y sus costos
    sku_cols = [col for col in df.columns if col.startswith("SKU_") and col[-1].isdigit()]
    costo_cols = [f"Costo_{col}" for col in sku_cols]

    for sku_col, costo_col in zip(sku_cols, costo_cols):
        nuevo_col = f"Costo_post_dcto_{sku_col}"

        def aplicar_descuento(row):
            costo = row[costo_col]
            sku = row[sku_col]
            if pd.isna(costo) or pd.isna(sku):
                return costo
            if not en_rango.loc[row.name]:
                return costo

            # Extraer prefijo de importadora
            sku_str = str(sku).strip().upper()
            partes = sku_str.split('-')
            if len(partes) < 1:
                return costo

            prefijo = partes[0]
            descuento = descuentos_dict.get(prefijo, 0)
            return costo * (1 - descuento)

        df[nuevo_col] = df.apply(aplicar_descuento, axis=1)

    return df