"""
UNIÓN DE ARCHIVOS DE MÁRGENES RDS1 E INDUSOL PARA ANÁLISIS AUTOMARCO, AUTOTEC Y GABTEC JULIO 2025 (HASTA 24-07)
"""

import pandas as pd

indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JULIO 2025 (HASTA 24-07)/MÁRGENES INDUSOL JULIO 2025 (HASTA 24-07).xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JULIO 2025 (HASTA 24-07)/MÁRGENES RDS1 JULIO 2025 (HASTA 24-07).xlsx', dtype = {"# de venta": str})

def eliminar_columnas(df):
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

    if "Margen x Ponderado" in df.columns:
        columnas_a_eliminar.append("Margen x Ponderado")

    if "Ponderado" in df.columns:
        columnas_a_eliminar.append("Ponderado")

    return df.drop(columns=columnas_a_eliminar, errors='ignore')

dfs = [indusol, rds1]
dfs_limpios = [eliminar_columnas(df) for df in dfs]
df_consolidado = pd.concat(dfs_limpios, ignore_index = True)
output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/JULIO 2025 (HASTA 24-07)/MÁRGENES_INDUSOL_RDS1_JULIO_2025_HASTA_24.xlsx'
df_consolidado.to_excel(output_path, index = False)