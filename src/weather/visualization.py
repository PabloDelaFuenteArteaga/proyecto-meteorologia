import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy
import sklearn.cluster
from sklearn.metrics import silhouette_score


def evaluar_kmeans(X, k_range=range(2, 11)):
    """
    Evalúa KMeans usando método del codo y silhouette score.
    """

    inertias = []
    silhouettes = []

    for k in k_range:
        km = sklearn.cluster.KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X)

        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X, labels))

    # ---- PLOTS (fuera del loop) ----
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(list(k_range), inertias, marker="o")
    axes[0].set_title("Método del codo")
    axes[0].set_xlabel("K")
    axes[0].set_ylabel("Inercia")

    axes[1].plot(list(k_range), silhouettes, marker="o")
    axes[1].set_title("Silhouette score")
    axes[1].set_xlabel("K")
    axes[1].set_ylabel("Score")

    # K óptimo
    k_opt = list(k_range)[np.argmax(silhouettes)]
    axes[1].axvline(k_opt, linestyle="--", label=f"K óptimo = {k_opt}")
    axes[1].legend()

    plt.tight_layout()
    plt.show()

    return inertias, silhouettes, k_opt


def dendogramas(X):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    linkages_list = ["complete", "single", "average"]
    colors_link = ["#534AB7", "#1D9E75", "#D85A30"]

    for ax, method, color in zip(axes, linkages_list, colors_link):
        Z = scipy.cluster.hierarchy.linkage(X, method=method)
        scipy.cluster.hierarchy.dendrogram(
            Z, ax=ax, color_threshold=0, above_threshold_color=color, leaf_font_size=6
        )
        ax.set_title(f"Linkage: {method}")
        ax.set_xlabel("Muestras")
        ax.set_ylabel("Distancia")

    plt.suptitle("Dendrogramas con distintos linkages", fontsize=13, fontweight="500")
    plt.tight_layout()
    plt.show()


def visualizacion_estacion(id, datos):
    """
    Visualiza temperatura y precipitación de una estación específica.

    Args:
        id (str): Identificador de la estación.
        datos (pd.DataFrame): DataFrame con datos meteorológicos.
    """

    # Filtrar por estación
    datos_estacion = datos[datos['station_id'] == id].copy()

    if datos_estacion.empty:
        print(f"No hay datos para la estación {id}")
        return

    datos_estacion['time'] = pd.to_datetime(datos_estacion['time'])
    datos_estacion = datos_estacion.set_index('time')

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Temperatura
    axes[0].plot(datos_estacion.index, datos_estacion['temp'],
                 color='red', linewidth=2, label='Media')
    axes[0].fill_between(datos_estacion.index, datos_estacion['tmax'],
                         datos_estacion['tmin'], alpha=0.3)
    axes[0].set_title(f'Temperatura - Estación {id}', fontweight='bold')
    axes[0].set_ylabel('°C')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Precipitación
    axes[1].bar(datos_estacion.index, datos_estacion['prcp'],
                color='steelblue', alpha=0.7)
    axes[1].set_title('Precipitación', fontweight='bold')
    axes[1].set_ylabel('mm')
    axes[1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.show()
