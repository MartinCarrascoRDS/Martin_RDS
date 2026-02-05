import subprocess
import sys

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')

scripts = [
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/FERRE.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/RDS.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS DIGITALES.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS SHOWROOM.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/SHOPIFY.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTAS RIPLEY.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/WALMART.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/MELI PERU.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/AUTOSOL.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/KIA Y POMPEYO.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA INTERNA.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/VENTA EMPRESA.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/UNION INFORMES DE VENTA.py", 2),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/UNION INFORMES DE VENTA FINAL.py", 0),
    ("/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/Pronóstico con ventas acumuladas.py", 2)
]

for script, num_inputs in scripts:
    print(f"\n--- Ejecutando {script} ---\n")
    if num_inputs == 2:
        inputs = f"{fecha}\n{fecha_anterior}\n"
    elif num_inputs == 1:
        inputs = f"{fecha}\n"
    else:
        inputs = ""
    subprocess.run([sys.executable, script], input=inputs.encode("utf-8"), check=True)