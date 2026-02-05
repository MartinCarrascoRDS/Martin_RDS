import os
import re
import pandas as pd
from datetime import datetime

# Carpeta donde están los archivos
folder = "/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/UNION INFORMES"

# Expresión regular para capturar la fecha después de "--"
regex_fecha = re.compile(r"--\s*(\d{4}-\d{2}-\d{2})")

# Listar archivos Excel en la carpeta
archivos = [f for f in os.listdir(folder) if f.endswith(".xlsx")]

# Extraer fechas y agrupar por mes
fechas_archivos = []
for archivo in archivos:
    match = regex_fecha.search(archivo)
    if match:
        fecha_str = match.group(1)
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        fechas_archivos.append((archivo, fecha))

# Pasar a DataFrame para agrupar por mes
df_files = pd.DataFrame(fechas_archivos, columns=["archivo", "fecha"])
df_files["anio_mes"] = df_files["fecha"].dt.to_period("M")

# Quedarse con el archivo de fecha máxima por mes
df_max = df_files.loc[df_files.groupby("anio_mes")["fecha"].idxmax()]

# Leer y concatenar
dfs = []
archivos_usados = []
for _, row in df_max.iterrows():
    path_file = os.path.join(folder, row["archivo"])
    df = pd.read_excel(path_file)  # <-- ajusta sheet_name/dtype si hace falta
    # df["ARCHIVO_ORIGEN"] = row["archivo"]
    dfs.append(df)
    archivos_usados.append(row["archivo"])

# Concatenar todos
df_final = pd.concat(dfs, ignore_index=True)

# Eliminar fechas repetidas, quedándose con la del año más reciente
df_final = (
    df_final
    .sort_values(by = ['AÑO COMPARACIÓN'], ascending = True)
    .drop_duplicates(subset = ['FECHA', 'ORIGEN'], keep = 'last')
)

df_final = df_final.sort_values(by = ['ORIGEN', 'FECHA']).reset_index(drop = True)

# Obtener la última fecha global
ultima_fecha = df_max["fecha"].max().strftime("%Y-%m-%d")

# Nombre del archivo de salida
output_file = os.path.join(folder, f"CONSOLIDADO VENTAS ACUMULADAS {ultima_fecha}.xlsx")

# Guardar en Excel
df_final.to_excel(output_file, index=False)

print("✅ Archivos concatenados y guardados en:")
print("  ", output_file)
print("\nArchivos incluidos en el consolidado:")
for a in archivos_usados:
    print("  -", a)