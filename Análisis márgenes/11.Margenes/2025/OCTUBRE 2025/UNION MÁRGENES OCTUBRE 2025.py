"""
UNIÓN DE MÁRGENES CON ESTADOS FILTRADOS
"""

import pandas as pd

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 AUTOSOL MÁRGENES.xlsx', dtype = {'# de venta': str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 BICISOL MÁRGENES.xlsx', dtype = {'# de venta': str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 BLACKPARTS MÁRGENES.xlsx', dtype = {'# de venta': str})
hyundai = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 HYUNDAI MÁRGENES.xlsx', dtype = {'# de venta': str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 INDUSOL MÁRGENES.xlsx', dtype = {'# de venta': str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 MERCADOREPUESTOS MÁRGENES.xlsx', dtype = {'# de venta': str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 RDS1 MÁRGENES.xlsx', dtype = {'# de venta': str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 RDS3 MÁRGENES.xlsx', dtype = {'# de venta': str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 REICARS MÁRGENES.xlsx', dtype = {'# de venta': str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 TRIANA MÁRGENES.xlsx', dtype = {'# de venta': str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 TYC MÁRGENES.xlsx', dtype = {'# de venta': str})

def eliminar_columnas(df):
    """
    Elimina las columnas de costo que no son necesarias para el análisis de márgenes.
    """
    columnas_a_eliminar = [col for col in df.columns if (
        (col.startswith('SKU_') or
        col.startswith('Costo_SKU_') or
        col.startswith('Costo_full_SKU_') or
        col.startswith('Costo_post_dcto_SKU_'))
        and col[-1].isdigit()
    )]

    if "Margen x Ponderado" in df.columns:
        columnas_a_eliminar.append("Margen x Ponderado")

    if "Ponderado" in df.columns:
        columnas_a_eliminar.append("Ponderado")

    return df.drop(columns=columnas_a_eliminar, errors='ignore')

dfs = [autosol, bicisol, blackparts, hyundai, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]
dfs_limpios = [eliminar_columnas(df) for df in dfs]
df_consolidado = pd.concat(dfs_limpios, ignore_index = True)
output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/11.Margenes/2025/OCTUBRE 2025/OCTUBRE 2025 CONSOLIDADO MÁRGENES.xlsx'
df_consolidado.to_excel(output_path, index = False)
