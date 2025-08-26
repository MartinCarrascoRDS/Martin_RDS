"""
Paso 1.2
Crear columna que permita diferenciar entre venta, reclamo, cancelación y devolución
"""

import pandas as pd
import numpy as np
import os

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = 2024 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS

archivo_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.1.Limpieza_sku/{año}/{fecha}/Paso1.1_{cuenta_meli}_{fecha}_listo.xlsx'
hoja_ventas = 'Sheet1'

df = pd.read_excel(archivo_ventas, sheet_name = hoja_ventas, dtype = {"# de venta": str})

inicios_estados_ventas = (
    'Acuerdas la entrega',
    'Despacharemos el paquete',
    'El envío está demorado, pero ya tienes el dinero disponible',
    'En camino',
    'En punto de retiro',
    'Entregado',
    'Etiqueta lista para imprimir',
    'Etiqueta para imprimir',
    'Etiqueta impresa',
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

def clasificar_estado(estado):
    if pd.isna(estado):
        return np.nan

    estado_lower = estado.lower()

    for inicio in inicios_estados_ventas:
        if estado.startswith(inicio):
            return 'Venta'
        
    if any(palabra in estado_lower for palabra in ['devolución', 'devuelto', 'devolvió', 'devolveremos']):
        return 'Devolución'
    
    if any(palabra in estado_lower for palabra in ['reclamo', 'venta con solicitud de cambio']):
        return 'Reclamo'
    
    if 'mediación' in estado_lower and not estado.startswith('Mediación finalizada. Te dimos el dinero'):
        return 'Reclamo'
    
    if 'no entregado' in estado_lower and not estado.startswith('Venta no entregada. Te dimos el dinero'):
        return 'Reclamo'
    
    if any(palabra in estado_lower for palabra in ['cancelaste', 'cancelada', 'cancelado', 'paquete no entregado']):
        return 'Cancelado'
    
    return "Otro"

df['Clasificación Estado'] = df['Estado'].apply(clasificar_estado)

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.2.Detectar_estados/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)
output_path = f'{output_folder}/Paso1.2_{cuenta_meli}_{fecha}_listo.xlsx'
df.to_excel(output_path, index = False)