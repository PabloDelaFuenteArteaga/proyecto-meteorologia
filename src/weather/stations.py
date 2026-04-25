import meteostat as ms


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


