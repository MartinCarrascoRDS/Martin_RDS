"""
Paso 3:
Filtrar estados deseados entre todos los estados de las ventas
"""

import pandas as pd

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/2.Eliminar_columnas/Paso2_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str})

inicios_estados_deseados = (
    'Acuerdas la entrega',
    'Despacharemos el paquete',
    'En camino',
    'En punto de retiro',
    'Entregado',
    'Etiqueta lista para imprimir',
    'Etiqueta para imprimir',
    'Envío reprogramado',
    'Listo para recolección',
    'Mediación finalizada. Te dimos el dinero',
    'Procesando en la bodega',
    'Venta concretada',
    'Venta entregada',
    'Venta no entregada. Te dimos el dinero'
)

df = df[df['Estado'].apply(lambda x: any(x.startswith(p) for p in inicios_estados_deseados))].reset_index(drop = True)

print(f"Se filtraron {len(df)} registros con estados deseados.")

output_path = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/Paso3_listo.xlsx'
df.to_excel(output_path, index = False)