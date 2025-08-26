"""
UNIÓN DE VENTAS TOTALES JULIO 2025
"""

import pandas as pd
import re

autosol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_AUTOSOL_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
bicisol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_BICISOL_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
blackparts = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_BLACKPARTS_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
indusol = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_INDUSOL_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
mercadorepuestos = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_MERCADOREPUESTOS_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
rds1 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_RDS1_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
rds3 = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_RDS3_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
reicars = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_REICARS_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
triana = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_TRIANA_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})
tyc = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/Paso1.1_TYC_JULIO 2025_listo.xlsx', dtype = {"# de venta": str})

dfs = [autosol, bicisol, blackparts, indusol, mercadorepuestos, rds1, rds3, reicars, triana, tyc]

df_consolidado = pd.concat(dfs, ignore_index = True)

meses_es = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

def convertir_fechas(fecha_str):
    """
    Junto con meses_es, fue directamente obtenida del paso 4.
    """
    if pd.isna(fecha_str):
        return pd.NaT
    try:
        fecha_str = str(fecha_str).lower()
        fecha_str = re.sub(r"\s*hs\.?", "", fecha_str)
        partes = fecha_str.split(' de ')
        if len(partes) < 3:
            return pd.NaT
        dia = partes[0].strip().zfill(2)
        mes = meses_es.get(partes[1].strip(), '01')
        año_hora = partes[2].strip()
        año = año_hora.split()[0]
        return pd.to_datetime(f"{año}/{mes}/{dia}", format="%Y/%m/%d")
    except Exception:
        return pd.NaT
    
if "Fecha de venta" in df_consolidado.columns:
    df_consolidado['Fecha de venta'] = df_consolidado['Fecha de venta'].apply(convertir_fechas)

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/JULIO 2025/VENTAS_TOTALES_CONSOLIDADO_JULIO_2025.xlsx'
df_consolidado.to_excel(output_path, index = False)