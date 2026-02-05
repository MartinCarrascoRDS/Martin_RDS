""""
Paso 1: Leer 2 archivos excel (recordar cambiar de csv a excel manualmente), uno de cada quincena del mes, donde se encuentra la información de ventas, y unirlos en un solo dataframe.
Subdividir la información en dataframes de costos de envío, ventas y devoluciones.
Neteo de valores importantes
"""

import pandas as pd
import os

año = 2025 # RECORDAR CAMBIAR EL AÑO PARA GENERAR NUEVAS CARPETAS
cuenta_walmart = input('Indique la cuenta de Walmart a la que corresponde este análisis (WALMART REPUESTOS O WALMART NEUMA): ')
fecha = input('Indique la fecha del análisis (ejemplo: OCTUBRE 2025): ')

direc_walmart1 = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/{año}/Walmart/{cuenta_walmart}/VENTAS {cuenta_walmart} {fecha} (QUINCENA 1).xlsx'
direc_walmart2 = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/{año}/Walmart/{cuenta_walmart}/VENTAS {cuenta_walmart} {fecha} (QUINCENA 2).xlsx'

walmart1 = pd.read_excel(direc_walmart1, dtype = {"SG": str, "Orden": str})
walmart2 = pd.read_excel(direc_walmart2, dtype = {"SG": str, "Orden": str})

walmart = pd.concat([walmart1, walmart2], ignore_index = True)

# Modificaciones df walmart
walmart = walmart[~walmart["SKU"].str.contains("Despacho cliente", na = False)]
walmart = walmart[~walmart["SKU"].str.contains("Descuento", na = False)]
walmart = walmart.drop(columns = ['Rut Seller', 'Nombre Seller', 'N¬∫ Liq.', 'Fecha Inicio Liq.', 'Fecha Fin Liq.'])
print(walmart.columns)

# Subdivisiones
walmart_envio = walmart[walmart['SKU'] == 'Despacho seller'].copy()
walmart_li = walmart[walmart['SKU'] == 'Logistica inversa'].copy()
walmart_ventas = walmart[~walmart['SKU'].isin(['Despacho seller', 'Logistica inversa', 'Descuento'])].copy()

# Neteo valores
walmart_envio['Costo logístico neto'] = walmart_envio['Precio Item'] / 1.19
walmart_li['Monto devolución neto'] = walmart_li['Precio Item'] / 1.19
walmart_ventas['Ingreso por venta neto'] = walmart_ventas['Precio Item'] / 1.19
walmart_ventas['Cargo comisión neto'] = walmart_ventas['Cargo Comision'] / 1.19

# Guardar dataframes
output_folder = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes Walmart/1.Leer_df_y_subdivisiones/{año}/{fecha}'
os.makedirs(output_folder, exist_ok = True)

output_path_envio = f'{output_folder}/{fecha} {cuenta_walmart} COSTOS DE ENVÍO.xlsx'
output_path_devoluciones = f'{output_folder}/{fecha} {cuenta_walmart} LOGÍSTICA INVERSA.xlsx'
output_path_ventas = f'{output_folder}/{fecha} {cuenta_walmart} VENTAS TOTALES.xlsx'
walmart_envio.to_excel(output_path_envio, index = False)
walmart_li.to_excel(output_path_devoluciones, index = False)
walmart_ventas.to_excel(output_path_ventas, index = False)