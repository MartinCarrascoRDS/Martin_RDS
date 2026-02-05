"""
Código para generar pronóstico de ventas a partir de reportes de ventas acumuladas.
"""

import pandas as pd
import numpy as np
import holidays

# 1. Leer informe consolidado de ventas acumuladas (procesado en UNION INFORMES DE VENTA FINAL.py).

fecha = input('Ingrese la fecha de corte (YYYY-MM-DD): ')
fecha_anterior = input('Ingrese la fecha de corte del año anterior (YYYY-MM-DD): ')
path_ventas = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/UNION INFORMES/CONSOLIDADO VENTAS ACUMULADAS {fecha}.xlsx'
df = pd.read_excel(path_ventas)

# 2. Preparar datos para pronóstico.

df['FECHA'] = pd.to_datetime(df['FECHA'])
df = df.sort_values('FECHA')
df['DIA'] = df['FECHA'].dt.dayofweek # (lunes = 0, martes = 1, miércoles = 2, jueves = 3, viernes = 4, sábado = 5, domingo = 6).

# 3. Listas de eventos especiales (días tipo cyber).

eventos_cl = pd.to_datetime([
    '2025-06-02', '2025-06-03', '2025-06-04', # Cyber Day 2025
    '2025-09-01', '2025-09-02', '2025-09-03', # AutoDay Mercado Libre 2025
    '2025-10-06', '2025-10-07', '2025-10-08', # Cyber Monday 2025
    '2025-11-28', '2025-11-29', '2025-11-30', '2025-12-01', # Black Friday 2025
    '2026-06-01', '2026-06-02', '2026-06-03', # Cyber Day 2026
    '2026-08-31', '2026-09-01', '2026-09-02', # AutoDay Mercado Libre 2026
    '2026-10-05', '2026-10-06', '2026-10-07', # Cyber Monday 2025
    '2026-11-27', '2026-11-28', '2026-11-29', '2026-11-30' # Black Friday 2026
])

eventos_pe = pd.to_datetime([
    '2025-04-07', '2025-04-08', '2025-04-09', '2025-04-10', # Cyber Wow 2025 (primera edición)
    '2025-07-14', '2025-07-15', '2025-07-16', '2025-07-17', # Cyber Wow 2025 (segunda edición)
    '2025-10-27', '2025-10-28', '2025-10-29', '2025-10-30', '2025-10-31', # Cyber Days 2025
    '2025-11-28', # Black Friday Perú 2025
    '2026-04-03', '2026-04-04', '2026-04-05', '2026-04-06', # Cyber Wow 2026 (primera edición)
    '2026-07-13', '2026-07-14', '2026-07-15', '2026-07-16', # Cyber Wow 2026 (segunda edición)
    '2026-10-26', '2026-10-27', '2026-10-28', '2026-10-29', '2026-10-30', # Cyber Days 2026
    '2026-11-27' # Black Friday Perú 2026
])

"""
OJO: ir corrigiendo eventos tipo cyber 2026 acorde vayan pasando las fechas reales, las que están puestas ahora son un pronóstico
"""

def asignar_tipo_dia(row):
    if row['ORIGEN'] == 'MELI PERU':
        eventos = eventos_pe
        feriados = feriados_pe
    else:
        eventos = eventos_cl
        feriados = feriados_cl

    if row['FECHA'] in eventos:
        return 'EVENTO'
    elif row['FECHA'] in feriados:
        return 'FERIADO'
    else:
        return 'NORMAL'

# 4. Feriados por país.

año_inicio = df['FECHA'].dt.year.min()
año_fin = pd.to_datetime(fecha).year

años = list(range(año_inicio, año_fin + 1))
feriados_cl = holidays.CL(years = años)
feriados_pe = holidays.PE(years = años)

# 5. Determinar rango de pronóstico.

ultima_fecha = df['FECHA'].max()
ultimo_dia_mes = ultima_fecha + pd.offsets.MonthEnd(0)

if ultima_fecha == ultimo_dia_mes:
    inicio = ultima_fecha + pd.Timedelta(days = 1)
    fin_mes = inicio + pd.offsets.MonthEnd(0)
else:
    fin_mes = ultimo_dia_mes
    inicio = ultima_fecha + pd.Timedelta(days = 1)

fechas_futuras = pd.date_range(inicio, fin_mes, freq = "D")

# 6. Cálculo del pronóstico.

resultados = []

for origen, datos_origen in df.groupby('ORIGEN'):
    grupo = datos_origen['GRUPO'].iloc[0]
    subgrupo = datos_origen['SUBGRUPO'].iloc[0]
    rut = datos_origen['RUT'].iloc[0]

    # Copia local de los datos históricos que se irá actualizando
    historial = datos_origen.copy()

    # Determinar origen de referencia.
    if origen.strip().upper() == 'MELI PERU':
        eventos = eventos_pe
        feriados = feriados_pe
    else:
        eventos = eventos_cl
        feriados = feriados_cl

    for fecha_objetivo in fechas_futuras:
        dia_semana = fecha_objetivo.dayofweek

        # Generar conjunto de candidatos: días con los que se armará el promedio del pronóstico.

        # 6.1. Que sean solo días iguales al día a pronosticar, sin considerar el día mismo.
        candidatos = historial[
            (historial['FECHA'] < fecha_objetivo) &
            (historial['DIA'] == dia_semana)
        ].sort_values('FECHA', ascending = False)

        # 6.2. Eliminar de los candidatos días sin venta, días feriados y días tipo cyber.
        candidatos = candidatos.dropna(subset = ['MONTO DE VENTAS'])
        candidatos = candidatos[~candidatos['FECHA'].isin(eventos)]
        candidatos = candidatos[~candidatos['FECHA'].isin(
            [f for f in candidatos['FECHA'] if f in feriados]
        )]

        # 6.3. Seleccionar los últimos 4 días válidos.
        historicos = candidatos.head(4)

        # 6.4. Calcular el promedio base.
        promedio_base = historicos['MONTO DE VENTAS'].mean() if not historicos.empty else np.nan

        # 6.5. Ajustar según el tipo de día pronosticado.
        if fecha_objetivo in eventos:
            pronostico = promedio_base * 1.45
            tipo_dia = 'EVENTO'
        elif fecha_objetivo in feriados:
            pronostico = promedio_base * 0.46
            tipo_dia = 'FERIADO'
        else:
            pronostico = promedio_base
            tipo_dia = 'NORMAL'

        # 6.6. Dataframe final con pronósticos.
        resultados.append({
            'FECHA': fecha_objetivo,
            'GRUPO': grupo,
            'SUBGRUPO': subgrupo,
            'RUT': rut,
            'ORIGEN': origen,
            'MONTO DE VENTAS': pronostico,
            'TIPO DIA': tipo_dia
        })

        # 6.7. Agregar este pronóstico al histórico
        historial = pd.concat([
            historial,
            pd.DataFrame({
                'FECHA': [fecha_objetivo],
                'DIA': [dia_semana],
                'MONTO DE VENTAS': [pronostico]
            })
        ], ignore_index = True)

# 7. Consolidar resultados.

df_pronostico = pd.DataFrame(resultados)
df_pronostico['MONTO DE VENTAS'] = pd.to_numeric(df_pronostico['MONTO DE VENTAS'])
df_pronostico['MONTO DE VENTAS'] = df_pronostico['MONTO DE VENTAS'].round(0)
df_pronostico['TIPO MONTO DE VENTAS'] = 'PRONOSTICADA'

# 8. Concatenar con INFORME VENTAS ACUMULADA {fecha anterior} -- {fecha}.xlsx

path_reales_mensual = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/UNION INFORMES/INFORME VENTAS ACUMULADAS {fecha_anterior} -- {fecha}.xlsx'
df_reales_mensual = pd.read_excel(path_reales_mensual)
df_reales_mensual['TIPO MONTO DE VENTAS'] = 'REAL'
df_reales_mensual['TIPO DIA'] = df_reales_mensual.apply(asignar_tipo_dia, axis = 1)

df_final = pd.concat([df_reales_mensual, df_pronostico], ignore_index = True)
df_final = df_final.sort_values(['ORIGEN', 'FECHA']).reset_index(drop = True)

# 9. Exportar a Excel.

path_salida = f'/Users/martincarrasco/Desktop/Martín_Carrasco/Reportes/Ventas acumuladas/Procesamiento ventas acumuladas/PRONOSTICOS/INFORME VENTAS ACUMULADAS {fecha_anterior} -- {fecha} CON PRONÓSTICO.xlsx'
df_final.to_excel(path_salida, index = False)

print(f'Se generó el pronóstico de ventas usando la información de ventas disponibles hasta el {fecha}')
print(df_pronostico.head(10))