"""
Paso 2:
Eliminar las columnas indeseadas del dataframe
Asegurarse de que no hayan espacios innecesarios antes o después de la columna Estado
"""

import pandas as pd
import os
from pipeline.procesamiento.funciones_para_analisis_margen import extraer_año_desde_fecha

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = extraer_año_desde_fecha(fecha)

archivo_venta = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/1.Leer_df_eliminar_paquetes/{año}/{fecha}/{fecha} {cuenta_meli} TOTAL VENTAS.xlsx'
hoja_venta = 'Sheet1'
df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str, 'No. Paquete': str})

print(f"Registros antes del paso 2: {len(df)}")

columnas_unicas = []
contador_estado = 0
contador_unidades = 0
contador_forma_entrega = 0
columnas_eliminar = [
        "Descripción del estado", "Paquete de varios productos", "Pertenece a un kit",
        "Anulaciones y reembolsos (PEN)", "Total (PEN)",
        "Precio unitario de venta de la publicación (PEN)",
        "Mes de facturación de tus cargos",
        "Tienda oficial", "Variante", "Tipo de publicación", "Factura adjunta",
        "Datos personales o de empresa", "Tipo y número de documento", "Dirección",
        "Tipo de contribuyente", "Actividad económica", "Comprador", "Negocio", "Cédula",
        "Domicilio", "Comuna", "Estado", "Código postal", "País", "Fecha en camino", "Fecha entregado",
        "Transportista", "Número de seguimiento", "URL de seguimiento",
        "Revisado por Mercado Libre", "Fecha de revisión",
        "Dinero a favor", "Resultado", "Destino", "Motivo del resultado",
        "Reclamo abierto", "Reclamo cerrado", "Con mediación"
    ]

for col in df.columns:
    if isinstance(col, str) and col.startswith("Estado"):
        contador_estado += 1
        if contador_estado == 1:
              columnas_unicas.append(col)
    elif isinstance(col, str) and col.startswith("Unidades"):
        contador_unidades += 1
        if contador_unidades == 1:
              columnas_unicas.append(col)
    elif isinstance(col, str) and col.startswith("Forma de entrega"):
        contador_forma_entrega += 1
        if contador_forma_entrega == 1:
            columnas_unicas.append(col)
    elif isinstance(col, str) and all(not col.startswith(nombre_col) for nombre_col in columnas_eliminar):
          columnas_unicas.append(col)

 
df = df[columnas_unicas]
"""
Este código está adaptado para tomar un excel con los encabezados de columna en la primera fila, y eliminar
las columnas indeseadas, las cuales se especifican en columnas_eliminar. Adicionalmente, se implementa
posteriormente unas lineas de código para evitar que se eliminen ciertas columnas que tienen el mismo
nombre que otras que si se desean eliminar, en este caso, Estado, Unidades y Forma de entrega.
"""   

output_path = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/2.Eliminar_columnas/{año}/{fecha}'
os.makedirs(output_path, exist_ok = True)
df.to_excel(f'{output_path}/{fecha} {cuenta_meli} paso 2.xlsx', index = False)