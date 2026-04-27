import pandas as pd
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

    # Convertir a Polars si viene de Pandas
    if isinstance(df, pd.DataFrame):
        df = df.reset_index()  # Resetear índice
        df = pl.from_pandas(df)

    # Renombrar si es necesario
    if "time" in df.columns and "date" not in df.columns:
        df = df.rename({"time": "date"})

    df = df.with_columns(
        pl.col("date").dt.month().alias("mes")
    )

    base = df.group_by("station_id").agg([
        pl.col("temp").mean().alias("temp_media"),
        pl.col("temp").std().alias("temp_std"),
        pl.col("prcp").mean().alias("precip_media"),
        pl.col("prcp").quantile(0.9).alias("precip_p90"),
        (pl.col("tmax").max() - pl.col("tmin").min()).alias("amplitud_termica"),
    ])

    # Estacionalidad
    mensual = (
        df.group_by(["station_id", "mes"])
        .agg(pl.col("temp").mean().alias("temp_media_mes"))
    )

    mensual_pivot = mensual.pivot(
        values="temp_media_mes",
        index="station_id",
        columns="mes"
    )

    # Unir todo
    caracteristicas = base.join(mensual_pivot, on="station_id", how="left")

    return caracteristicas
