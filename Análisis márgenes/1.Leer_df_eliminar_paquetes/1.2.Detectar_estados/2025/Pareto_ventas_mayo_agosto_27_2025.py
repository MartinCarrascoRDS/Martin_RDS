"""
80/20 DE LAS VENTAS POR CUENTA ENTRE MAYO Y AGOSTO (HASTA EL 27) DEL 2025
"""

import pandas as pd

archivo_entrada = "/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/Ventas 20250501 - 20252708.xlsx"
archivo_salida = "/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/2025/Pareto ventas 20250501 - 20252708.xlsx"
col_monto = "Ingresos por venta (CLP) Neto"
col_producto = ["# de publicación", "Título de la publicación"]

xls = pd.ExcelFile(archivo_entrada)
hojas = [hoja for hoja in xls.sheet_names if hoja != "CONSOLIDADO"]

pareto_por_cuenta = {}

for hoja in hojas:
    df = pd.read_excel(xls, sheet_name=hoja)

    df_agrup = df.groupby(col_producto, as_index=False)[col_monto].sum()

    df_agrup = df_agrup.sort_values(by=col_monto, ascending=False)

    total = df_agrup[col_monto].sum()
    df_agrup['% sobre total'] = df_agrup[col_monto] / total
    df_agrup['% acumulado'] = df_agrup['% sobre total'].cumsum()
    df_agrup['Pareto_80'] = df_agrup['% acumulado'] <= 80

    pareto_por_cuenta[hoja] = df_agrup

with pd.ExcelWriter(archivo_salida) as writer:
    for cuenta, df_result in pareto_por_cuenta.items():
        df_result.to_excel(writer, sheet_name=cuenta, index=False)

print(f"Análisis de Pareto por dinero generado en: {archivo_salida}")