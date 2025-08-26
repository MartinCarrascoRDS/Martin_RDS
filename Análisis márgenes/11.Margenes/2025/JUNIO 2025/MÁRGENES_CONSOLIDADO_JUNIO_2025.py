"""
UNIÓN DE ARCHIVOS DE MÁRGENES JUNIO 2025
"""

import pandas as pd

bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES BICISOL JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES BLACKPARTS JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES INDUSOL JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES MERCADOREPUESTOS JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES RDS1 JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES RDS3 JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES REICARS JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES TRIANA JUNIO 2025.xlsx', sheet_name='Sheet1', dtype={'# de venta': str})

def eliminar_columnas_costo(df):
    """
    Elimina las columnas de costo que no son necesarias para el análisis de márgenes.
    """
    columnas_a_eliminar = [col for col in df.columns if (
        (col.startswith('SKU_') or
        col.startswith('Costo_SKU_') or
        col.startswith('Costo_post_dcto_SKU_'))
        and col[-1].isdigit()
    )]

    if "Costo_full" in df.columns:
        columnas_a_eliminar.append("Costo_full")

    return df.drop(columns=columnas_a_eliminar, errors='ignore')

dfs = [bicisol, blackparts, indusol, mercadorepuestos, rds1, rds3, reicars, triana]
dfs_limpios = [eliminar_columnas_costo(df) for df in dfs]
df_consolidado = pd.concat(dfs_limpios, ignore_index=True)
output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JUNIO 2025/MÁRGENES_CONSOLIDADO_JUNIO_2025.xlsx'
df_consolidado.to_excel(output_path, index=False)