import pandas as pd

data = pd.read_csv('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Interanuales/Ventas procesadas/ventas accesorios-lubricantes-neumaticos-repuestos 2024-2025 (hasta 02-11-2025).csv')

data['SUBARU'] = data['Producto'].str.contains('SUBARU', case = False, na = False)
data['SUBARU'] = data['SUBARU'].replace({True: 'Sí', False: 'No'})

data.to_csv('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Interanuales/Ventas procesadas/Estudio Subaru ventas accesorios-lubricantes-neumaticos-repuestos 2024-2025 (hasta 02-11-2025).csv', index = False)