<<<<<<< HEAD
# 🌡️ Minimum Temperature Raster — Zonal Stats Perú

## 📌 Descripción
Este proyecto analiza temperaturas mínimas (Tmin) a nivel distrital en Perú, usando un raster GeoTIFF (tmin_raster.tif) y límites administrativos (shapefile distrital). Se generan estadísticas zonales, visualizaciones y propuestas de política pública frente a friajes y heladas.

## 📂 Estructura del repositorio
```
Minimum-Temperature-Raster/
├── app/                        # Streamlit app
│   ├── estimation.py          # carga de datos y filtros
│   ├── plot.py                # funciones de gráficos
│   └── streamlit_app.py       # interfaz principal de la app
├── data/
│   ├── tmin_raster.tif        # raster original (opcional)
│   ├── tmin_raster_peru.tif   # raster recortado a Perú
│   ├── tmin_zstats_distrito.csv # métricas por distrito (exportadas)
│   └── shape_file/            # shapefile distrital (shp, dbf, shx, prj)
├── notebooks/                 # Notebook con EDA y cálculo de zonal stats
│   └── tmin_analysis.ipynb
├── requirements.txt           # dependencias de Python
└── README.md                  # este archivo
```

## 🔧 Reproducibilidad

### 1. Crear entorno
```bash
conda create -n tmin python=3.10
conda activate tmin
pip install -r requirements.txt
```

### 2. Preparar datos
El raster original (tmin_raster.tif) se recorta al territorio peruano usando:
```bash
python data/prepare_data.py
```
Esto genera `data/tmin_raster_peru.tif`.

### 3. Calcular estadísticas
Ejecutar el notebook en `/notebooks`:
- Clip del raster.
- Cálculo de métricas zonales (mean, min, max, std, p10, p90, frost_share).
- Exportación a `tmin_zstats_distrito.csv`.
- Generación de gráficos (histograma, ranking, mapa).

### 4. Ejecutar la aplicación
```bash
streamlit run app/streamlit_app.py
```

## 📊 Entregables
- **Zonal Stats**: `tmin_zstats_distrito.csv` (por distrito, todas las bandas).
- **Visualizaciones**:
  - Histograma con mediana/p10/p90.
  - Ranking Top/Bottom 15 (tabla + gráfico).
  - Mapa estático (choropleth).
- **App pública de Streamlit**: interfaz con filtros, descargas y diagnóstico.
- **Políticas públicas**: sección con diagnóstico y 3 medidas priorizadas.

## 🏛️ Políticas públicas (ejemplo)

### Vivienda térmica / ISUR
- **Objetivo**: reducir IRA/ILI en población vulnerable.
- **Población objetivo**: ~25,000 hogares altoandinos.
- **Costo estimado**: S/ 8,000 por hogar → total ~S/ 200 millones.
- **KPI**: −20% casos ARI en MINSA/ESSALUD.

### Refugios y kits antiheladas para ganado
- **Objetivo**: disminuir mortalidad de alpacas y pérdidas agropecuarias.
- **Población objetivo**: 50,000 productores pecuarios.
- **Costo estimado**: S/ 500 por kit → total ~S/ 25 millones.
- **KPI**: −30% mortalidad de alpacas reportada.

### Calendarios agrícolas + alertas tempranas
- **Objetivo**: anticipar friajes en Amazonía y ajustar actividades.
- **Población objetivo**: 1,000 escuelas y 500 centros de salud en Loreto/Ucayali.
- **Costo estimado**: S/ 10,000 por centro → total ~S/ 15 millones.
- **KPI**: +15% asistencia escolar en meses críticos.

## 🚀 Despliegue
La aplicación puede ejecutarse en Streamlit Community Cloud:
👉 [Abrir app en línea](TU-LINK) (reemplazar `<TU-LINK>` con la URL de tu despliegue en Streamlit Cloud).

## 📑 Fuente de datos
- **Raster Tmin**: [especificar fuente oficial] (°C, 5 bandas = 5 periodos).
- **Shapefile distrital**: INEI / IGN (UBIGEO).

## 📜 Licencia
Uso académico dentro del curso de Data Science con Python.
 
=======
🌡️ Minimum Temperature Raster — Zonal Stats Perú
📌 Descripción

Este proyecto analiza temperaturas mínimas (Tmin) a nivel distrital en Perú, usando un raster GeoTIFF (tmin_raster.tif) y límites administrativos (shapefile distrital).
Se generan estadísticas zonales, visualizaciones y propuestas de política pública frente a friajes y heladas.

📂 Estructura del repositorio
Minimum-Temperature-Raster/
├── app/                     # Streamlit app
│   ├── estimation.py        # carga de datos y filtros
│   ├── plot.py              # funciones de gráficos
│   └── streamlit_app.py     # interfaz principal de la app
├── data/                    
│   ├── tmin_raster.tif          # raster original (opcional)
│   ├── tmin_raster_peru.tif     # raster recortado a Perú
│   ├── tmin_zstats_distrito.csv # métricas por distrito (exportadas)
│   └── shape_file/              # shapefile distrital (shp, dbf, shx, prj)
├── notebooks/               # Notebook con EDA y cálculo de zonal stats
│   └── tmin_analysis.ipynb
├── requirements.txt         # dependencias de Python
└── README.md                # este archivo

🔧 Reproducibilidad
1. Crear entorno
conda create -n tmin python=3.10
conda activate tmin
pip install -r requirements.txt

2. Preparar datos

El raster original (tmin_raster.tif) se recorta al territorio peruano usando:

python data/prepare_data.py


Esto genera data/tmin_raster_peru.tif.

3. Calcular estadísticas

Ejecutar el notebook en /notebooks:

Clip del raster.

Cálculo de métricas zonales (mean, min, max, std, p10, p90, frost_share).

Exportación a tmin_zstats_distrito.csv.

Generación de gráficos (histograma, ranking, mapa).

4. Ejecutar la aplicación
streamlit run app/streamlit_app.py

📊 Entregables

Zonal Stats: tmin_zstats_distrito.csv (por distrito, todas las bandas).

Visualizaciones:

Histograma con mediana/p10/p90.

Ranking Top/Bottom 15 (tabla + gráfico).

Mapa estático (choropleth).

App pública de Streamlit: interfaz con filtros, descargas y diagnóstico.

Políticas públicas: sección con diagnóstico y 3 medidas priorizadas.

🏛️ Políticas públicas (ejemplo)

Vivienda térmica / ISUR

Objetivo: reducir IRA/ILI en población vulnerable.

Población objetivo: ~25,000 hogares altoandinos.

Costo estimado: S/ 8,000 por hogar → total ~S/ 200 millones.

KPI: −20% casos ARI en MINSA/ESSALUD.

Refugios y kits antiheladas para ganado

Objetivo: disminuir mortalidad de alpacas y pérdidas agropecuarias.

Población objetivo: 50,000 productores pecuarios.

Costo estimado: S/ 500 por kit → total ~S/ 25 millones.

KPI: −30% mortalidad de alpacas reportada.

Calendarios agrícolas + alertas tempranas

Objetivo: anticipar friajes en Amazonía y ajustar actividades.

Población objetivo: 1,000 escuelas y 500 centros de salud en Loreto/Ucayali.

Costo estimado: S/ 10,000 por centro → total ~S/ 15 millones.

KPI: +15% asistencia escolar en meses críticos.

🚀 Despliegue

La aplicación puede ejecutarse en Streamlit Community Cloud:

👉 Abrir app en línea

(reemplazar <TU-LINK> con la URL de tu despliegue en Streamlit Cloud).

📑 Fuente de datos

Raster Tmin: [especificar fuente oficial] (°C, 5 bandas = 5 periodos).

Shapefile distrital: INEI / IGN (UBIGEO).

📜 Licencia

Uso académico dentro del curso de Data Science con Python.
>>>>>>> 037338b494f82c4d40a40c2c242ec6cdbf6fb30e
