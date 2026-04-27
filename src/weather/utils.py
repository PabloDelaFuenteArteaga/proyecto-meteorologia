import geopandas as gpd
from shapely.geometry import Point


def puntos_latitud_longitud(estaciones):
    """Convert a temperature from Celsius to Fahrenheit.

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


