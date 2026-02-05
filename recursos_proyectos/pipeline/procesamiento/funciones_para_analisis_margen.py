"""
FUNCIONES PARA ANÁLISIS DE MÁRGENES

El siguiente archivo contiene las funciones que se utilizan dentro del análisis de márgenes.
Originalmente, estas funciones se encuentran repartidas en varios archivos .py dentro de la carpeta Análisis márgenes, y algunos dentro de algunos archivos .py dentro del pipeline.
El objetivo de este archivo es tener todas las funciones en un solo lugar, para facilitar su mantenimiento, actualización y uso.
"""

import pandas as pd
import numpy as np
import re

# Funciones que se utilizan en el primer paso del análisis de márgenes

def extraer_numero_de_paquetes(estado_str):
    """
    Extrae el número de ventas en paquete desde una cadena de texto.
    Pensado puntualmente para usar en la columna 'Estado' de la base de datos de ventas de Mercado Libre, que indica 'Paquete de x productos' cuando la venta es en paquete.

    Argumentos:
    estado_str (str): Cadena de texto que contiene información sobre el estado de la venta.
    Retorna:
    int: Número de ventas en paquete. Si no se encuentra información, retorna 0.
    """

    match = re.search(r"Paquete de (\d+)", str(estado_str))
    return int(match.group(1)) if match else 0

def extraer_año_desde_fecha(fecha):
    """
    Extrae el año de una fecha para poder leerla correctamente en los directorios.

    Argumentos:
    fecha (str): Cadena de texto que contiene la fecha de las ventas en formato 'MES AÑO' (ENERO 2026, FEBRERO 2025, SEPTIEMBRE 2025 (HASTA 07-09), etc.)
    """

    match = re.search(r'(20\d{2})', fecha)
    if not match:
        raise ValueError(f'No se pudo extraer el año a partir de la fecha {fecha}')
    return int(match.group(1))

meses_es = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

def convertir_fechas(fecha_str):
    """
    Junto con meses_es, fue directamente obtenida del paso 4 del análisis de márgenes.
    Está especialmente pensado para las bases de ventas obtenidas de Mercado Libre.
    """
    if pd.isna(fecha_str):
        return pd.NaT
    try:
        fecha_str = str(fecha_str).lower()
        fecha_str = re.sub(r"\s*hs\.?", "", fecha_str)
        partes = fecha_str.split(' de ')
        if len(partes) < 3:
            return pd.NaT
        dia = partes[0].strip().zfill(2)
        mes = meses_es.get(partes[1].strip(), '01')
        año_hora = partes[2].strip()
        año = año_hora.split()[0]
        return pd.to_datetime(f"{año}/{mes}/{dia}", format="%Y/%m/%d")
    except Exception:
        return pd.NaT

# Funciones que se utilizan en el Paso 1.1, que consta de la limpieza de SKU

def limpiar_sku(sku):
    """
    Limpia prefijos 'F- ', 'XX- ' y 'Z- ' en cualquier parte de cada fragmento separado por '/',
    normaliza multiplicadores, elimina paréntesis y espacios innecesarios.
    
    Argumentos:
    sku (str): el SKU a limpiar.
    Retorna:
    str: el SKU limpio para el formato RDS.
"""

    # Si el SKU es NaN, retornar NaN
    if pd.isna(sku):
        return sku
    
    # Convertir a mayúscula y eliminar espacios al inicio y final
    sku = str(sku).upper().strip()

    # Separar por '/' y limpiar los prefijos en cada parte
    partes = re.split(r"\s*/\s*", sku)
    partes_limpias = [
        re.sub(r"(F-\s*|XX-\s*|Z-\s*)+", "", parte).strip()
        for parte in partes
    ]
    sku_limpio = " / ".join(partes_limpias)

    # Insertar espacio si el formato es como "RX-9951960"
    sku = re.sub(r'([A-Z]+-)(\d)', r'\1 \2', sku)

    # Eliminar " / " solo si está antes de un multiplicador tipo X2, X3, X4...
    # Ejemplo: "RX- 0020611 / X2" → "RX- 0020611 X2"
    sku = re.sub(r'\s*/\s*(X\d+)\b', r' \1', sku)

    # Detectar multiplicadores tipo (X2), (X 2), etc. y convertirlos a "X2"
    sku_limpio = re.sub(r"\(\s*[Xx]\s*(\d{1,3})\s*\)", r" X\1", sku_limpio)

    # Eliminar contenido entre paréntesis
    sku_limpio = re.sub(r"\([^)]*\)", "", sku_limpio).strip()

    # Corregir espacios alrededor de "/"
    sku_limpio = re.sub(r"\s*/\s*", " / ", sku_limpio)

    # Unificar "X 2", "X   10", etc. en "X2", "X10"
    sku_limpio = re.sub(r"X\s+(\d+)", r"X\1", sku_limpio)

    # Agregar " / " antes de BI-, IT-, etc. cuando no hay barra
    sku_limpio = re.sub(r"(?<!/)\s(?=[A-Z]{2,6}-\s)", " / ", sku_limpio)

    # Limpiar espacios dobles restantes
    sku_limpio = re.sub(r"\s{2,}", " ", sku_limpio).strip()

    return sku_limpio

# def limpiar_sku(sku):
#     """
#     Limpia prefijos 'F-', 'XX-' y 'Z-' en cualquier parte de cada fragmento separado por '/',
#     normaliza multiplicadores, elimina paréntesis y espacios innecesarios.

#     Args:
#         sku (str): el SKU a limpiar.

#     Returns:
#         str | pd.NA: el SKU limpio para el formato RDS.
#     """
#     import re
#     import pandas as pd

#     # Normalización de casos nulos o vacíos
#     if sku is None:
#         return pd.NA
#     sku_str = str(sku).strip()
#     if sku_str == "" or sku_str.upper() in {"NAN", "NONE"}:
#         return pd.NA

#     # Trabajar sobre una sola variable consistente
#     sku = sku_str.upper().strip()

#     # 1) Separar por "/" y procesar cada fragmento
#     partes = re.split(r"\s*/\s*", sku)
#     partes_limpias = []
#     for parte in partes:
#         p = parte.strip()

#         # Eliminar prefijos: F-, XX-, Z-
#         p = re.sub(r'\b(?:F|XX|Z)-\s*', '', p)

#         # Insertar espacio si formato "RX-9951960"
#         p = re.sub(r'([A-Z]+-)(?=\d)', r'\1 ', p)

#         # Quitar "/ X2" -> " X2"
#         p = re.sub(r'\s*/\s*(X\d+)\b', r' \1', p, flags=re.IGNORECASE)

#         partes_limpias.append(p)

#     # Reunir con " / "
#     sku_limpio = " / ".join([pt for pt in partes_limpias if pt != ""])

#     # Normalizaciones globales
#     sku_limpio = re.sub(r"\(\s*[Xx]\s*(\d{1,3})\s*\)", r" X\1", sku_limpio)
#     sku_limpio = re.sub(r"\([^)]*\)", "", sku_limpio).strip()
#     sku_limpio = re.sub(r"\s*/\s*", " / ", sku_limpio)
#     sku_limpio = re.sub(r"\bX\s+(\d+)\b", r"X\1", sku_limpio, flags=re.IGNORECASE)
#     sku_limpio = re.sub(r"(?<!/)\s(?=[A-Z]{2,6}-\s)", " / ", sku_limpio)
#     sku_limpio = re.sub(r"\s{2,}", " ", sku_limpio).strip()
#     sku_limpio = re.sub(r"^\d+W-\s*", "", sku_limpio, flags=re.IGNORECASE)

#     if sku_limpio == "":
#         return pd.NA

#     return sku_limpio

def limpiar_sku_walmart(sku):
    """
    Limpia códigos SKU provenientes de Walmart, que siguen la siguiente estructura:
    <código interno walmart>- <código proveedor>- <código producto proveedor> / <multiplicador>

    Ejemplo de input:
    '1W- RX- 235236'
    '12W- IT- 233634 / X2'

    Pasos:
    1. Convertir a mayúsculas
    2. Eliminar código interno walmart
    3. Eliminar / antes del multiplicador, para que este quede separado del SKU con un espacio ("IT- 233634 X2")
    4. Pasos similares a la función limpiar_sku
    """

    if not isinstance(sku, str):
        return sku
    
    sku = sku.upper()

    sku = re.sub(r'\b\d{1,3}W-\s*', '', sku)

    sku = re.sub(r'^([A-Z]{2})-([A-Z0-9])', r'\1- \2', sku)

    multiplicador = re.search(r'/\s*X(\d+)', sku)
    mult_text = ""
    if multiplicador:
        valor = multiplicador.group(1)
        mult_text = f" X{valor}"
        sku = re.sub(r'/\s*X\d+', '', sku)

    sku = re.sub(r'[^A-Z0-9\- ]', '', sku)

    sku = re.sub(r'\s{2,}', ' ', sku).strip()

    sku = sku + mult_text

    return sku


def obtener_proveedores(sku_limpio):
    """
    Extrae las siglas de los proveedores desde un SKU limpio.
    Las siglas son las letras antes del guion en cada fragmento separado por '/'.
    
    Argumentos:
    sku_limpio (str): el SKU limpio del cual se extraerán las siglas.
    Retorna:
    list: una lista ordenada de siglas únicas de proveedores.
    """
    partes = str(sku_limpio).split(" / ")
    siglas = set()

    for parte in partes:
        match = re.match(r"([A-Z]{2,6})-", parte.strip())
        if match:
            siglas.add(match.group(1))

    return sorted(siglas)

# Funciones que se utilizan en el Paso 1.2, que consta de la detección de estados y su clasificación

inicios_estados_ventas = (
    'Acuerdas la entrega',
    'Despacharemos el paquete',
    'El envío está demorado, pero ya tienes el dinero disponible',
    'En camino',
    'En punto de retiro',
    'Entregado',
    'Etiqueta lista para imprimir',
    'Etiqueta para imprimir',
    'Etiqueta impresa',
    'Envío demorado',
    'Envío reprogramado',
    'Listo para recolección',
    'Llega el',
    'Llega entre el',
    'Mediación finalizada. Te dimos el dinero',
    'Procesando en la bodega',
    'Venta concretada',
    'Venta entregada',
    'Venta no entregada. Te dimos el dinero'
)

def clasificar_estado(estado):
    """
    Clasifica el estado de una venta en categorías: 'Venta', 'Devolución', 'Reclamo', 'Cancelado' u 'Otro'.
    
    Argumentos:
    estado (str): el estado de la venta a clasificar.
    Retorna:
    str: la categoría del estado.
    """
    if pd.isna(estado):
        return np.nan

    estado_lower = estado.lower()

    for inicio in inicios_estados_ventas:
        if estado.startswith(inicio):
            return 'Venta'
        
    if any(palabra in estado_lower for palabra in ['devolución', 'devuelto', 'devolvió', 'devolveremos']):
        return 'Devolución'
    
    if any(palabra in estado_lower for palabra in ['reclamo', 'venta con solicitud de cambio']):
        return 'Reclamo'
    
    if 'mediación' in estado_lower and not estado.startswith('Mediación finalizada. Te dimos el dinero'):
        return 'Reclamo'
    
    if 'no entregado' in estado_lower and not estado.startswith('Venta no entregada. Te dimos el dinero'):
        return 'Reclamo'
    
    if any(palabra in estado_lower for palabra in ['cancelaste', 'cancelada', 'cancelado', 'paquete no entregado']):
        return 'Cancelado'
    
    return "Otro"

# Funciones que se utilizan en el Paso 6, que consta de la expansión de SKUs

def expand_sku(sku_limpio):
    """
    Expande un SKU limpio en una lista de SKUs individuales, considerando multiplicadores.
    
    Argumentos:
    sku_limpio (str): el SKU limpio a expandir.
    Retorna:
    list: una lista de SKUs individuales.
    """

    if pd.isna(sku_limpio):
        return []
    sku_limpio = str(sku_limpio).strip()
    if sku_limpio == "":
        return []
    
    parts = [s.strip() for s in sku_limpio.split(" / ")]
    expanded = []
    i = 0
    while i < len(parts):
        item = parts[i]

        # CASO 1: es un multiplicador suelto tipo X2
        match_mult = re.fullmatch(r"x(\d+)", item.lower())
        if match_mult and expanded:
            count = int(match_mult.group(1))
            expanded.extend([expanded[-1]] * (count - 1))  # ya hay una, agrega el resto

        else:
            # CASO 2: SKU con multiplicador pegado al final (ejemplo "AL- 2352 X2")
            match_embedded = re.fullmatch(r"(.*)\s+X(\d+)", item, re.IGNORECASE)
            if match_embedded:
                sku_base = match_embedded.group(1).strip()
                count = int(match_embedded.group(2))
                expanded.extend([sku_base] * count)
            else:
                # CASO 3: SKU normal
                expanded.append(item)

        i += 1
    return expanded

# Funciones que se utilizan en el Paso 9, que consta de la aplicación de descuentos a los productos

# descuentos_importadoras = {
#     'MA': 0.05,
#     'RX': 0.10,
#     'CR': 0.03,
#     'AL': 0.04,
#     'NC': 0.04
# }

descuentos_importadoras = {} # Se deja vacío cuando no hay un descuento de tipo cyber

def aplicar_descuentos(df, fecha_col, fecha_inicio, fecha_fin, descuentos_dict, activar=True, reglas_extra=None):
    """
    Aplica descuentos a los costos de un DataFrame según rango de fechas, prefijos de SKU y reglas adicionales.

    Argumentos:
    df (pd.DataFrame): DataFrame de entrada que contiene columnas de SKUs y sus costos asociados.
    fecha_col (str): nombre de la columna en 'df' que contiene las fechas de venta.
    fecha_inicio (str o pd.Timestamp): fecha de inicio de rango en el que se aplican los descuentos.
    fecha_fin (str o pd.Timestamp): fecha de fin de rango en el que se aplican los descuentos.
    descuentos_dict (dict): diccionario de pares {prefijo: descuento} donde prefijo es un string (ej: "MA") y descuento es un número entre 0 y 1.
    activar (bool, opcional, default = True): Si es False, no aplica descuentos y devuelve el DataFrame original.
    reglas_extra (list, opcional, default = None): Lista de funciones adicionales que reciben cada fila ('row') del DataFrame y retornan la fila modificada. Se aplican después de los descuentos por prefijo.
    Retorna:
    pd.DataFrame: copia del DataFrame original con columnas adicionales 'Costo_post_dcto_{SKU_x}' que contienen los costos ajustados según descuentos aplicados.
    """
    if not activar:
        print("Descuentos no aplicados, devolviendo el DataFrame original.")
        return df

    df = df.copy()
    df[fecha_col] = pd.to_datetime(df[fecha_col])
    en_rango = (df[fecha_col] >= fecha_inicio) & (df[fecha_col] <= fecha_fin)

    sku_cols = [col for col in df.columns if re.match(r"^SKU_\d+$", col)]
    costo_cols = [f"Costo_{col}" for col in sku_cols]
    costo_full_cols = [f"Costo_full_{col}" for col in sku_cols]

    for sku_col, costo_col, costo_full_col in zip(sku_cols, costo_cols, costo_full_cols):
        nuevo_col = f"Costo_post_dcto_{sku_col}"

        def aplicar_descuento(row):
            if not en_rango.loc[row.name]:
                return row[costo_col] if row.get("Forma de entrega", "").strip() != "Mercado Envíos Full" else row[costo_full_col]
            
            if str(row.get("Forma de entrega", "")).strip() == "Mercado Envíos Full":
                return row.get(costo_full_col, np.nan)
            
            sku = str(row[sku_col]).strip().upper()
            prefijo = sku.split('-')[0] if '-' in sku else sku
            descuento = descuentos_dict.get(prefijo, 0)
            costo = row.get(costo_col, np.nan)
            if pd.isna(costo):
                return costo
            return costo * (1 - descuento)

        df[nuevo_col] = df.apply(aplicar_descuento, axis=1)

    if reglas_extra:
        for regla in reglas_extra:
            df = df.apply(regla, axis=1)

    return df


def descuento_sku_prefijo(
    row,
    prefijo="IT-",
    porcentaje=0.15,
    fecha_col="Fecha de venta",
    fecha_inicio=None,
    fecha_fin=None,
    excluir_full=False
):
    
    """
    Aplica un descuento a los costos de un SKU dentro de una fila del DataFrame, condicionado por el prefijo del SKU, el rango de fechas y la modalidad (Full o no).

    Argumentos:
    row (pd.Series): Fila del DataFrame sobre la cual se aplicará el descuento.
    prefijo (str, opcional, default = "IT-"): prefijo del SKU que activa la aplicación del descuento.
    porcentaje (float, opcional, default = 0.15): porcentaje de descuento a aplicar. Debe ser un número entre 0 y 1.
    fecha_col (str, opcional, default = 'Fecha de venta'): nombre de la columna que contiene la fecha de la venta.
    fecha_inicio (str o pd.Timestamp, opcional, default = None): fecha de inicio del rango en el que se aplica el descuento. Si es None, no se aplica restricción por inicio.
    fecha_fin (str o pd.Timestamp, opcional, default = None): fecha de fin del rango en el que se aplica el descuento. Si es None, no se aplica restricción por fin.
    excluir_full (bool, opcional, default = False): Si es True, no aplica descuentos a las filas que corresponden a la modalidad Full.

    Retorna:
    pd.Series: La fila original ('row') con los costos modificados si corresponde aplicar el descuento.
    """

    fecha = row[fecha_col]
    if fecha_inicio and fecha < pd.to_datetime(fecha_inicio):
        return row
    if fecha_fin and fecha > pd.to_datetime(fecha_fin):
        return row

    sku_cols = [c for c in row.index if c.startswith("SKU_") and c[4:].isdigit()]

    for col in sku_cols:
        if str(row[col]).startswith(prefijo):

            if not excluir_full and row.get("Forma de entrega", "") == "Mercado Envíos Full":
                costo_col = f"Costo_full_{col}"
            else:
                costo_col = f"Costo_{col}"

            costo_post_col = f"Costo_post_dcto_{col}"

            if costo_post_col not in row.index:
                row[costo_post_col] = row.get(costo_col, np.nan)

            if pd.notna(row.get(costo_post_col)):
                row[costo_post_col] = row[costo_post_col] * (1 - porcentaje)

    return row

def limpiar_valor(val):
    """
    Recibe val (puede ser str, int, float, etc.).
    - Si es string, quita '$' y puntos de miles, luego lo convierte a float.
    - Si ya es numérico, lo devuelve tal cual.
    - Si no puede, devuelve NaN.

    Esta función presenta problemas en la práctica con los excel que se me entrega, por precaución, recordar eliminar los caracteres raros en los números manualmente en el excel.
    """
    
    if pd.isna(val):
        return np.nan
    if isinstance(val, str):
        # Quitar signo de peso y puntos
        limpio = re.sub(r"[^\d\-]", "", val)
        try:
            return float(limpio)
        except:
            return np.nan
    try:
        return float(val)
    except:
        return np.nan
    
def calcular_costo_final(row):
    """
    Calcula el costo final de una venta sumando los costos de los SKUs.
    
    Lógica:
    - Si existen columnas con prefijo "Costo_post_dcto_", usa esas.
    - Si no existen:
        - Si la forma de entrega es "Mercado Envíos Full", usa "Costo_full_<SKU>".
        - En caso contrario, usa "Costo_<SKU>".

    Parámetros
    ----------
    row : pandas.Series
        Una fila del DataFrame con las columnas de costos y forma de entrega.

    Retorna
    -------
    float
        La suma de los costos encontrados en la fila. Devuelve NaN si no hay valores válidos.
    """
    
    if any(col.startswith("Costo_post_dcto_") for col in row.index):
        prefijo = "Costo_post_dcto_"
    else:
        if row.get("Forma de entrega") == "Mercado Envíos Full":
            prefijo = "Costo_full_"
        else:
            prefijo = "Costo_SKU"

    valores = []
    for col in row.index:
        if col.startswith(prefijo):
            v = limpiar_valor(row[col])
            if not pd.isna(v):
                valores.append(v)

    return sum(valores) if valores else np.nan

# Funciones que se utilizan en el Paso 10, que consta de eliminar ventas a las que no se le encontró algún costo

def detectar_sku_faltante(row, columnas_sku, col_forma_entrega = 'Forma de entrega'):
    """
    Detecta si en una fila existe un SKU con costo faltante.

    Lógica:
    - Si existen columnas con prefijo "Costo_post_dcto_", usa esas.
    - Si no existen:
        - Si la forma de entrega es "Mercado Envíos Full", usa "Costo_full_<SKU>".
        - En caso contrario, usa "Costo_<SKU>".

    Parámetros
    ----------
    row : pandas.Series
        Fila del DataFrame sobre la cual se evaluará la presencia de SKUs y costos.
    columnas_sku : list of str
        Lista con los nombres de las columnas que contienen los SKUs
        (ejemplo: ["SKU_1", "SKU_2", ...]).

    Retorna
    -------
    str
        "SKU faltante" si encuentra un SKU con costo vacío.
        "Sin SKU faltante" en caso contrario.
    """
    
    # 1) ¿Existen columnas post descuento?
    hay_post = any(col.startswith("Costo_post_dcto_") for col in row.index)
    forma = str(row.get(col_forma_entrega, "")).strip()

    if hay_post:
        prefijos = ["Costo_post_dcto_"]
    else:
        if forma == "Mercado Envíos Full":
            prefijos = ["Costo_full_"]
        else:
            # Normal: primero el nuevo esquema "Costo_SKU_", luego fallback "Costo_"
            prefijos = ["Costo_SKU_", "Costo_"]

    for sku_col in columnas_sku:
        sku = row.get(sku_col)
        if pd.notna(sku):
            costo = None
            # prueba en orden los prefijos definidos
            for pref in prefijos:
                col_costo = f"{pref}{sku_col}"
                if col_costo in row.index:
                    costo = row.get(col_costo)
                    break
            # si no encontró columna o el valor es NaN -> faltante
            if pd.isna(costo):
                return "SKU faltante"

    return "Sin SKU faltante"


# Funciones que se utilizan en el duodécimo paso del análisis de márgenes (antes llamado Paso 11, que consta del cálculo de márgenes)

def clasificar_precio(valor):
    """
    Clasifica la venta en rangos dependiendo del ingreso bruto al cual se vendieron.
    MUY IMPORTANTE: PRECIO BRUTO, NO NETO.

    Argumentos:
    valor (int): el ingreso por venta bruto.
    Retorna:
    str: la clasificación por rango de la venta de acuerdo al ingreso bruto generado.
    """
    
    if 0 <= valor <= 19989:
        return '01 - $0-$19989'
    elif 19990 <= valor <= 79999:
        return '02 - $19990-$79999'
    elif 80000 <= valor <= 149999:
        return '03 - $80000-$149999'
    elif valor >= 150000:
        return '04 - $150000 o más'