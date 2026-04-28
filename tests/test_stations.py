import pandas as pd

import src.weather.stations as stations


class TestStations:
    def test_obtencion_ids(self):

        df = pd.DataFrame({"id": ["123", "456"], "nombre": ["A", "B"]})

        resultado = stations.obtencion_ids(df)

        assert resultado == ["123", "456"]

    def test_limpiar_datos_meteorologicos(self):

        # Creamos un DF con datos sucios

        df_sucio = pd.DataFrame(
            {
                "temp": [20.0, None, 25.0],
                "snwd": [1.0, 1.0, 1.0],  # Esta columna debe eliminarse
                "prcp": [1.0, None, 5.0],
                "rhum": [50.0, 50.0, None],
            }
        )

        df_limpio = stations.limpiar_datos_meteorologicos(df_sucio)

        assert "snwd" not in df_limpio.columns
        assert df_limpio["prcp"].isnull().sum() == 0
        assert df_limpio["prcp"].iloc[1] == 0  # El NA de prcp debe ser 0
        assert df_limpio["rhum"].iloc[2] == 50.0  # El NA de rhum es la media (50)
