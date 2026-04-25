import geopandas as gpd
from shapely.geometry import Point


def celsius_to_fahrenheit(temp_c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit.

    Args:
        temp_c: The temperature in degrees Celsius.

    Returns:
        The temperature in degrees Fahrenheit.
    """
    return (temp_c * 9 / 5) + 32

def puntos_latitud_longitud(estaciones):

    latitudes, longitudes = [], []

    for latitud in estaciones["latitude"]:
        latitudes.append(latitud)

    for longitud in estaciones["longitude"]:
        longitudes.append(longitud)

    puntos = zip(longitudes, latitudes)

    return puntos

def crear_geodf(puntos):
    return gpd.GeoDataFrame(
        geometry=[Point(p) for p in puntos],
        crs="EPSG:4326"
    )
