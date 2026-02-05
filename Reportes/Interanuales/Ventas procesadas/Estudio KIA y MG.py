import pandas as pd
import re

data = pd.read_csv('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Interanuales/Ventas procesadas/ventas accesorios-lubricantes-neumaticos-repuestos 2024-2025 (hasta 02-11-2025).csv')

data['KIA'] = data['Producto'].str.contains('KIA', case = False, na = False)
data['KIA'] = data['KIA'].replace({True: 'Sí', False: 'No'})

patron_mg = r'(?<![A-Za-z0-9])(?:(?<=^)|(?<=[\s\.,;:/\-\(\)\[\]]))mg(?:\s|3|zs|gt|zx|5|hs|one|rx5|4|rx9)\b'

data["MG"] = data["Producto"].str.contains(patron_mg, flags=re.IGNORECASE, regex=True, na=False)
data["MG"] = data["MG"].replace({True: "Sí", False: "No"})

data.to_csv('/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Interanuales/Ventas procesadas/Estudio KIA y MG ventas accesorios-lubricantes-neumaticos-repuestos 2024-2025 (hasta 02-11-2025).csv', index = False)