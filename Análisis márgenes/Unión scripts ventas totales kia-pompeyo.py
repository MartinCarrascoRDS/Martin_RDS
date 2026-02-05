import subprocess
import sys
from pathlib import Path

CUENTAS_MELI = ['KIA', 'POMPEYO']
FECHAS = ['ENERO 2025', 'FEBRERO 2025', 'MARZO 2025', 'ABRIL 2025', 'MAYO 2025', 'JUNIO 2025', 'JULIO 2025', 'AGOSTO 2025',
          'SEPTIEMBRE 2025', 'OCTUBRE 2025', 'NOVIEMBRE 2025', 'DICIEMBRE 2025 (01-15)', 'DICIEMBRE 2025 (16-31)', 'ENERO 2026 (01-15)']
"""FECHAS = ['DICIEMBRE 2025 (16-31)']"""
SCRIPTS = [
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/1.Leer_df_eliminar_paquetes/1.leer_df_eliminar_paquetes.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/2.Eliminar_columnas/2.Eliminar_columnas.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/3.Filtrar_estados/3.Filtrar_estados.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/4.Forzar_formatos/4.Forzar_formatos.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes/5.Limpieza_sku/5.Limpieza_sku.py')
]

for cuenta_meli in CUENTAS_MELI:
    for fecha in FECHAS:
        for script in SCRIPTS:
            print(f"\n--- Ejecutando {Path(script).name} para cuenta {cuenta_meli} y fecha {fecha} ---\n")
            try:
                inputs = f'{cuenta_meli}\n{fecha}\nFalse'
                subprocess.run([sys.executable, script], input = inputs.encode('utf-8'), check = True)
            except subprocess.CalledProcessError as e:
                print(f'Error al ejecutar {Path(script).name} para cuenta {cuenta_meli} y fecha {fecha}: {e}')