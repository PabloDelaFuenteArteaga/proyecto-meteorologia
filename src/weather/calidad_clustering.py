import numpy as np
from sklearn.metrics import adjusted_rand_score, davies_bouldin_score, silhouette_score
from sklearn.utils import resample


def obtener_silhouette(X, labels):
    # Filtramos ruido (-1) para que no rompa la métrica
    mask = labels != -1
    if len(np.unique(labels[mask])) < 2:
        return 0.0

    return silhouette_score(X[mask], labels[mask])


def obtener_davies_bouldin(X, labels):
    mask = labels != -1
    if len(np.unique(labels[mask])) < 2:
        return float("inf")

    return davies_bouldin_score(X[mask], labels[mask])


def obtener_estabilidad(X, func_clustering, nombres, params, n_iter=3):
    indices = np.arange(len(X))
    scores = []

    # Resultado original para comparar
    res_orig = func_clustering(X, nombres, **params)
    labels_orig = res_orig["labels"]

    for i in range(n_iter):
        # Tomamos el 80% de los datos al azar
        idx_sub = resample(
            indices, n_samples=int(len(X) * 0.8), random_state=i, replace=False
        )
        res_sub = func_clustering(X[idx_sub], nombres, **params)

        # Comparamos estabilidad con ARI
        score = adjusted_rand_score(labels_orig[idx_sub], res_sub["labels"])
        scores.append(score)

    return np.mean(scores)
