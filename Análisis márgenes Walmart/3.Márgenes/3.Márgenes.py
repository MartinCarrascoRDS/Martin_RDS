"""
Paso 3: Cálculo de márgenes
"""
import pandas as pd
import os

año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS
cuenta_walmart = input('Indique la cuenta de Walmart a la que corresponde este análisis (WALMART REPUESTOS O WALMART NEUMA): ')
fecha = input('Indique la fecha del análisis (ejemplo: OCTUBRE 2025): ')

direc_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes Walmart/2.Cruce_de_costos/{año}/{fecha}/{fecha} {cuenta_walmart} VENTAS SIN DEVOLUCIÓN.xlsx'
ventas = pd.read_excel(direc_ventas, dtype = {'SG': str, 'Orden': str})

def clasificar_precio(valor):
    if 0 <= valor <= 19989:
        return '01 - $0-$19989'
    elif 19990 <= valor <= 79999:
        return '02 - $19999-$79999'
    elif 80000 <= valor <= 149999:
        return '03 - $80000-$149999'
    elif valor >= 150000:
        return '04 - $150000 o más'
    
ventas['Cuenta walmart'] = cuenta_walmart    
ventas['Rango de precio'] = ventas['Precio Item'].apply(clasificar_precio)
ventas['Total costo'] = ventas['Costo SKU neto'] - ventas['Costo logístico neto prorrateado'] - ventas['Cargo comisión neto']
ventas['Utilidad'] = ventas['Ingreso por venta neto'] - ventas['Total costo']
ventas['Margen'] = ventas['Utilidad'] / ventas['Ingreso por venta neto']

ventas_encontrados = ventas[ventas['Costo SKU neto'].notna()]
print(f'De un total de {ventas.shape[0]} productos vendidos, se encontró el costo de {ventas_encontrados.shape[0]}')

ingreso_neto_total = ventas_encontrados['Ingreso por venta neto'].sum()
utilidad_total = ventas_encontrados['Utilidad'].sum()
margen_linea_final = utilidad_total / ingreso_neto_total

print(f'Ingreso total: {ingreso_neto_total:,.0f}')
print(f'Utilidad total: {utilidad_total:,.0f}')
print(f'El margen línea final de {cuenta_walmart} en {fecha} es de {margen_linea_final * 100:.2f}%')

output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes Walmart/3.Márgenes/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)
output_path_ventas = f'{output_folder}/{fecha} {cuenta_walmart} MÁRGENES.xlsx'
output_path_ventas_encontrados = f'{output_folder}/{fecha} {cuenta_walmart} MÁRGENES COSTOS ENCONTRADOS.xlsx'
ventas.to_excel(output_path_ventas, index = False)
ventas_encontrados.to_excel(output_path_ventas_encontrados, index = False)