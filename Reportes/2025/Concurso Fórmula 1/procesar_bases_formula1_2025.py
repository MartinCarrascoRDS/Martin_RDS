"""
PROCESAMIENTO BASES FÓRMULA 1 2025

Script para procesar bases de venta de las cuentas de MeLi.
Objetivo: obtener todos los registros con los estados entregado, venta concretada y venta entregada para ver la información
de las personas que realizaron.

RECORDAR CAMBIAR PATHS DEPENDIENDO DEL MES QUE SE QUIERA ADAPTAR
"""

import pandas as pd
import re

# ================================
# 1. Lectura de archivos
# ================================
autosol = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS AUTOSOL SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)
bicisol = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS BICISOL SEPTIEMBRE 2025.xlsx',
    dtype={'# de venta': str}, skiprows=5
)
blackparts = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS BLACKPARTS SEPTIEMBRE 2025.xlsx',
    dtype={'# de venta': str}, skiprows=5
)
indusol = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS INDUSOL SEPTIEMBRE 2025.xlsx',
    dtype={'# de venta': str}, skiprows=5
)
mercadorepuestos = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS MERCADOREPUESTOS SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)
rds1 = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS RDS1 SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)
rds3 = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS RDS3 SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)
reicars = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS REICARS SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)
triana = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS TRIANA SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)
tyc = pd.read_excel(
    '/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/F1 VENTAS TYC SEPTIEMBRE 2025.xlsx',
    dtype={"# de venta": str}, skiprows=5
)

# ================================
# 2. Guardar en un diccionario
# ================================
dfs = {
    "autosol": autosol,
    "bicisol": bicisol,
    "blackparts": blackparts,
    "indusol": indusol,
    "mercadorepuestos": mercadorepuestos,
    "rds1": rds1,
    "rds3": rds3,
    "reicars": reicars,
    "triana": triana,
    "tyc": tyc
}

# ================================
# 3. Función de filtrado
# ================================
estados_validos = ["Entregado", "Venta concretada", "Venta entregada"]
patron_paquete = re.compile(r"Paquete de (\d+) productos")

def filtrar_df(df):
    filas_a_conservar = []
    i = 0
    while i < len(df):
        estado = str(df.iloc[i]["Estado"])
        
        # Caso 1: estado válido normal
        if estado in estados_validos:
            filas_a_conservar.append(i)
            i += 1
            continue
        
        # Caso 2: paquete
        match = patron_paquete.fullmatch(estado)
        if match:
            x = int(match.group(1))
            if i + x < len(df) and all(
                str(df.iloc[j]["Estado"]) in estados_validos
                for j in range(i + 1, i + 1 + x)
            ):
                filas_a_conservar.append(i)
                filas_a_conservar.extend(range(i + 1, i + 1 + x))
                i += x + 1
                continue
        
        # Caso 3: descartar
        i += 1

    # Filtrar por filas seleccionadas
    df_filtrado = df.iloc[filas_a_conservar]

    # Filtrar ingresos >= 19990
    df_filtrado = df_filtrado[df_filtrado["Ingresos por productos (CLP)"] >= 19990]

    return df_filtrado

# ================================
# 4. Filtrar y agregar columna Cuenta
# ================================
dfs_filtrados = []

for nombre, df in dfs.items():
    df_filtrado = filtrar_df(df).copy()
    df_filtrado["Cuenta"] = nombre
    dfs_filtrados.append(df_filtrado)

# ================================
# 5. Concatenar y exportar
# ================================
df_final = pd.concat(dfs_filtrados, ignore_index=True)
df_final.to_excel("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/Ventas Septiembre 2025 para concurso.xlsx", index=False)