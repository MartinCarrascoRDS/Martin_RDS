"""
UNIÓN DE TODOS LOS INFORMES DE VENTAS ACUMULADOS
"""

import pandas as pd
import numpy as np
import os

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
año_actual = pd.to_datetime(fecha).year
año_anterior = pd.to_datetime(fecha_anterior).year

# Rutas
path_autosol = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/AUTOSOL/VENTAS ACUMULADAS AUTOSOL {fecha}.xlsx'
path_ferre = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/FERRE/VENTAS ACUMULADAS FERRE {fecha}.xlsx'
path_meli_peru = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU/VENTAS ACUMULADAS MELI PERU {fecha}.xlsx'
path_rds = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/RDS/VENTAS ACUMULADAS RDS {fecha}.xlsx'
path_venta_empresa = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA EMPRESA/VENTAS ACUMULADAS VENTA EMPRESA {fecha}.xlsx'
path_venta_interna = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA INTERNA/VENTAS ACUMULADAS VENTA INTERNA {fecha}.xlsx'
path_ventas_digitales = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS DIGITALES/VENTAS ACUMULADAS VENTAS DIGITALES {fecha}.xlsx'
path_ventas_ripley = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS RIPLEY/VENTAS ACUMULADAS VENTAS RIPLEY {fecha}.xlsx'
path_ventas_showroom = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS SHOWROOM/VENTAS ACUMULADAS VENTAS SHOWROOM {fecha}.xlsx'
path_walmart = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/WALMART/VENTAS ACUMULADAS WALMART {fecha}.xlsx'
path_kia_pompeyo = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/KIA Y POMPEYO/VENTAS ACUMULADAS KIA Y POMPEYO {fecha}.xlsx'
path_shopify = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS SHOPIFY/VENTAS ACUMULADAS VENTAS SHOPIFY {fecha}.xlsx'
path_autosol_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/AUTOSOL/VENTAS ACUMULADAS AUTOSOL {fecha_anterior}.xlsx'
path_ferre_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/FERRE/VENTAS ACUMULADAS FERRE {fecha_anterior}.xlsx'
path_meli_peru_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU/VENTAS ACUMULADAS MELI PERU {fecha_anterior}.xlsx'
path_rds_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/RDS/VENTAS ACUMULADAS RDS {fecha_anterior}.xlsx'
path_venta_empresa_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA EMPRESA/VENTAS ACUMULADAS VENTA EMPRESA {fecha_anterior}.xlsx'
path_venta_interna_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA INTERNA/VENTAS ACUMULADAS VENTA INTERNA {fecha_anterior}.xlsx'
path_ventas_digitales_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS DIGITALES/VENTAS ACUMULADAS VENTAS DIGITALES {fecha_anterior}.xlsx'
path_ventas_ripley_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS RIPLEY/VENTAS ACUMULADAS VENTAS RIPLEY {fecha_anterior}.xlsx'
path_ventas_showroom_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS SHOWROOM/VENTAS ACUMULADAS VENTAS SHOWROOM {fecha_anterior}.xlsx'
path_walmart_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/WALMART/VENTAS ACUMULADAS WALMART {fecha_anterior}.xlsx'
path_kia_pompeyo_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/KIA Y POMPEYO/VENTAS ACUMULADAS KIA Y POMPEYO {fecha_anterior}.xlsx'
path_shopify_ly = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS SHOPIFY/VENTAS ACUMULADAS VENTAS SHOPIFY {fecha_anterior}.xlsx'

paths = {
    "AUTOSOL": path_autosol,
    "FERRE": path_ferre,
    "MELI PERU": path_meli_peru,
    "RDS": path_rds,
    "VENTA EMPRESA": path_venta_empresa,
    "VENTA INTERNA": path_venta_interna,
    "VENTAS DIGITALES": path_ventas_digitales,
    "VENTAS RIPLEY": path_ventas_ripley,
    "VENTAS SHOWROOM": path_ventas_showroom,
    "WALMART": path_walmart,
    "KIA Y POMPEYO": path_kia_pompeyo,
    "SHOPIFY": path_shopify,
    "AUTOSOL LY": path_autosol_ly,
    "FERRE LY": path_ferre_ly,
    "MELI PERU LY": path_meli_peru_ly,
    "RDS LY": path_rds_ly,
    "VENTA EMPRESA LY": path_venta_empresa_ly,
    "VENTA INTERNA LY": path_venta_interna_ly,
    "VENTAS DIGITALES LY": path_ventas_digitales_ly,
    "VENTAS RIPLEY LY": path_ventas_ripley_ly,
    "VENTAS SHOWROOM LY": path_ventas_showroom_ly,
    "WALMART LY": path_walmart_ly,
    "KIA Y POMPEYO LY": path_kia_pompeyo_ly,
    "SHOPIFY_LY": path_shopify_ly
}

dfs = []

for nombre, path in paths.items():
    if os.path.exists(path):
        df = pd.read_excel(path)
        dfs.append(df)
        print(f"Se ha leído el archivo de {nombre}, que posee {len(df)} filas")
    else:
        print(f"No se encontró el archivo de {nombre} en la ruta especificada.")

if dfs:
    df_final = pd.concat(dfs, ignore_index = True)
    df_final = df_final.sort_values(by = "FECHA", ascending = True).reset_index(drop = True)

    condiciones = [
        df_final["ORIGEN"].isin(["FERREMAQ", "SANTA ELBA", "COCO"]),
        df_final["ORIGEN"].isin(["RDS1", "RDS3", "TRIANA", "REICARS", "TYC",
                                 "MERCADOREPUESTOS", "BLACKPARTS", "BICISOL", 
                                 "INDUSOL", "HYUNDAI", "MAHINDRA", "AUTOSOL", "IMPACSOL"]),
        df_final["ORIGEN"].isin(["RDS DIGITAL", "FERRESOL DIGITAL"]),
        df_final["ORIGEN"].isin(["RDS SHOWROOM", "FERRESOL SHOWROOM"]),
        df_final["ORIGEN"] == "RIPLEY",
        df_final["ORIGEN"].isin(["WALMART", "WALMART NEUMA"]),
        df_final["ORIGEN"] == "MELI PERU",
        df_final["ORIGEN"] == "SERVITECA",
        df_final["ORIGEN"].isin(["RDS INTERNA", "FERRESOL INTERNA"]),
        df_final["ORIGEN"].isin(["RDS EMPRESA", "FERRESOL EMPRESA"]),
        df_final["ORIGEN"] == "KIA",
        df_final["ORIGEN"] == "POMPEYO",
        df_final["ORIGEN"].isin(["RDS SHOPIFY", "FERRESOL SHOPIFY"])
    ]

    resultados = [
        "MELI FERRE",
        "MELI RDS",
        "DIGITAL",
        "SHOWROOM",
        "VENTAS RIPLEY",
        "VENTAS WALMART",
        "MELI PERU",
        "VENTAS SERVITECA",
        "VENTAS INTERNA",
        "VENTAS EMPRESA",
        "VENTAS KIA",
        "VENTAS POMPEYO",
        "VENTAS SHOPIFY"
    ]

    df_final["SUBGRUPO"] = np.select(condiciones, resultados, default="OTROS")

    condiciones2 = [
        df_final["SUBGRUPO"].isin(["MELI FERRE", "MELI RDS", "MELI PERU"]),
        df_final["SUBGRUPO"] == "DIGITAL",
        df_final["SUBGRUPO"] == "SHOWROOM",
        df_final["SUBGRUPO"].isin(["VENTAS RIPLEY", "VENTAS WALMART"]),
        df_final["SUBGRUPO"] == "VENTAS SERVITECA",
        df_final["SUBGRUPO"] == "VENTAS INTERNA",
        df_final["SUBGRUPO"] == "VENTAS EMPRESA",
        df_final["SUBGRUPO"] == "VENTAS KIA",
        df_final["SUBGRUPO"] == "VENTAS POMPEYO",
        df_final["SUBGRUPO"] == "VENTAS SHOPIFY"
    ]

    resultados2 = [
        "MERCADO LIBRE",
        "DIGITAL",
        "SHOWROOM",
        "RETAIL",
        "SERVITECA",
        "VENTA INTERNA",
        "VENTA EMPRESA",
        "VENTA KIA",
        "VENTA POMPEYO",
        "VENTA SHOPIFY"
    ]

    df_final["GRUPO"] = np.select(condiciones2, resultados2, default="OTROS")

    condiciones3 = [
        df_final["ORIGEN"].isin(["FERREMAQ", "SANTA ELBA", "COCO",
                                 "FERRESOL DIGITAL", "FERRESOL SHOWROOM",
                                 "FERRESOL INTERNA", "FERRESOL EMPRESA", "FERRESOL SHOPIFY"]),
        df_final["ORIGEN"].isin(["RDS1", "RDS3", "TRIANA", "REICARS", "TYC",
                                 "MERCADOREPUESTOS", "BLACKPARTS", "BICISOL", 
                                 "INDUSOL", "HYUNDAI", "MAHINDRA", "AUTOSOL", "IMPACSOL",
                                 "RDS DIGITAL", "RDS SHOWROOM", "RIPLEY", "WALMART",
                                 "WALMART NEUMA", "MELI PERU", "SERVITECA",
                                 "RDS INTERNA", "RDS EMPRESA", "RDS SHOPIFY"]),
        df_final["ORIGEN"].isin(["KIA", "POMPEYO"])
    ]

    resultados3 = [
        "FERRESOL",
        "RDS",
        "KIA - POMPEYO"
    ]

    df_final["RUT"] = np.select(condiciones3, resultados3, default = "OTROS")

    columnas_numericas = [
        'CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES',
        'TICKET PROMEDIO', 'CANTIDAD DE NOTAS DE CRÉDITO', 'MONTO DE NOTAS DE CRÉDITO',
        'VAR % CANTIDAD DE VENTAS', 'VAR% MONTO DE VENTAS', 'VAR% UNIDADES', 'VAR % TICKET PROMEDIO',
        'VISITAS', 'CONVERSIÓN', 'MONTO DE VENTAS (PEN)', 'TICKET PROMEDIO (PEN)'
    ]

    for col in columnas_numericas:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors = 'coerce')

    columnas_rellenar = [
        'CANTIDAD DE VENTAS', 'MONTO DE VENTAS', 'UNIDADES',
        'TICKET PROMEDIO', 'CANTIDAD DE NOTAS DE CRÉDITO', 'MONTO DE NOTAS DE CRÉDITO',
        'VISITAS', 'CONVERSIÓN', 'MONTO DE VENTAS (PEN)', 'TICKET PROMEDIO (PEN)'
    ]

    for col in columnas_rellenar:
        if col in df_final.columns:
            df_final[col] = df_final[col].fillna(0)

    df_final["AÑO COMPARACIÓN"] = f'{año_actual}' # Guía para entender de que año es la comparación (siempre será el año indicado contra el año pasado)

    df_final.to_excel(f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/UNION INFORMES/INFORME VENTAS ACUMULADAS {fecha_anterior} -- {fecha}.xlsx', index = False)
    print(f"Se ha guardado el informe final con {len(df_final)} filas.")

else:
    print("No se encontraron archivos para procesar.")