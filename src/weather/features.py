import polars as pl


def caracteristicas_climaticas(df: "pl.DataFrame") -> "pl.DataFrame":
    """
    Construye un vector de características climáticas por estación a partir
    de datos diarios meteorológicos.

    Para cada estación, se agregan estadísticas descriptivas que resumen
    el comportamiento climático a lo largo del tiempo.

    Features calculadas:
        - Temperatura media
        - Desviación estándar de temperatura
        - Precipitación media
        - Percentil 90 de precipitación
        - Variabilidad térmica

    Args:
        df (pl.DataFrame): DataFrame de Polars con columnas:
            - station_id (str): identificador de la estacion
            - tavg (float): temperatura media diaria
            - prcp (float): precipitación diaria

    Returns:
        pl.DataFrame: DataFrame con una fila por estación y sus features.

    Example:
        >>> caracteristicas = construir_features_climaticas(df_polars)
        >>> caracteristicas.shape[0]  # número de estaciones
    """

    caracteristicas = df.group_by("station_id").agg([
        pl.col("tavg").mean().alias("temp_media"),
        pl.col("tavg").std().alias("temp_std"),
        pl.col("prcp").mean().alias("precip_media"),
        pl.col("prcp").quantile(0.9).alias("precip_p90"),
        (pl.col("tavg").max() - pl.col("tavg").min()).alias("amplitud_termica"),
    ])

    return caracteristicas
