"""
Cruce de reporte de ventas de mercado libre con base de datos entregada por clic repuestos

Por tema de análisis de ventas en paquete, se necesita necesariamente cruzar con el reporte de ventas procesado que fue generado en procesar_bases_formula1_2025.py

RECORDAR CAMBIAR PATHS DEPENDIENDO DEL MES QUE SE QUIERA ADAPTAR
"""

import pandas as pd

clic_dte = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/reporte_ventas_con_clientes AGOSTO 2025 (1).xlsx',
                     dtype = {'Venta ML ID': str, 'Pack ML ID': str, 'Teléfono': str})

clic_dte['Venta ML ID'] = clic_dte['Venta ML ID'].str.strip().str.lstrip("'")
clic_dte['Pack ML ID'] = clic_dte['Pack ML ID'].str.strip().str.lstrip("'")

ventas = pd.read_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/Ventas Agosto 2025 para concurso.xlsx',
                       dtype = {'# de venta': str})

# Primero, dentro de la base de clic repuestos, filtrar las ventas válidas para participación en el concurso.

# Solo ventas de Mercado Libre
clic_dte = clic_dte[clic_dte['Origen'] == 'MercadoLibre Venta']
# El Tipo de Documento debe ser Boleta electrónica
clic_dte = clic_dte[clic_dte['Tipo DTE'] == 'Boleta electrónica']
# El Monto Total debe ser mayor a 19990
clic_dte = clic_dte[clic_dte['Total DTE'] > 19990]
# No participan las ventas de HYUNDAI CHILE
clic_dte = clic_dte[clic_dte['Cuenta ML'] != 'HYUNDAI CHILE']

# Ahora, hacer el cruce entre ambas bases

nombre_a_venta = ventas.set_index('# de venta')['Datos personales o de empresa'].to_dict()
clic_dte['Nombre (base MeLi) Venta ML'] = clic_dte['Venta ML ID'].map(nombre_a_venta)
clic_dte['Nombre (base MeLi) Pack ML'] = clic_dte['Pack ML ID'].map(nombre_a_venta)
clic_dte['Nombre (base MeLi)'] = clic_dte['Nombre (base MeLi) Venta ML'].combine_first(
    clic_dte['Nombre (base MeLi) Pack ML']
)

direccion_a_venta = ventas.set_index('# de venta')['Dirección'].to_dict()
clic_dte['Dirección (base MeLi) Venta ML'] = clic_dte['Venta ML ID'].map(direccion_a_venta)
clic_dte['Dirección (base MeLi) Pack ML'] = clic_dte['Pack ML ID'].map(direccion_a_venta)
clic_dte['Dirección (base MeLi)'] = clic_dte['Dirección (base MeLi) Venta ML'].combine_first(
    clic_dte['Dirección (base MeLi) Pack ML']
)

cedula_a_venta = ventas.set_index('# de venta')['Cédula'].to_dict()
clic_dte['Cédula (base MeLi) Venta ML'] = clic_dte['Venta ML ID'].map(cedula_a_venta)
clic_dte['Cédula (base MeLi) Pack ML'] = clic_dte['Pack ML ID'].map(cedula_a_venta)
clic_dte['Cédula (base MeLi)'] = clic_dte['Cédula (base MeLi) Venta ML'].combine_first(
    clic_dte['Cédula (base MeLi) Pack ML']
)

clic_dte.drop(
    ['Nombre (base MeLi) Venta ML', 'Nombre (base MeLi) Pack ML',
     'Dirección (base MeLi) Venta ML', 'Dirección (base MeLi) Pack ML',
     'Cédula (base MeLi) Venta ML', 'Cédula (base MeLi) Pack ML'],
    axis=1,
    inplace=True
)

clic_dte['Teléfono'] = clic_dte['Teléfono'].replace(['nan', 'NaN'], '').fillna('')

clic_dte.to_excel('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/2025/Concurso Fórmula 1/Ventas para concurso agosto 2025 (clic_dte repuestos).xlsx', index = False)