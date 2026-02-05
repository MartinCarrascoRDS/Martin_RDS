import subprocess
import sys
from pathlib import Path

CUENTAS_MELI = ['RDS PERU']
FECHAS = ['SEPTIEMBRE 2025', 'OCTUBRE 2025', 'NOVIEMBRE 2025', 'DICIEMBRE 2025']
SCRIPTS = [
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/1.Leer_df_eliminar_paquetes/1.leer_df_eliminar_paquetes.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/2.Eliminar_columnas/2.Eliminar_columnas.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/3.Filtrar_estados/3.Filtrar_estados.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/4.Forzar_formatos/4.Forzar_formatos.py'),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/5.Limpieza_sku/5.Limpieza_sku.py')
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