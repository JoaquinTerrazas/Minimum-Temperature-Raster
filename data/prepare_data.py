# prepare_data.py — Recorta tmin_raster.tif a Perú usando shapefile distrital
from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.mask import mask

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SHAPE_PATH = DATA / "shape_file" / "DISTRITOS.shp"
RASTER_IN = DATA / "tmin_raster.tif"            # raster original
RASTER_OUT = DATA / "tmin_raster_peru.tif"      # raster recortado

if not RASTER_IN.exists():
    raise FileNotFoundError(f"No existe {RASTER_IN}")

# Cargar shapefile y disolver a un polígono único de Perú
gdf = gpd.read_file(SHAPE_PATH)
geom_peru = gdf.geometry.unary_union
geoms = [geom_peru.__geo_interface__]

# Recorte del raster
with rasterio.open(RASTER_IN) as src:
    out_image, out_transform = mask(src, geoms, crop=True, nodata=-9999)
    out_meta = src.meta.copy()

out_meta.update({
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform,
    "nodata": -9999
})

with rasterio.open(RASTER_OUT, "w", **out_meta) as dest:
    dest.write(out_image)

print("✅ Recorte listo en:", RASTER_OUT)
