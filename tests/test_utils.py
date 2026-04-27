import numpy as np

from weather.clustering import clustering_dbscan


class test_clustering:
    def test_dbscan_labels():
        X = np.random.rand(50, 2)

        labels = clustering_dbscan(X, eps=0.5)

        assert len(labels) == 50
