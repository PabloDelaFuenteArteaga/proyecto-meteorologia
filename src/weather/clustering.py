import numpy as np
import sklearn.cluster


def clustering_k_means(X: np.ndarray, k: int):
    """
    Aplica clustering K-Means a un conjunto de datos.

    El algoritmo K-Means divide los datos en k clusters
    minimizando la varianza intra-cluster.

    Args:
        X (np.ndarray): Matriz de características (n_samples, n_features).
        k (int): Número de clusters a generar.

    Returns:
        labels (np.ndarray): Etiquetas de cluster para cada muestra.
        centroids (np.ndarray): Coordenadas de los centroides de los clusters.
    """
    model = sklearn.cluster.KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10)

    labels = model.fit_predict(X)

    centroids = model.cluster_centers_

    return labels, centroids

def clustering_dbscan(X: np.ndarray, eps: float, min_samples: int = 2, metric: str = "euclidean"):
    """
    Aplica DBSCAN clustering.

    Args:
        X (np.ndarray): Matriz de features
        eps (float): Radio de vecindad
        min_samples (int): Puntos mínimos por cluster
        metric (str): Métrica usada

    Returns:
        labels (np.ndarray): Etiquetas de cluster para cada muestra.
    """
    model = sklearn.cluster.DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric=metric)

    labels = model.fit_predict(X)

    return labels

def clustering_jerarquico(X: np.ndarray, n_clusters: int = 4, linkage: str = "ward"):
    """
    Aplica clustering jerárquico aglomerativo.

    El clustering jerárquico construye una estructura en forma de árbol
    fusionando iterativamente los clusters más similares.

    Args:
        X (np.ndarray): Matriz de características (n_samples, n_features).
        n_clusters (int): Número de clusters finales a generar.
        linkage (str): Método de enlace ('ward', 'complete', 'average').

    Returns:
        labels (np.ndarray): Etiquetas de cluster para cada muestra.
    """
    model = sklearn.cluster.AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage)

    labels = model.fit_predict(X)

    return labels
