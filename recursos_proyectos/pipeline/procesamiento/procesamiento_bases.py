import pandas as pd
import calendar
from datetime import datetime
import re

def procesar_por_par_producto_marca(path_csv, fecha_limite, año, seller = None, sep = ','):
    with open(path_csv, mode = 'r', encoding = 'utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'Titulo_Publicacion' in line:
            header_line = i
            break
    else:
            print("Error al leer CSV")
    
    df = pd.read_csv(path_csv, skiprows = header_line, sep = sep)

    df = df.iloc[1:]
    
    df.rename(columns = {
        'Titulo_Publicacion': 'Producto',
        'level3': 'Categoría',
        'level4': 'Subcategoría',
        'Periodo.Mes': 'Mes',
        'Nombre_Vendedor': 'Seller',
        'Volumen_de_Ventas_Moneda_Local': 'Ventas'
    }, inplace = True)

    if seller is not None:
        if isinstance(seller, list):
            df = df[df["Seller"].isin(seller)].copy()
        else:
            df = df[df['Seller'] == seller].copy()

    texto_cols = ['Producto', 'Marca', 'Categoría', 'Subcategoría', 'Seller']
    for col in texto_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    for col in ['Unidades_Vendidas', 'Ventas']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\s+', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    if 'Mes' in df.columns:
        df['Mes'] = pd.to_numeric(df['Mes'], errors='coerce').fillna(0).astype(int)
    else:
        raise ValueError("La columna 'Mes' es necesaria en el CSV")

    df['Año'] = año

    cols = list(df.columns)
    cols.remove('Año')
    mes_index = cols.index('Mes')
    cols.insert(mes_index, 'Año')
    df = df[cols]

    def obtener_ultimo_dia(año, mes):
        ultimo_dia = calendar.monthrange(año, mes)[1]
        return pd.Timestamp(year=año, month=mes, day=ultimo_dia)

    df['Fecha venta'] = df.apply(lambda row: obtener_ultimo_dia(row['Año'], row['Mes']), axis=1)
    df['Fecha venta'] = df['Fecha venta'].dt.strftime('%Y-%m-%d')

    cols = list(df.columns)
    cols.remove('Fecha venta')
    mes_index = cols.index('Mes')
    cols.insert(mes_index + 1, 'Fecha venta')
    df = df[cols]

    df['Fecha venta'] = pd.to_datetime(df['Fecha venta'])

    df = df[df['Fecha venta'] < fecha_limite]

    fechas_completas = pd.date_range(start=df['Fecha venta'].min(),
                                     end=df['Fecha venta'].max(),
                                     freq='M')

    producto_marca = df[['Producto', 'Marca']].drop_duplicates()

    combinaciones = (
        producto_marca.assign(key=1)
        .merge(pd.DataFrame({'Fecha venta': fechas_completas, 'key': 1}), on='key')
        .drop('key', axis=1)
    )

    df = combinaciones.merge(df, 
                             on=['Producto', 'Marca', 'Fecha venta'], 
                             how='left')

    df['Unidades_Vendidas'] = df['Unidades_Vendidas'].fillna(0).astype(int)

    df = df.groupby(
        ["Producto", "Marca", "Fecha venta"], as_index=False
    ).agg({"Unidades_Vendidas": "sum"})

    df = df[["Producto", "Marca", "Fecha venta", "Unidades_Vendidas"]]

    return df


def procesar_por_columna(path_csv, fecha_limite, año, columna_agrupacion, seller = None, sep = ','):
    with open(path_csv, mode = 'r', encoding = 'utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'Titulo_Publicacion' in line:
            header_line = i
            break
    else:
            print("Error al leer CSV")
    
    df = pd.read_csv(path_csv, skiprows = header_line, sep = sep)

    df = df.iloc[1:]
    
    df.rename(columns = {
        'Titulo_Publicacion': 'Producto',
        'level3': 'Categoría',
        'level4': 'Subcategoría',
        'Periodo.Mes': 'Mes',
        'Nombre_Vendedor': 'Seller',
        'Volumen_de_Ventas_Moneda_Local': 'Ventas'
    }, inplace = True)

    if seller is not None:
        if isinstance(seller, list):
            df = df[df["Seller"].isin(seller)].copy()
        else:
            df = df[df['Seller'] == seller].copy()

    texto_cols = ['Producto', 'Marca', 'Categoría', 'Subcategoría', 'Seller']
    for col in texto_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    for col in ['Unidades_Vendidas', 'Ventas']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\s+', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    if 'Mes' in df.columns:
        df['Mes'] = pd.to_numeric(df['Mes'], errors='coerce').fillna(0).astype(int)
    else:
        raise ValueError("La columna 'Mes' es necesaria en el CSV")

    df['Año'] = año

    cols = list(df.columns)
    cols.remove('Año')
    mes_index = cols.index('Mes')
    cols.insert(mes_index, 'Año')
    df = df[cols]

    def obtener_ultimo_dia(año, mes):
        ultimo_dia = calendar.monthrange(año, mes)[1]
        return pd.Timestamp(year=año, month=mes, day=ultimo_dia)

    df['Fecha venta'] = df.apply(lambda row: obtener_ultimo_dia(row['Año'], row['Mes']), axis=1)
    df['Fecha venta'] = df['Fecha venta'].dt.strftime('%Y-%m-%d')

    cols = list(df.columns)
    cols.remove('Fecha venta')
    mes_index = cols.index('Mes')
    cols.insert(mes_index + 1, 'Fecha venta')
    df = df[cols]

    df['Fecha venta'] = pd.to_datetime(df['Fecha venta'])
    df = df[df["Fecha venta"] < fecha_limite]

    fechas_completas = pd.date_range(start=df['Fecha venta'].min(),
                                  end=df['Fecha venta'].max(),
                                  freq='M')
    
    agrupacion_unica = df[columna_agrupacion].drop_duplicates()

    combinaciones = (
    agrupacion_unica.assign(key=1)
    .merge(pd.DataFrame({'Fecha venta': fechas_completas, 'key': 1}), on='key')
    .drop('key', axis=1)
)

    df = combinaciones.merge(df,
                         on=[columna_agrupacion, 'Fecha venta'],
                         how='left')
    
    df['Unidades_Vendidas'] = df['Unidades_Vendidas'].fillna(0)

    df['Unidades_Vendidas'] = df['Unidades_Vendidas'].astype(int)

    df = df.groupby(
    [columna_agrupacion, "Fecha venta"], as_index=False
).agg({"Unidades_Vendidas": "sum"})

    df = df[[columna_agrupacion, "Fecha venta", "Unidades_Vendidas"]]
    return df



def ventas_semanales(ruta_archivo_anterior, ruta_archivo_actual, ruta_salida = None):
    """
    Compara dos archivos de ventas individuales y extrae las filas exclusivas del archivo más reciente.

    Parámetros:
    - ruta_archivo_anterior (str): Ruta al archivo con ventas hasta una fecha anterior.
    - ruta_archivo_actual (str): Ruta al archivo con ventas hasta una fecha más reciente.
    - ruta_salida (str, opcional): Ruta donde guardar el archivo resultante. Si es None, no se guarda.

    Retorna:
    - DataFrame con las ventas exclusivas del archivo más reciente.
    """
    df_anterior = pd.read_csv(ruta_archivo_anterior)
    df_actual = pd.read_csv(ruta_archivo_actual)
    
    df_anterior = procesar_para_powerBI(df_anterior)
    df_actual = procesar_para_powerBI(df_actual)

    df_anterior.columns = df_anterior.columns.str.lower()
    df_actual.columns = df_actual.columns.str.lower()

    columnas_excluir = {'Año', 'Mes', 'Fecha venta'}
    columnas_clave = [col for col in df_actual.columns if col not in columnas_excluir]

    df_merge = df_actual.merge(
        df_anterior[columnas_clave],
        on = columnas_clave,
        how = 'left',
        indicator = True
    )

    ventas_nuevas = df_merge[df_merge['_merge'] == 'left_only'].drop(columns = ['_merge'])

    if ruta_salida:
        ventas_nuevas.to_excel(ruta_salida, index = False)

    return ventas_nuevas



def procesar_para_powerBI(path_csv, año, fecha_ultima_venta, mercado, producto = None, marca = None, categoria = None, subcategoria = None, seller = None, sep = ','):

    """
    Procesa una base de datos proveniente de un archivo CSV de Nubimetrics para su uso en Power BI. Puede ser usada también con otros fines
    """
    with open(path_csv, mode = 'r', encoding = 'utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if 'Titulo_Publicacion' in line:
            header_line = i
            break
    else:
            print("Error al leer CSV")
    
    df = pd.read_csv(path_csv, skiprows = header_line, sep = sep)
    

    df = df.iloc[1:]
    
    df.rename(columns = {
        'Titulo_Publicacion': 'Producto',
        'sku': 'SKU',
        'level3': 'Categoría',
        'level4': 'Subcategoría',
        'Periodo.Mes': 'Mes',
        'Nombre_Vendedor': 'Seller',
        'Volumen_de_Ventas_Moneda_Local': 'Ventas'
    }, inplace = True)

    if 'Producto' in df.columns:
        df.insert(loc = df.columns.get_loc('Producto') + 1, column = 'Mercado', value = mercado)
    else:
        print("La columna 'Producto' no se encuentra en el DataFrame. Asegúrate de que el CSV tenga la estructura correcta.")
    
    if producto is not None:
        if isinstance(producto, list):
            df = df[df["Producto"].isin(producto)].copy()
        else:
            df = df[df['Producto'] == producto].copy()

    if marca is not None:
        if isinstance(marca, list):
            df = df[df["Marca"].isin(marca)].copy()
        else:
            df = df[df['Marca'] == marca].copy()

    if categoria is not None:
        if isinstance(categoria, list):
            df = df[df["Categoría"].isin(categoria)].copy()
        else:
            df = df[df['Categoría'] == categoria].copy()

    if subcategoria is not None:
        if isinstance(subcategoria, list):
            df = df[df["Subcategoría"].isin(subcategoria)].copy()
        else:
            df = df[df['Subcategoría'] == subcategoria].copy()
    
    if seller is not None:
        if isinstance(seller, list):
            df = df[df["Seller"].isin(seller)].copy()
        else:
            df = df[df['Seller'] == seller].copy()

    texto_cols = ['Producto', 'Marca', 'Categoría', 'Subcategoría', 'Seller']
    for col in texto_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    for col in ['Unidades_Vendidas', 'Ventas']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r'\s+', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            df[col] = df[col].round(0).astype(int)

    df['Mes'] = pd.to_numeric(df['Mes'], errors = 'coerce').astype(int)

    df['Año'] = año
    cols = list(df.columns)
    cols.remove('Año')
    mes_index = cols.index('Mes')
    cols.insert(mes_index, 'Año')
    df = df[cols]

    def obtener_primer_dia(año, mes):
        return pd.Timestamp(year=año, month=mes, day=1)
    
    df['Fecha venta'] = df.apply(lambda row: obtener_primer_dia(row['Año'], row['Mes']), axis=1)
    df['Fecha venta'] = df['Fecha venta'].dt.strftime('%Y-%m-%d')

    cols = list(df.columns)
    cols.remove('Fecha venta')
    mes_index = cols.index('Mes')
    cols.insert(mes_index + 1, 'Fecha venta')
    df = df[cols]

    diccionario_proveedores = {
        'MA': 'MANNHEIM',
        'SC': 'MATSUMOTO',
        'BI': 'BICIMOTO',
        'CR': 'CUATRO RUEDAS',
        'AL': 'ALSACIA',
        'NR': 'NORIEGA',
        'EM': 'EMASA',
        'NC': 'NEUMACHILE',
        'RX': 'REFAX',
        'GAB': 'GABTEC',
        'ATM': 'AUTOMARCO',
        'TEC': 'AUTOTEC',
        'MEC': 'MEC',
        'IM': 'IMASA',
        'IT': 'ITALFRENOS',
        'RDS': 'BODEGA'
    }

    sellers_rds = {
    'AUTOSOLSERVITECA', 'REPUESTOS DEL SOL', 'REICARSCHILE', 'BLACKPARTSCL',
    'RDS3', 'MERCADOREPUESTOSCL', 'TRI PARTS', 'INVERSIONESDELSOL LTDA',
    'INDUSOLRDS', 'HYUNDAI CHILE', 'TYC'
    }

    def extraer_proveedor(sku, seller):
        if pd.isna(sku) or pd.isna(seller):
            return "-"
        
        if seller not in sellers_rds:
            return "-"
        
        sku = str(sku).upper()
        sku = re.sub(r'^(XXF|FXX|XX|F)', '', sku)

        for abrev in sorted(diccionario_proveedores.keys(), key = lambda x: -len(x)):
            if sku.startswith(abrev):
                return diccionario_proveedores[abrev]
            
        return "-"
    
    df['Proveedor'] = df.apply(lambda row: extraer_proveedor(row['SKU'], row['Seller']), axis = 1)

    cols = list(df.columns)
    cols.remove('Proveedor')
    mercado_index = cols.index('Mercado')
    cols.insert(mercado_index + 1, 'Proveedor')
    df = df[cols]

    nombre_partes = [f'Ventas_procesadas_mercado_de_{mercado}']

    if producto:
        nombre_partes.append(f'producto_{producto}')
    if marca:
        nombre_partes.append(f'marca_{marca}')
    if categoria:
        nombre_partes.append(f'categoria_{categoria}')
    if subcategoria:
        nombre_partes.append(f'subcategoria_{subcategoria}')
    if seller:
        nombre_partes.append(f'seller_{seller}')

    es_31_diciembre = False
    
    try:
        fecha_dt = datetime.strptime(fecha_ultima_venta, '%Y-%m-%d')
        if fecha_dt.day == 31 and fecha_dt.month == 12:
            es_31_diciembre = True
    except ValueError:
            pass
    
    if es_31_diciembre:
        nombre_partes.append(f'año_{año}')
    else:
        nombre_partes.append(f'año_{año}_hasta_{fecha_ultima_venta}')
        
    nombre_archivo = '_'.join(nombre_partes) + '.csv'

    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', sep = sep)

    return df