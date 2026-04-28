from weather.utils import puntos_latitud_longitud


class TestUtils:
    def test_puntos_latitud_longitud_formato(self):
        # 1. Preparación: Creamos datos de prueba manuales
        # (Simulamos un DataFrame o un diccionario con las columnas necesarias)
        estaciones_fake = {
            "latitude": [40.4167, 41.3833, 37.3833],
            "longitude": [-3.7033, 2.1833, -5.9833],
        }

        # 2. Ejecución: Llamamos a la función
        # Como la función devuelve un objeto 'zip' (un iterador),
        # lo convertimos a lista para poder inspeccionarlo.
        resultado = puntos_latitud_longitud(estaciones_fake)
        lista_puntos = list(resultado)

        # 3. Verificaciones (Assertions)

        # ¿El número de puntos coincide con la entrada?
        assert len(lista_puntos) == 3

        # ¿El primer punto es (Longitud, Latitud)?
        # IMPORTANTE: Tu función hace zip(longitudes, latitudes)
        punto_madrid = lista_puntos[0]
        assert punto_madrid[0] == -3.7033  # Longitud
        assert punto_madrid[1] == 40.4167  # Latitud

        # Verificamos el tipo de dato de los elementos
        assert isinstance(punto_madrid, tuple)

    def test_puntos_latitud_longitud_vacio(self):
        """Verifica que no explote si le pasamos datos vacíos."""
        estaciones_vacias = {"latitude": [], "longitude": []}
        resultado = list(puntos_latitud_longitud(estaciones_vacias))

        assert len(resultado) == 0
