"""
Contiene la función descuentos, que sirve para aplicar descuentos a los costos de productos
según un rango de fechas y un diccionario de descuentos por importadora.

Pensado especialmente para el paso 9, que se encuentra en /Users/martincarrasco/Desktop/Martín_Carrasco/Testeo Reportes/Análisis márgenes/9.Descuentos/9.Descuentos.py
"""

import pandas as pd

# descuentos_importadoras = {
#     'MA': 0.05,
#     'RX': 0.10,
#     'CR': 0.03,
#     'AL': 0.04,
#     'NC': 0.04
# }

descuentos_importadoras = {} # Se deja vacío cuando no hay un descuento de tipo cyber

def aplicar_descuentos(df, fecha_col, fecha_inicio, fecha_fin, descuentos_dict, activar=True, reglas_extra=None):
    if not activar:
        print("Descuentos no aplicados, devolviendo el DataFrame original.")
        return df

    df = df.copy()
    df[fecha_col] = pd.to_datetime(df[fecha_col])
    en_rango = (df[fecha_col] >= fecha_inicio) & (df[fecha_col] <= fecha_fin)

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

            sku_str = str(sku).strip().upper()
            partes = sku_str.split('-')
            if len(partes) < 1:
                return costo

            prefijo = partes[0]
            descuento = descuentos_dict.get(prefijo, 0)
            return costo * (1 - descuento)

        df[nuevo_col] = df.apply(aplicar_descuento, axis=1)

    if reglas_extra:
        for regla in reglas_extra:
            df = df.apply(regla, axis=1)

    return df


def descuento_sku_prefijo(
    row,
    prefijo="IT-",
    porcentaje=0.15,
    fecha_col="Fecha de venta",
    fecha_inicio=None,
    fecha_fin=None,
    excluir_full=False
):

    if excluir_full:
        forma_entrega = str(row.get("Forma de entrega", "")).strip().lower()
        if "full" in forma_entrega:
            return row

    fecha = pd.to_datetime(row[fecha_col])
    if fecha_inicio is not None and fecha < pd.to_datetime(fecha_inicio):
        return row
    if fecha_fin is not None and fecha > pd.to_datetime(fecha_fin):
        return row

    columnas_sku = [col for col in row.index if col.startswith("SKU_") and col[-1].isdigit()]

    for col_sku in columnas_sku:
        i = col_sku.split('_')[-1]
        col_costo = f"Costo_post_dcto_SKU_{i}"

        if pd.notna(row[col_sku]) and str(row[col_sku]).startswith(prefijo):
            if col_costo in row and pd.notna(row[col_costo]):
                row[col_costo] *= (1 - porcentaje)

    return row
    