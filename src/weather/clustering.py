import sklearn


def clustering_kmeans(X, nombres_estaciones, k=None):
    # Si k es None, lo pedimos (para uso manual).
    # Si k ya viene (estabilidad), no preguntamos.
    if k is None:
        k = int(input("¿Cuántos clusters para K-Means?: "))

    model = sklearn.cluster.KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X)
    return {"labels": labels, "metodo": "K-Means", "parametros": {"k": k}}


def clustering_dbscan(X, nombres_estaciones, eps=None, min_samples=None):
    if eps is None or min_samples is None:
        eps = float(input("eps (radio): "))
        min_samples = int(input("min_samples: "))

    model = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    return {
        "labels": labels,
        "metodo": "DBSCAN",
        "parametros": {"eps": eps, "min_samples": min_samples},
    }


def clustering_jerarquico(X, nombres_estaciones, n_clusters=None, linkage=None):
    if n_clusters is None:
        n_clusters = int(input("¿Cuántos clusters? "))
        linkage_opcion = input("Método (1:ward, 2:complete, 3:average): ") or "1"
        linkage = {"1": "ward", "2": "complete", "3": "average"}.get(
            linkage_opcion, "ward"
        )

    model = sklearn.cluster.AgglomerativeClustering(
        n_clusters=n_clusters, linkage=linkage
    )
    labels = model.fit_predict(X)
    return {
        "labels": labels,
        "metodo": "Jerárquico",
        "parametros": {"n_clusters": n_clusters, "linkage": linkage},
    }
