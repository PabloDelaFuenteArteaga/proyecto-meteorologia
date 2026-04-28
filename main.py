from datetime import datetime

import polars as pl

from weather import calidad_clustering, clustering, features, stations, utils

df_ib = stations.estaciones_iberia()

utils.mapa(df_ib)

ids = stations.obtencion_ids(stations.estaciones_iberia())

datos = stations.datos_diarios_estacion(
    ids, datetime(2010, 1, 1), datetime(2023, 12, 31)
)

# Limpiar datos
datos = stations.limpiar_datos_meteorologicos(datos)

"""
print(datos.head(40))
print(f"\nNAs restantes:\n{datos.isnull().sum()}")
"""

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
