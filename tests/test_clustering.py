from unittest.mock import patch

import numpy as np

from src.weather import clustering


class TestClustering:
    def _generar_datos_prueba(self):
        """Genera una matriz X de 10 muestras y 2 características."""
        # Creamos dos grupos de puntos claramente separados
        grupo1 = np.random.normal(loc=0, scale=0.5, size=(5, 2))
        grupo2 = np.random.normal(loc=5, scale=0.5, size=(5, 2))
        return np.vstack([grupo1, grupo2])

    def test_clustering_kmeans_con_parametros(self):
        X = self._generar_datos_prueba()
        nombres = [f"Estacion_{i}" for i in range(10)]

        # Pasamos k=2 directamente (esto evita el input())
        resultado = clustering.clustering_kmeans(X, nombres, k=2)

        assert resultado["metodo"] == "K-Means"
        assert resultado["parametros"]["k"] == 2
        assert len(resultado["labels"]) == 10
        # Verificamos que haya etiquetas de clusters (0 y 1)
        assert set(resultado["labels"]).issubset({0, 1})

    def test_clustering_dbscan_con_parametros(self):
        X = self._generar_datos_prueba()
        nombres = [f"Estacion_{i}" for i in range(10)]

        # Pasamos eps y min_samples directamente
        resultado = clustering.clustering_dbscan(X, nombres, eps=0.5, min_samples=2)

        assert resultado["metodo"] == "DBSCAN"
        assert resultado["parametros"]["eps"] == 0.5
        assert len(resultado["labels"]) == 10

    def test_clustering_jerarquico_con_parametros(self):
        X = self._generar_datos_prueba()
        nombres = [f"Estacion_{i}" for i in range(10)]

        # Pasamos n_clusters y linkage directamente
        resultado = clustering.clustering_jerarquico(
            X, nombres, n_clusters=2, linkage="ward"
        )

        assert resultado["metodo"] == "Jerárquico"
        assert resultado["parametros"]["linkage"] == "ward"
        assert len(resultado["labels"]) == 10

    def test_kmeans_simulando_input(self):
        """Test para verificar que funciona incluso si el usuario tiene que escribir."""
        X = self._generar_datos_prueba()
        nombres = [f"Estacion_{i}" for i in range(10)]

        # 'patch' intercepta el input() y devuelve "2" automáticamente
        with patch("builtins.input", return_value="2"):
            resultado = clustering.clustering_kmeans(X, nombres, k=None)

        assert resultado["parametros"]["k"] == 2
        assert resultado["metodo"] == "K-Means"
