from datetime import datetime

import meteostat as ms
import pandas as pd
import polars as pl

import src.weather.calidad_clustering as calidad_clustering
import src.weather.clustering as clustering
import src.weather.features as features
import src.weather.stations as stations
import src.weather.utils as utils
import src.weather.visualization as visualization

df_ib = stations.estaciones_iberia()

utils.mapa(df_ib)

ids = stations.obtencion_ids(stations.estaciones_iberia())

# Para obtener datos de más de 3 años
ms.config.block_large_requests = False

datos = stations.datos_diarios_estacion(
    ids, datetime(2010, 1, 1), datetime(2023, 12, 31)
)

# Limpiar datos
datos = stations.limpiar_datos_meteorologicos(datos)

datos = datos.reset_index()

# Convertir a Polars
datos_polars = pl.from_pandas(datos)

# Ahora pasa el DataFrame de Polars
caracteristicas = features.caracteristicas_climaticas(datos_polars)
print(caracteristicas)

print(f"LOS DATOS SON: \n\n {datos_polars}")
print(caracteristicas.columns)
print(caracteristicas.shape)
print(caracteristicas.describe())

print("\n" + "=" * 50)
print("ANÁLISIS DE CARACTERÍSTICAS CLIMÁTICAS")
print("=" * 50)
print(caracteristicas)

# CLUSTERING
print("\n" + "=" * 50)
print("PREPARANDO DATOS PARA CLUSTERING")
print("=" * 50)

# Convertir a pandas y preparar matriz X
caracteristicas_pd = caracteristicas.to_pandas().dropna()

ids_limpios = caracteristicas_pd["station_id"].tolist()

# Excluir la columna station_id y usar solo features numéricas
X = caracteristicas_pd.drop(columns=["station_id"]).values

print(f"Matriz de características: {X.shape}")
print(f"Número de estaciones: {len(ids)}")


print("\n-----------VISUALIZACIÓN DE UNA ESTACIÓN-----------")
id_elegido = input(
    f"Los ids disponibles son: \n {ids_limpios} \n\nEliga uno por favor: "
)

visualization.visualizacion_estacion(id_elegido, datos)


datos_id = datos[datos["station_id"] == id_elegido]

# Llamamos a la función
caracteristicas_una = features.caracteristicas_climaticas(datos_id)

print(f"\n-----------MÉTRICAS DE LA ESTACIÓN - {id_elegido}-----------")
print(caracteristicas_una)
for columna in caracteristicas_una.columns:
    print(f"{columna}: {caracteristicas_una[columna][0]}")
print()


comparativa = []

# --- 1. K-MEANS ---
res_km = clustering.clustering_kmeans(X, ids_limpios)
est_km = calidad_clustering.obtener_estabilidad(
    X, clustering.clustering_kmeans, ids_limpios, res_km["parametros"]
)

comparativa.append(
    {
        "Modelo": "K-Means",
        "Silhouette": calidad_clustering.obtener_silhouette(X, res_km["labels"]),
        "Davies-Bouldin": calidad_clustering.obtener_davies_bouldin(
            X, res_km["labels"]
        ),
        "Estabilidad": est_km,
    }
)

# --- 2. DBSCAN ---
res_db = clustering.clustering_dbscan(X, ids_limpios)

comparativa.append(
    {
        "Modelo": "DBSCAN",
        "Silhouette": calidad_clustering.obtener_silhouette(X, res_db["labels"]),
        "Davies-Bouldin": calidad_clustering.obtener_davies_bouldin(
            X, res_db["labels"]
        ),
        "Estabilidad": 0.0,
    }
)

# --- 3. JERÁRQUICO ---
res_jer = clustering.clustering_jerarquico(X, ids_limpios)
est_jer = calidad_clustering.obtener_estabilidad(
    X, clustering.clustering_jerarquico, ids_limpios, res_jer["parametros"]
)

comparativa.append(
    {
        "Modelo": "Jerárquico",
        "Silhouette": calidad_clustering.obtener_silhouette(X, res_jer["labels"]),
        "Davies-Bouldin": calidad_clustering.obtener_davies_bouldin(
            X, res_jer["labels"]
        ),
        "Estabilidad": est_jer,
    }
)

# --- RESUMEN DE ASIGNACIÓN DE CLUSTERS ---
print("\n" + "=" * 70)
print("COMPOSICIÓN DE LOS CLUSTERS POR MÉTODO")
print("=" * 70)

df_clusters = pd.DataFrame(
    {
        "station_id": ids_limpios,
        "K-Means": res_km["labels"],
        "DBSCAN": res_db["labels"],
        "Jerárquico": res_jer["labels"],
    }
)

print(df_clusters)

# --- TABLA FINAL ---
print("\n" + "=" * 70)
print(
    f"{'ALGORITMO':<15} | {'SILHOUETTE':<12} | {'D-BOULDIN':<12} | {'ESTABILIDAD':<12}"
)
print("-" * 70)
for m in comparativa:
    print(
        f"{m['Modelo']:<15} | {m['Silhouette']:<12.4f} | {m['Davies-Bouldin']:<12.4f} | {m['Estabilidad']:<12.4f}"
    )
print("=" * 70)
