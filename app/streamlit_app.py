from pathlib import Path          # rutas relativas
import numpy as np                # cálculos rápidos
import streamlit as st            # framework UI
from estimation import load_data, filter_df, df_to_csv_bytes  # nuestras utilidades
from plot import plot_distribution, build_rankings, plot_map, plot_ranking_bar # funciones de gráficos

st.set_page_config(page_title="Tmin Perú — Zonal Stats", layout="wide")   # config de página
st.title("Zonal Stats de Temperatura Mínima (Tmin) — Perú")               # título
st.caption("Evidencia para diagnóstico de friaje/heladas — Resultados precalculados (notebook).")  # subtítulo

# =========== Sección 1: Carga de datos ===========
with st.spinner("Cargando datos..."):                     # indicador de carga
    df, gdf, bands, deps = load_data()                    # lee CSV maestro + shapefile
st.sidebar.subheader("Información")
st.sidebar.write(f"Distritos: **{df['__UBIGEO__'].nunique()}**")         # KPI lateral
st.sidebar.write(f"Bandas: **{len(bands)}**")                            # KPI lateral

# =========== Sección 2: Controles ===========
# Selector de periodo (banda)
default_band = bands[-1]                                                  # última banda
band_sel = st.sidebar.selectbox("Periodo (banda)", options=bands, index=len(bands)-1)  # drop-down de bandas

# Selector de departamento (incluye "TODOS")
dep_opts = ["TODOS"] + deps                                               # opciones (TODOS + lista)
dep_sel = st.sidebar.selectbox("Departamento", options=dep_opts, index=0) # drop-down de departamentos

# Umbral de riesgo para p10 (solo para resaltado/kpis, no recalcula frost_share)
thr = st.sidebar.slider("Umbral (°C) para marcar riesgo (p10 < umbral)", -10.0, 10.0, 0.0, 0.5)

# Variable de mapa: mean (por defecto) o p10 (toggle)
use_p10 = st.sidebar.toggle("Usar p10 en el mapa", value=False)           # interruptor
map_var = "p10" if use_p10 else "mean"                                    # decide variable a mapear

# =========== Sección 3: Filtro de datos ===========
df_band, gdf_map = filter_df(df, gdf, band_sel, dep_sel)                  # aplica filtros
n_obs = len(df_band)                                                      # conteo de filas
pct_riesgo = float((df_band["p10"] < thr).mean()*100) if n_obs > 0 else 0.0  # % con p10<thr
mean_mean = float(df_band["mean"].mean()) if n_obs > 0 else np.nan           # promedio de mean
c1, c2, c3 = st.columns(3)                                                # 3 KPIs
c1.metric("Distritos mostrados", n_obs)                                   # KPI 1
c2.metric(f"% con p10 < {thr:.1f} °C", f"{pct_riesgo:.1f}%")              # KPI 2
c3.metric("Promedio de Tmin media (°C)", f"{mean_mean:.1f}" if np.isfinite(mean_mean) else "—")  # KPI 3

# =========== Sección 4: Distribución ===========
st.subheader("Distribución de Tmin media por distrito")
if n_obs == 0:
    st.info("No hay distritos para la selección actual.")                 # mensaje si vacío
else:
    fig1 = plot_distribution(df_band, band_sel, dep_sel)                  # figura histograma+líneas guía
    st.pyplot(fig1)                                                       # render en app
    csv_bytes, fname = df_to_csv_bytes(df_band, f"tmin_stats_{band_sel}_{dep_sel}.csv")  # CSV filtrado
    st.download_button("Descargar tabla filtrada (CSV)", data=csv_bytes, file_name=fname, mime="text/csv")  # botón descarga

# =========== Sección 5: Rankings ===========
st.subheader("Ranking de distritos (Tmin media)")
if n_obs == 0:
    st.info("No hay distritos para la selección actual.")                 # mensaje si vacío
else:
    top, bot = build_rankings(df_band, K=15)                              # tablas top/bottom
    tab1, tab2 = st.tabs(["Top 15 más fríos", "Top 15 más cálidos"])     # pestañas

    with tab1:
        st.dataframe(top, use_container_width=True)                       # muestra top
        d1, n1 = df_to_csv_bytes(top, f"ranking_top15_{band_sel}_{dep_sel}.csv")  # CSV top
        st.download_button("Descargar Top 15 (CSV)", data=d1, file_name=n1, mime="text/csv")  # botón descarga

    with tab2:
        st.dataframe(bot, use_container_width=True)                       # muestra bottom
        d2, n2 = df_to_csv_bytes(bot, f"ranking_bottom15_{band_sel}_{dep_sel}.csv")  # CSV bottom
        st.download_button("Descargar Top 15 cálidos (CSV)", data=d2, file_name=n2, mime="text/csv")  # botón descarga

    with tab1:
        # ... tabla y descarga ya existentes
        fig_top = plot_ranking_bar(top, f"Top 15 distritos más fríos — {band_sel}")
        st.pyplot(fig_top)

    with tab2:
        # ... tabla y descarga ya existentes
        fig_bot = plot_ranking_bar(bot, f"Top 15 distritos más cálidos — {band_sel}", color="tomato")
        st.pyplot(fig_bot)
    

# =========== Sección 6: Mapa estático ===========
st.subheader(f"Mapa estático — Tmin {'p10' if use_p10 else 'mean'}")
if gdf_map.empty:
    st.info("Sin geometrías para la selección actual.")                   # mensaje si vacío
else:
    fig2 = plot_map(gdf_map, map_var, band_sel, dep_sel)                  # figura de mapa
    st.pyplot(fig2)                                                       # render en app

# =========== Sección 7: Políticas públicas ===========
st.header("Políticas Públicas — Diagnóstico y Medidas")
if n_obs == 0:
    st.info("No hay datos para la selección actual.")                     # mensaje si vacío
else:
    n_riesgo = int((df_band["p10"] < thr).sum())                          # conteo distritos en riesgo
    st.markdown(f"""
**Diagnóstico.** En **{dep_sel}** (o país completo) para **{band_sel}**:
- **{n_riesgo}** distritos ({pct_riesgo:.1f}%) con **p10 < {thr:.1f} °C**.
- Tmin media promedio **{mean_mean:.1f} °C**.

**Focalización sugerida:** distritos con `p10 < {thr:.1f} °C` y/o `frost_share` elevado.
""")
    st.markdown("""
**Medidas (plantilla):**
1) **Vivienda térmica / ISUR** — Objetivo: reducir ARI/ILI. Población: hogares altoandinos. KPI: −X% ARI/ILI.
2) **Kits antiheladas y refugios ganaderos** — Objetivo: bajar mortalidad de alpacas/ovinos. KPI: −X% mortalidad.
3) **Calendarios agrícolas + alertas tempranas** — Objetivo: anticipar friajes y ajustar actividades. KPI: +X% asistencia escolar.
""")

# =========== Pie de reproducibilidad ===========
st.markdown("---")
st.caption("""
**Reproducibilidad**: Esta app lee `data/tmin_zstats_distrito.csv` y `data/shape_file/DISTRITOS.shp`.
Para regenerar resultados: ejecutar el notebook (clip → zonal stats → figuras). Versiona `requirements.txt` en la raíz.
""")
