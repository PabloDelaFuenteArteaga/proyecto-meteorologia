import meteostat as ms
import pandas as pd


def estaciones_iberia():
    """
    Filtra estaciones meteorológicas en la península ibérica (España y Portugal),
    excluyendo territorios no peninsulares.

    Args:
        punto_partida (ms.Point): Punto geográfico de referencia.

    Returns:
        pandas.DataFrame: Estaciones filtradas.

    Examples:
        >>> punto = ms.Point(40.4, -3.7)
        >>> df = estaciones_iberia(punto)
        >>> isinstance(df, type(estaciones_iberia(punto)))
        True
        >>> set(df["country"].unique()).issubset({"ES", "PT"})
        True
        >>> df["region"].isin(["CN", "CE", "ML"]).any()
        False
    """

    punto_universidad = ms.Point(40.4331476987954, -3.707841790075972)

    # Prácticamente todas las estaciones a nivel mundial
    estaciones = ms.stations.nearby(
        punto_universidad, radius=50000000, limit=200000
    ).reset_index()
    # Filtramos a las estaciones ibéricas
    estaciones_ib = estaciones[
        (
            (estaciones["country"] == "ES") | (estaciones["country"] == "PT")
        )  # España y Portugal
        & (estaciones["region"] != "CN")  # Sin Canarias
        & (estaciones["region"] != "CE")  # Sin Ceuta
        & (estaciones["region"] != "ML")  # Sin Melilla
        & (estaciones["region"].notna())
    ]

    return estaciones_ib


def obtencion_ids(estaciones):
    """
    Extrae los identificadores de estaciones de un DataFrame.

    Args:
        estaciones (pandas.DataFrame): DataFrame con columna 'id'.

    Returns:
        list: Lista de identificadores de estaciones.

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"id": ["A", "B", "C"]})
        >>> obtencion_ids(df)
        ['A', 'B', 'C']
    """
    return estaciones["id"].to_list()


# Para obtener datos de más de 3 años
ms.config.block_large_requests = False


def limpiar_datos_meteorologicos(datos):
    """
    Limpia datos meteorológicos eliminando columnas con demasiados NAs
    y rellenando los NAs residuales de forma inteligente.

    Args:
        datos (pandas.DataFrame): DataFrame con datos meteorológicos.

    Returns:
        pandas.DataFrame: DataFrame limpio sin NAs problemáticos.

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     "temp": [1.0, 2.0, 3.0],
        ...     "snwd": [None, None, None],
        ...     "prcp": [0.0, None, 1.5]
        ... })
        >>> df_limpio = limpiar_datos_meteorologicos(df)
        >>> df_limpio.isnull().sum().sum() == 0
        True
    """

    datos = datos.copy()

    # Columnas a eliminar (>70% NAs)
    columnas_eliminar = ["snwd", "wpgt", "tsun"]
    datos = datos.drop(
        columns=[col for col in columnas_eliminar if col in datos.columns]
    )

    # Convertir a float64 SOLO las columnas numéricas (excluyendo station_id)
    columnas_numericas = datos.select_dtypes(include=["number"]).columns
    datos[columnas_numericas] = datos[columnas_numericas].astype("float64")

    # Rellenar NAs residuales
    if "rhum" in datos.columns:
        datos["rhum"] = datos["rhum"].fillna(datos["rhum"].mean())

    if "prcp" in datos.columns:
        datos["prcp"] = datos["prcp"].fillna(0)

    return datos


def datos_diarios_estacion(ids, inicio, fin):
    dfs = []

    for id in ids:
        df = ms.daily(ms.Station(id=id), inicio, fin).fetch()

        if df is None or df.empty:
            continue

        df["station_id"] = id
        dfs.append(df)

    if not dfs:
        raise ValueError("No se han encontrado datos para ninguna estación")

    return pd.concat(dfs)
