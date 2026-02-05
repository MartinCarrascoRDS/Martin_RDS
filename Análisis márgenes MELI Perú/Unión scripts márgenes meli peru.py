import subprocess
import sys
from pathlib import Path

CUENTAS_MELI = ['RDS PERU']
FECHAS = ['ENERO 2026']
SCRIPTS = [
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/1.Leer_df_eliminar_paquetes/1.leer_df_eliminar_paquetes.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/2.Eliminar_columnas/2.Eliminar_columnas.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/3.Filtrar_estados/3.Filtrar_estados.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/4.Forzar_formatos/4.Forzar_formatos.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/5.Limpieza_sku/5.Limpieza_sku.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/6.Separar_sku/6.Separar_sku.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/7.Cruzar_costos_full/7.Cruzar_costos_full.py', 0),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/8.Cruzar_costos_gral/8.Cruzar_costos_gral.py', 0),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/9.Descuentos/9.Descuentos.py', 0),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/10.Eliminar_sin_costos/10.Eliminar_sin_costos.py', 2),
    ('/Users/martincarrasco/Desktop/Martín_Carrasco/Análisis márgenes MELI Perú/11.Margenes/11.Margenes.py', 2)
]

for cuenta_meli in CUENTAS_MELI:
    for fecha in FECHAS:
        for script, num_params in SCRIPTS:
            print(f"\n--- Ejecutando {Path(script).name} para cuenta {cuenta_meli} y fecha {fecha} ---\n")

            if num_params == 2:
                inputs = f'{cuenta_meli}\n{fecha}\n'
                subprocess.run([sys.executable, script], input = inputs.encode('utf-8'), check = True)
            else:
                subprocess.run([sys.executable, script], check = True)