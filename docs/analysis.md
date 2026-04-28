# Análisis de Datos y Clustering

## Data Loading & Cleaning
- Para cargar los datos se ha usado la propia librería Meteostat. Para ello se selecciona un punto concreto con la función `ms.Point()` y acto seguido se generan una gran cantidad de estaciones cercanas con la función `ms.stations.nerby()` usando los parámetros de `radius` y `limit`. Una vez obtenidas las estaciones filtramos por las estaciones de España y Portugal exceptuando Canarias y las ciudades autónomas de Ceuta y Melilla. Todo este proceso se ha realizado en una misma función llamada `estaciones_iberia()`.

- Para realizar la limpieza de los datos meteorológicos se ha creado una función llamada `limpiar_datos_meteorologicos()` en la cual se han eliminado 3 columnas con un porcentaje demasido alto de datos faltantes y se han imputado NAs en las variables que contaban con una cantidad moderada de ellos.

## Exploratory Analysis
- Se han calculado distintas métricas para todas las estaciones, función `caracteristicas_climaticas()`, entre ellas la temperatura media de cada estación, la temperatura media de cada uno de los meses (del 1 al 12) de cada estación, la desviación estándar de la temperatura y la precipitación media.

## Results
- Dependiendo de los parámetros elegidos en cada uno de los modelos de clustering (KMeans, DBScan y Jerárquico) se han obtenido diferentes resultados. Para poder visualizarlos debemos analizar la tabla donde comparamos basándonos en las métricas **Silhoutte Score**, **Davies-Bouldin** y **Estabilidad**. Asimismo, es posible analizar la asignación de clusters realizada por cada modelo para cada estación meteorológica.

## Conclusions
- El estudio demuestra que la combinación de métricas estadísticas y estacionales permite crear zonas clímaticas en la península Ibérica de forma automatizada y precisa.
