import matplotlib.pyplot as plt
import pandas as pd


def visualizacion_estacion(id, datos):
    """
    Visualiza temperatura y precipitación de una estación específica.

    Args:
        id (str): Identificador de la estación.
        datos (pd.DataFrame): DataFrame con datos meteorológicos.
    """

    # Filtrar por estación
    datos_estacion = datos[datos["station_id"] == id].copy()

    if datos_estacion.empty:
        print(f"No hay datos para la estación {id}")
        return

    datos_estacion["time"] = pd.to_datetime(datos_estacion["time"])
    datos_estacion = datos_estacion.set_index("time")

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Temperatura
    axes[0].plot(
        datos_estacion.index,
        datos_estacion["temp"],
        color="red",
        linewidth=2,
        label="Media",
    )
    axes[0].fill_between(
        datos_estacion.index, datos_estacion["tmax"], datos_estacion["tmin"], alpha=0.3
    )
    axes[0].set_title(f"Temperatura - Estación {id}", fontweight="bold")
    axes[0].set_ylabel("°C")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Precipitación
    axes[1].bar(
        datos_estacion.index, datos_estacion["prcp"], color="steelblue", alpha=0.7
    )
    axes[1].set_title("Precipitación", fontweight="bold")
    axes[1].set_ylabel("mm")
    axes[1].grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.show()
