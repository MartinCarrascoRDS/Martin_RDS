"""
Cruce de reporte de ventas de mercado libre con base de datos entregada por clic repuestos

Por tema de análisis de ventas en paquete, se necesita necesariamente cruzar con el reporte de ventas procesado que fue generado en procesar_bases_formula1_2025.py

RECORDAR CAMBIAR PATHS DEPENDIENDO DEL MES QUE SE QUIERA ADAPTAR
"""

import pandas as pd

clic = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/informe-de-ventas AGOSTO.xlsx',
                     dtype = {'N° de Venta de MercadoLibre': str, 'Telefono': str})

clic['N° de Venta de MercadoLibre'] = clic['N° de Venta de MercadoLibre'].str.strip()

ventas = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/Ventas Agosto 2025 para concurso.xlsx',
                       dtype = {'# de venta': str})

# Primero, dentro de la base de clic repuestos, filtrar las ventas válidas para participación en el concurso.

# El Tipo de Documento debe ser Boleta electrónica
clic = clic[clic['Tipo de Documento'] == 'Boleta electrónica']
# El Monto Total debe ser mayor a 19990
clic = clic[clic['Monto Total'] > 19990]
# No participan las ventas de HYUNDAI CHILE
clic = clic[clic['Vendedor'] != 'HYUNDAI CHILE']
# No participan las ventas de Walmart, Walmart Neuma, o ventas internas
clic = clic[(clic['Canal de Venta'] != 'Walmart') & (clic['Canal de Venta'] != 'Wallmart Neuma') & (clic['Canal de Venta'] != 'Venta interna')]

# Ahora, hacer el cruce entre ambas bases

nombre_a_venta = ventas.set_index('# de venta')['Datos personales o de empresa'].to_dict()
clic['Nombre (base MeLi)'] = clic['N° de Venta de MercadoLibre'].map(nombre_a_venta)

direccion_a_venta = ventas.set_index('# de venta')['Dirección'].to_dict()
clic['Dirección (base MeLi)'] = clic['N° de Venta de MercadoLibre'].map(direccion_a_venta)

cedula_a_venta = ventas.set_index('# de venta')['Cédula'].to_dict()
clic['Cédula (base Meli)'] = clic['N° de Venta de MercadoLibre'].map(cedula_a_venta)

clic['Telefono'] = clic['Telefono'].astype(str)
clic['Telefono'] = clic['Telefono'].str.replace('nan', '', regex = False)

clic.to_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/Ventas para concurso agosto 2025 (clic repuestos).xlsx', index = False)