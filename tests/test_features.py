from datetime import datetime

import pandas as pd
import polars as pl

from src.weather.features import caracteristicas_climaticas


class TestFeatures:
    def _generar_datos_polars(self):
        """Genera datos sintéticos para una estación durante 2 meses."""
        return pl.DataFrame(
            {
                "station_id": ["MAD1", "MAD1", "MAD1", "MAD1"],
                "date": [
                    datetime(2023, 1, 1),
                    datetime(2023, 1, 15),
                    datetime(2023, 2, 1),
                    datetime(2023, 2, 15),
                ],
                "temp": [10.0, 12.0, 20.0, 22.0],
                "tmax": [15.0, 17.0, 25.0, 27.0],
                "tmin": [5.0, 7.0, 15.0, 17.0],
                "prcp": [0.0, 10.0, 0.0, 20.0],
            }
        )

    def test_caracteristicas_climaticas_columnas(self):
        df = self._generar_datos_polars()
        resultado = caracteristicas_climaticas(df)

        # Verificar que el resultado es un DataFrame de Polars
        assert isinstance(resultado, pl.DataFrame)

        # Verificar columnas base
        columnas_esperadas = [
            "station_id",
            "temp_media",
            "temp_std",
            "precip_media",
            "precip_p90",
            "amplitud_termica",
        ]
        for col in columnas_esperadas:
            assert col in resultado.columns

        # Verificar que existen las columnas de los meses (1 y 2 en este caso)
        assert "1" in resultado.columns
        assert "2" in resultado.columns

    def test_calculos_logica(self):
        df = self._generar_datos_polars()
        resultado = caracteristicas_climaticas(df)

        # Estación MAD1
        res_mad = resultado.filter(pl.col("station_id") == "MAD1")

        # Amplitud térmica: tmax max (27) - tmin min (5) = 22
        assert res_mad["amplitud_termica"][0] == 22.0

        # Precip media: (0 + 10 + 0 + 20) / 4 = 7.5
        assert res_mad["precip_media"][0] == 7.5

        # Temperatura media del mes 1 (Enero): (10 + 12) / 2 = 11.0
        # Polars nombra las columnas del pivot como strings
        assert res_mad["1"][0] == 11.0

    def test_compatibilidad_pandas(self):
        # Crear un DataFrame de Pandas para probar la conversión interna
        df_pd = pd.DataFrame(
            {
                "station_id": ["BCN1"],
                "time": [
                    datetime(2023, 5, 1)
                ],  # Usamos 'time' para probar el renombrado
                "temp": [25.0],
                "tmax": [30.0],
                "tmin": [20.0],
                "prcp": [5.0],
            }
        )

        resultado = caracteristicas_climaticas(df_pd)

        assert isinstance(resultado, pl.DataFrame)
        assert resultado["station_id"][0] == "BCN1"
        assert "5" in resultado.columns  # Mes de mayo
