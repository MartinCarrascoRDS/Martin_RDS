"""
Paso 2:
Eliminar las columnas indeseadas del dataframe
Asegurarse de que no hayan espacios innecesarios antes o después de la columna Estado
"""

import pandas as pd

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/Paso1_listo.xlsx'
hoja_venta = 'Sheet1'
df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str})

columnas_unicas = []
contador_estado = 0
contador_unidades = 0
contador_forma_entrega = 0
columnas_eliminar = [
        "Descripción del estado", "Paquete de varios productos", "Pertenece a un kit",
        "Anulaciones y reembolsos (CLP)", "Total (CLP)",
        "Precio unitario de venta de la publicación (CLP)",
        "Mes de facturación de tus cargos", "Venta por publicidad",
        "Canal de venta", "Tienda oficial", "Variante", "Tipo de publicación", "Factura adjunta",
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

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/2.Eliminar_columnas/Paso2_listo.xlsx'
df.to_excel(output_path, index = False)