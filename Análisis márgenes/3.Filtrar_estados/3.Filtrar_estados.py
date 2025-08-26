"""
Paso 3:
Filtrar estados deseados entre todos los estados de las ventas
"""

import pandas as pd
import os

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS
estados = input('¿Quieres filtrar los estados? (True en caso de querer, False en caso de no querer): ').strip()

if estados.lower() == 'true':
    filtrar_estados = True
elif estados.lower() == 'false':
    filtrar_estados = False
else:
    raise ValueError('Por favor ingresa un valor válido para filtrar estados (TRUE O FALSE)')

archivo_venta = '/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/2.Eliminar_columnas/Paso2_listo.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str})

print(f"Existen {len(df)} registros previo a cualquier acción hecha en el paso 3")

df["Cuenta Meli"] = cuenta_meli

inicios_estados_deseados = (
    'Acuerdas la entrega',
    'Despacharemos el paquete',
    'El envío está demorado, pero ya tienes el dinero disponible',
    'En camino',
    'En punto de retiro',
    'Entregado',
    'Etiqueta lista para imprimir',
    'Etiqueta para imprimir',
    'Etiqueta impresa'
    'Envío demorado',
    'Envío reprogramado',
    'Listo para recolección',
    'Llega el',
    'Llega entre el',
    'Mediación finalizada. Te dimos el dinero',
    'Procesando en la bodega',
    'Venta concretada',
    'Venta entregada',
    'Venta no entregada. Te dimos el dinero'
)

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)

if filtrar_estados:
    df = df[df['Estado'].apply(lambda x: any(x.startswith(p) for p in inicios_estados_deseados))].reset_index(drop = True)
    print(f"Se filtraron {len(df)} registros con estados deseados.")
    output_path = f'{output_folder}/Paso3_{cuenta_meli}_{fecha}_listo.xlsx'
else:
    print('No se filtrarán los estados')
    print(f'Existen {len(df)} datos')
    output_path = f'{output_folder}/Paso3_{cuenta_meli}_{fecha}_omitido.xlsx'

df.to_excel(output_path, index = False)