import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


def puntos_latitud_longitud(estaciones):
    """.

    Args:

    Returns:
    """

    latitudes, longitudes = [], []

    for latitud in estaciones["latitude"]:
        latitudes.append(latitud)

    for longitud in estaciones["longitude"]:
        longitudes.append(longitud)

    puntos = zip(longitudes, latitudes)

    return puntos


def crear_geodf(puntos):
    return gpd.GeoDataFrame(geometry=[Point(p) for p in puntos], crs="EPSG:4326")


def mapa(df):

    puntos = puntos_latitud_longitud(df)
    gdf_estaciones = crear_geodf(puntos)

    # Carga del mapa base (URL robusta de Natural Earth)
    # Esta URL apunta al archivo .json crudo (raw)
    url_mapa = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
    world = gpd.read_file(url_mapa)

    # 3. Filtrado del fondo
    # Filtramos España y Portugal para que el mapa no pese y se vea bien
    peninsula = world[world["NAME"].isin(["Spain", "Portugal"])]

    # 4. REPRESENTACIÓN (El orden importa)
    fig, ax = plt.subplots(figsize=(12, 10))

    # Primero dibujamos la península (EL FONDO)
    peninsula.plot(ax=ax, color="#E5E5E5", edgecolor="#999999", zorder=1)

    # Después dibujamos tus estaciones (ENCIMA)
    gdf_estaciones.plot(
        ax=ax,
        marker="o",
        color="red",
        markersize=25,
        alpha=0.6,
        zorder=2,
        label=f"Estaciones ({len(df)})",
    )

    # 5. AJUSTE DE LÍMITES (Zoom a la Península)
    # Si no ponemos esto, el mapa podría verse muy lejos
    ax.set_xlim([-10, 5])
    ax.set_ylim([35, 44.5])

    # Estética
    plt.title("Estaciones Meteorológicas - Península Ibérica", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.show()
