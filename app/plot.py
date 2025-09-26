import io                 # para exportar PNG en memoria si se quiere
import numpy as np        # estadísticas simples
import pandas as pd       # manipulación de tablas
import geopandas as gpd   # choropleth
import matplotlib.pyplot as plt  # gráficos base

def plot_distribution(df_band: pd.DataFrame, band_sel: str, dep_sel: str):
    """Histograma de 'mean' con líneas guía: mediana, p10 y p90. Retorna figura Matplotlib."""
    fig, ax = plt.subplots(figsize=(7, 4))                           # crea figura
    x = df_band["mean"].dropna().values                              # serie de interés
    ax.hist(x, bins=30, density=True, alpha=0.7, label="Histograma") # histograma densidad

    med = float(np.nanmedian(x))                                     # mediana
    p10 = float(np.nanpercentile(x, 10))                              # percentil 10
    p90 = float(np.nanpercentile(x, 90))                              # percentil 90
    ax.axvline(med, color="k", linestyle="--", linewidth=1.5, label=f"Mediana: {med:.1f} °C")  # línea mediana
    ax.axvline(p10, color="gray", linestyle=":", linewidth=1.2, label=f"P10: {p10:.1f} °C")    # línea p10
    ax.axvline(p90, color="gray", linestyle=":", linewidth=1.2, label=f"P90: {p90:.1f} °C")    # línea p90

    ax.set_title(f"Distribución de Tmin media — {band_sel} — {dep_sel}")  # título
    ax.set_xlabel("Tmin media (°C)")                                       # etiqueta eje x
    ax.set_ylabel("Densidad")                                              # etiqueta eje y
    ax.grid(alpha=0.3)                                                     # cuadriculado suave
    ax.legend()                                                            # leyenda
    return fig                                                             # retorna figura

def build_rankings(df_band: pd.DataFrame, K: int = 15):
    """Devuelve (topK_fríos, topK_cálidos) como DataFrames para mostrar/descargar."""
    cols = ["__UBIGEO__", "__NOMBRE__", "__DEP__", "mean", "min", "max", "p10", "p90", "std", "frost_share"]  # columnas a conservar
    top = df_band.sort_values("mean", ascending=True).head(K)[cols].reset_index(drop=True)    # más fríos
    bot = df_band.sort_values("mean", ascending=False).head(K)[cols].reset_index(drop=True)   # más cálidos
    return top, bot

def plot_map(gdf_map: gpd.GeoDataFrame, map_var: str, band_sel: str, dep_sel: str):
    """Choropleth estático de la variable 'map_var' (mean o p10). Retorna figura Matplotlib."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 9))                         # crea figura
    gdf_map.plot(column=map_var, ax=ax, legend=True)                     # choropleth con leyenda
    ax.set_axis_off()                                                    # oculta ejes
    ax.set_title(f"Choropleth • Tmin {map_var} — {band_sel} — {dep_sel}", fontsize=12)  # título
    # Pie de fuente
    plt.annotate("Fuente: CSV maestro pre-calculado + shapefile distrital. Unidades: °C.",
                 xy=(0.5, 0.02), xycoords="figure fraction", ha="center", fontsize=9)
    return fig                                                           # retorna figura

def plot_ranking_bar(df_rank: pd.DataFrame, title: str, color: str = "steelblue"):
    """Bar chart horizontal de distritos según Tmin media. Retorna figura Matplotlib."""
    fig, ax = plt.subplots(figsize=(6, 6))
    df_rank_sorted = df_rank.sort_values("mean", ascending=True)  # ordenar de frío a cálido
    ax.barh(df_rank_sorted["__NOMBRE__"], df_rank_sorted["mean"], color=color)
    ax.set_xlabel("Tmin media (°C)")
    ax.set_title(title)
    plt.tight_layout()
    return fig
