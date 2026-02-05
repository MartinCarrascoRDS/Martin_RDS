"""
Unión de ventas totales de Mercado Libre, luego de pasar por el paso 1 de leer df y eliminar paquetes.
Con fecha personalizable.
"""

import pandas as pd
import os

fecha = input('Indique la fecha de las ventas totales a unir (ejemplo: JUNIO 2025): ')
año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS

# Rutas de los archivos de ventas totales
path_autosol = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_AUTOSOL_{fecha}_listo.xlsx'
path_bicisol = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_BICISOL_{fecha}_listo.xlsx'
path_blackparts = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_BLACKPARTS_{fecha}_listo.xlsx'
path_hyundai = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_HYUNDAI_{fecha}_listo.xlsx'
path_indusol = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_INDUSOL_{fecha}_listo.xlsx'
path_kia = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_KIA_{fecha}_listo.xlsx'
path_mercadorepuestos = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_MERCADOREPUESTOS_{fecha}_listo.xlsx'
path_pompeyo = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_POMPEYO_{fecha}_listo.xlsx'
path_rds1 = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_RDS1_{fecha}_listo.xlsx'
path_rds3 = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_RDS3_{fecha}_listo.xlsx'
path_reicars = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_REICARS_{fecha}_listo.xlsx'
path_triana = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_TRIANA_{fecha}_listo.xlsx'
path_tyc = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/{año}/{fecha}/Paso1_totales_TYC_{fecha}_listo.xlsx'

paths = {
    'AUTOSOL': path_autosol,
    'BICISOL': path_bicisol,
    'BLACKPARTS': path_blackparts,
    'HYUNDAI': path_hyundai,
    'INDUSOL': path_indusol,
    'KIA': path_kia,
    'MERCADOREPUESTOS': path_mercadorepuestos,
    'POMPEYO': path_pompeyo,
    'RDS1': path_rds1,
    'RDS3': path_rds3,
    'REICARS': path_reicars,
    'TRIANA': path_triana,
    'TYC': path_tyc
}

dfs = []

for cuenta, path in paths.items():
    if os.path.exists(path):
        df_temp = pd.read_excel(path, dtype = {'# de venta': str})