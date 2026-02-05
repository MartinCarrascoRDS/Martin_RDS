"""
Paso 3:
Filtrar estados deseados entre todos los estados de las ventas
"""

import pandas as pd
import os
import numpy as np
from pipeline.procesamiento.funciones_para_analisis_margen import extraer_año_desde_fecha

cuenta_meli = input('Indique la cuenta de Mercado Libre a la que corresponde este análisis (ejemplo: BLACKPARTS): ')
fecha = input('Indique la fecha del análisis (ejemplo: JUNIO 2025): ')
año = extraer_año_desde_fecha(fecha)

archivo_venta = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/2.Eliminar_columnas/{año}/{fecha}/{fecha} {cuenta_meli} Paso 2.xlsx'
hoja_venta = 'Sheet1'

df = pd.read_excel(archivo_venta, sheet_name = hoja_venta, dtype = {'# de venta': str, 'No. Paquete': str})

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
    'Etiqueta impresa',
    'Envío demorado',
    'Envío reprogramado',
    'Esperando disponibilidad de stock',
    'Está demorado 5 días',
    'Etiqueta impresa',
    'Listo para recolección',
    'Llega el',
    'Llega entre el',
    'Mediación finalizada. Te dimos el dinero',
    'Para despachar',
    'Para entregar a la colecta',
    'Procesando en la bodega',
    'Te dimos el dinero de la venta y reembolsamos al comprador',
    'Venta concretada',
    'Venta entregada',
    'Venta no entregada. Te dimos el dinero',
    'Ya despachaste el paquete'
)

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/3.Filtrar_estados/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)

# Función obtenida desde paso 1.2
def clasificar_estado(estado):
    if pd.isna(estado):
        return np.nan

    estado_lower = estado.lower()

    for inicio in inicios_estados_deseados:
        if estado.startswith(inicio):
            return 'Venta'
    
    if any(palabra in estado_lower for palabra in ['cancelaste', 'cancelada', 'cancelado', 'cancelar', 'paquete no entregado', 'venta no entregada', 'no entregado']):
        return 'Cancelado'
        
    if any(palabra in estado_lower for palabra in ['devolución', 'devuelto', 'devolvió', 'devolveremos', 'te entregamos el producto', 'cambio', 'reembolsamos']):
        return 'Devolución'
    
    if any(palabra in estado_lower for palabra in ['reclamo', 'venta con solicitud de cambio', 'cambio listo para retirar']):
        return 'Reclamo'
    
    if 'mediación' in estado_lower and not estado.startswith('Mediación finalizada. Te dimos el dinero'):
        return 'Reclamo'
    
    return "Otro"

df['Clasificación Estado'] = df['Estado'].apply(clasificar_estado)
df_ventas = df[df['Clasificación Estado'] == 'Venta']
print(f'Considerando todos los estados posibles, existen {len(df)} registros.')
print(f'Después de filtrar por estados de venta, quedan {len(df_ventas)} registros.')

output_path = f'{output_folder}/{fecha} {cuenta_meli} VENTAS CLASIFICADAS.xlsx'
df.to_excel(output_path, index = False)