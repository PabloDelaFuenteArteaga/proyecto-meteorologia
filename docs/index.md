# Clustering de Regiones Climáticas Homogéneas en la Península Ibérica

Línea 6: este proyecto aplica técnicas de **aprendizaje no supervisado** (k-means, DBSCAN y clustering 
jerárquico) a series temporales meteorológicas para identificar y cartografiar regiones climáticas con 
comportamiento similar.

# Autor
Pablo De la Fuente Arteaga.

## Fuente de datos
Datos históricos de estaciones meteorológicas y/o puntos de malla de la península ibérica, incluyendo 
variables como temperatura, precipitación, humedad y viento.

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
