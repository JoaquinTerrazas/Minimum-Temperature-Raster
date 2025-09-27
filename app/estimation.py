from pathlib import Path  # rutas relativas robustas
import pandas as pd       # tablas/CSV
import geopandas as gpd   # vectores (shapefile)
import unicodedata        # quitar tildes en nombres

# Rutas relativas
ROOT = Path(__file__).resolve().parents[1]          # raíz del repo
DATA = ROOT / "data"                                # carpeta data
CSV_MASTER = DATA / "tmin_zstats_distrito.csv"      # CSV maestro (salida del notebook)
SHAPE_PATH = DATA / "shape_file" / "DISTRITOS.shp"  # shapefile distrital

def quitar_tildes(s: str) -> str:
    """Normaliza a MAYÚSCULAS sin tildes (para nombres)."""
    if pd.isna(s): 
        return s
    s = str(s).upper()
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("ASCII")

def load_data():
    """Carga CSV maestro y shapefile; retorna df (stats), gdf (geometrías), bandas y departamentos."""
    if not CSV_MASTER.exists():
        raise FileNotFoundError(f"No existe {CSV_MASTER}. Genera el CSV desde el notebook.")
    if not SHAPE_PATH.exists():
        raise FileNotFoundError(f"No existe {SHAPE_PATH}. Versiona el shapefile completo (.shp/.dbf/.shx/.prj).")

    # Cargar CSV maestro (todas las bandas/metricas por distrito)
    df = pd.read_csv(CSV_MASTER)
    df["__UBIGEO__"] = df["__UBIGEO__"].astype(str).str.zfill(6)     # UBIGEO estándar de 6 dígitos
    df["__NOMBRE__"] = df["__NOMBRE__"].apply(quitar_tildes)         # nombre sin tildes

    # Cargar shapefile para traer Departamento y geometría
    gdf = gpd.read_file(SHAPE_PATH, engine="pyogrio")

    # Campos de tu shapefile (ajustados a lo que hallamos): IDDIST=UBIGEO ; DEPARTAMEN=Departamento
    FIELD_UBIGEO = "IDDIST"
    FIELD_DEP = "DEPARTAMEN"

    # Mapeo UBIGEO -> Departamento (normalizado)
    map_dep = (
        gdf[[FIELD_UBIGEO, FIELD_DEP]]
        .rename(columns={FIELD_UBIGEO: "__UBIGEO__", FIELD_DEP: "__DEP__"})
        .assign(
            __UBIGEO__=lambda x: x["__UBIGEO__"].astype(str).str.zfill(6),
            __DEP__=lambda x: x["__DEP__"].apply(quitar_tildes),
        )
        .drop_duplicates(subset="__UBIGEO__")
    )
    # Unir Departamento al CSV maestro (para filtrar en la UI)
    df = df.merge(map_dep, on="__UBIGEO__", how="left")

    # Listas para controles
    bands = sorted(df["band_label"].dropna().unique().tolist())         # periodos/bandas disponibles
    deps = sorted(df["__DEP__"].dropna().unique().tolist())             # departamentos disponibles

    return df, gdf, bands, deps

def filter_df(df: pd.DataFrame, gdf: gpd.GeoDataFrame, band_sel: str, dep_sel: str | None):
    """Aplica filtros por banda y departamento. Devuelve df filtrado y gdf listo para mapa."""
    df_band = df[df["band_label"] == band_sel].copy()                   # filtra periodo
    if dep_sel and dep_sel != "TODOS":
        df_band = df_band[df_band["__DEP__"] == dep_sel].copy()         # filtra departamento

    # Preparar GeoDataFrame para mapa (unión por UBIGEO)
    FIELD_UBIGEO = "IDDIST"
    FIELD_DEP = "DEPARTAMEN"
    gdf_map = (
        gdf[[FIELD_UBIGEO, FIELD_DEP, "geometry"]]
        .rename(columns={FIELD_UBIGEO: "__UBIGEO__", FIELD_DEP: "__DEP__"})
        .assign(
            __UBIGEO__=lambda x: x["__UBIGEO__"].astype(str).str.zfill(6),
            __DEP__=lambda x: x["__DEP__"].apply(quitar_tildes),
        )
        .merge(df_band[["__UBIGEO__", "mean", "p10", "p90", "std", "min", "max", "frost_share"]],
               on="__UBIGEO__", how="inner")
    )
    return df_band, gdf_map

def df_to_csv_bytes(df: pd.DataFrame, name_hint: str = "table.csv") -> tuple[bytes, str]:
    """Convierte un DataFrame a bytes CSV (para botones de descarga en Streamlit)."""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return csv_bytes, name_hint
