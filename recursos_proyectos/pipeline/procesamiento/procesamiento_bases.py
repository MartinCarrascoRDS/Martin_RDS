import pandas as pd
import calendar

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

    df['Fecha_Compra'] = df.apply(lambda row: obtener_ultimo_dia(row['Año'], row['Mes']), axis=1)
    df['Fecha_Compra'] = df['Fecha_Compra'].dt.strftime('%Y-%m-%d')

    cols = list(df.columns)
    cols.remove('Fecha_Compra')
    mes_index = cols.index('Mes')
    cols.insert(mes_index + 1, 'Fecha_Compra')
    df = df[cols]

    df['Fecha_Compra'] = pd.to_datetime(df['Fecha_Compra'])

    df = df[df['Fecha_Compra'] < fecha_limite]

    fechas_completas = pd.date_range(start=df['Fecha_Compra'].min(),
                                     end=df['Fecha_Compra'].max(),
                                     freq='M')

    producto_marca = df[['Producto', 'Marca']].drop_duplicates()

    combinaciones = (
        producto_marca.assign(key=1)
        .merge(pd.DataFrame({'Fecha_Compra': fechas_completas, 'key': 1}), on='key')
        .drop('key', axis=1)
    )

    df = combinaciones.merge(df, 
                             on=['Producto', 'Marca', 'Fecha_Compra'], 
                             how='left')

    df['Unidades_Vendidas'] = df['Unidades_Vendidas'].fillna(0).astype(int)

    df = df.groupby(
        ["Producto", "Marca", "Fecha_Compra"], as_index=False
    ).agg({"Unidades_Vendidas": "sum"})

    df = df[["Producto", "Marca", "Fecha_Compra", "Unidades_Vendidas"]]

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

    df['Fecha_Compra'] = df.apply(lambda row: obtener_ultimo_dia(row['Año'], row['Mes']), axis=1)
    df['Fecha_Compra'] = df['Fecha_Compra'].dt.strftime('%Y-%m-%d')

    cols = list(df.columns)
    cols.remove('Fecha_Compra')
    mes_index = cols.index('Mes')
    cols.insert(mes_index + 1, 'Fecha_Compra')
    df = df[cols]

    df['Fecha_Compra'] = pd.to_datetime(df['Fecha_Compra'])
    df = df[df["Fecha_Compra"] < fecha_limite]

    fechas_completas = pd.date_range(start=df['Fecha_Compra'].min(),
                                  end=df['Fecha_Compra'].max(),
                                  freq='M')
    
    agrupacion_unica = df[columna_agrupacion].drop_duplicates()

    combinaciones = (
    agrupacion_unica.assign(key=1)
    .merge(pd.DataFrame({'Fecha_Compra': fechas_completas, 'key': 1}), on='key')
    .drop('key', axis=1)
)

    df = combinaciones.merge(df,
                         on=[columna_agrupacion, 'Fecha_Compra'],
                         how='left')
    
    df['Unidades_Vendidas'] = df['Unidades_Vendidas'].fillna(0)

    df['Unidades_Vendidas'] = df['Unidades_Vendidas'].astype(int)

    df = df.groupby(
    [columna_agrupacion, "Fecha_Compra"], as_index=False
).agg({"Unidades_Vendidas": "sum"})

    df = df[[columna_agrupacion, "Fecha_Compra", "Unidades_Vendidas"]]
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

    columnas_excluir = {'Año', 'Mes', 'Fecha_Compra'}
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



def procesar_para_powerBI(path_csv, año, producto = None, marca = None, categoria = None, subcategoria = None, seller = None, sep = ','):
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

    df['Fecha_Compra'] = df.apply(lambda row: obtener_ultimo_dia(row['Año'], row['Mes']), axis=1)
    df['Fecha_Compra'] = df['Fecha_Compra'].dt.strftime('%Y-%m-%d')

    cols = list(df.columns)
    cols.remove('Fecha_Compra')
    mes_index = cols.index('Mes')
    cols.insert(mes_index + 1, 'Fecha_Compra')
    df = df[cols]

    return df