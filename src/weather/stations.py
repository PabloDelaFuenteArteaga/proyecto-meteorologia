import meteostat as ms
import pandas as pd


def estaciones_iberia(punto_partida):
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

    # Prácticamente todas las estaciones a nivel mundial
    estaciones = ms.stations.nearby(punto_partida,
                                    radius=50000000, limit=200000).reset_index()
    # Filtramos a las estaciones ibéricas
    estaciones_ib = estaciones[((estaciones["country"] == "ES") | (estaciones["country"] == "PT")) # España y Portugal
                                & (estaciones["region"] != "CN") # Sin Canarias
                                & (estaciones["region"] != "CE") # Sin Ceuta
                                & (estaciones["region"] != "ML") # Sin Melilla
                                & (estaciones["region"].notna())]

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
    return estaciones["id"].tolist()

# Para obtener datos de más de 3 años
ms.config.block_large_requests = False


def datos_diarios_estacion(ids, inicio, fin):
    dfs = []

    for id in ids:
        df = ms.daily(ms.Station(id=id), inicio, fin).fetch()
        df["station_id"] = id
        dfs.append(df)

    return pd.concat(dfs)
