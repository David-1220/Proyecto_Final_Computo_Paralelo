import streamlit as st
import pandas as pd
import plotly.express as px
import ray
import time

# ======================================
# CONFIGURACIÓN
# ======================================

st.set_page_config(
    page_title="Proyecto ATUS - Big Data",
    layout="wide"
)

# ======================================
# TÍTULO
# ======================================

st.title(" Análisis de Accidentes Viales - ATUS 2024")

st.markdown("""
- David Alejandro Pérez González 367759 
- Ana Sofía Ledezma Díaz 367897
- Evelyn Oyuky Torres Alanís 367868
 
- Python - Pandas - Ray - Parquet - Streamlit
""")


# ======================================
# CARGAR DATASET
# ======================================

@st.cache_data
def cargar_datos():

    df = pd.read_parquet(
        "../data/raw/atus_anual_2024.parquet"
    )

    return df

df = cargar_datos()

# ======================================
# DICCIONARIO DE ESTADOS
# ======================================

estados = {
    1: "Aguascalientes",
    2: "Baja California",
    3: "Baja California Sur",
    4: "Campeche",
    5: "Coahuila",
    6: "Colima",
    7: "Chiapas",
    8: "Chihuahua",
    9: "CDMX",
    10: "Durango",
    11: "Guanajuato",
    12: "Guerrero",
    13: "Hidalgo",
    14: "Jalisco",
    15: "Estado de México",
    16: "Michoacán",
    17: "Morelos",
    18: "Nayarit",
    19: "Nuevo León",
    20: "Oaxaca",
    21: "Puebla",
    22: "Querétaro",
    23: "Quintana Roo",
    24: "San Luis Potosí",
    25: "Sinaloa",
    26: "Sonora",
    27: "Tabasco",
    28: "Tamaulipas",
    29: "Tlaxcala",
    30: "Veracruz",
    31: "Yucatán",
    32: "Zacatecas"
}

# CREAR COLUMNA CON NOMBRES

df["ESTADO"] = df["ID_ENTIDAD"].map(estados)

# ======================================
# LIMPIEZA BÁSICA
# ======================================

# Horas válidas
df_horas = df[
    (df["ID_HORA"] >= 0) &
    (df["ID_HORA"] <= 23)
]

# Meses válidos
df_meses = df[
    (df["MES"] >= 1) &
    (df["MES"] <= 12)
]

# ======================================
# MÉTRICAS GENERALES
# ======================================

st.header("Métricas Generales")

# Convertir columnas numéricas
columnas_numericas = [
    "CONDHERIDO",
    "PASAHERIDO",
    "PEATHERIDO",
    "CICLHERIDO",
    "OTROHERIDO",
    "CONDMUERTO",
    "PASAMUERTO",
    "PEATMUERTO",
    "CICLMUERTO",
    "OTROMUERTO"
]

for columna in columnas_numericas:

    df[columna] = pd.to_numeric(
        df[columna],
        errors='coerce'
    ).fillna(0)

# Totales
total_accidentes = len(df)

total_heridos = (
    df["CONDHERIDO"].sum() +
    df["PASAHERIDO"].sum() +
    df["PEATHERIDO"].sum() +
    df["CICLHERIDO"].sum() +
    df["OTROHERIDO"].sum()
)

total_fallecidos = (
    df["CONDMUERTO"].sum() +
    df["PASAMUERTO"].sum() +
    df["PEATMUERTO"].sum() +
    df["CICLMUERTO"].sum() +
    df["OTROMUERTO"].sum()
)

# Mostrar métricas
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Accidentes",
    f"{total_accidentes:,}"
)

col2.metric(
    "Total Heridos",
    f"{int(total_heridos):,}"
)

col3.metric(
    "Total Fallecidos",
    f"{int(total_fallecidos):,}"
)

# Preguntas de analisis
st.header("PREGUNTAS DE ANÁLISIS")


# ======================================
# 1. TOP ESTADOS
# ======================================

st.header("Estados con Más Accidentes")

top_estados = (
    df["ESTADO"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_estados.columns = [
    "Estado",
    "Accidentes"
]

fig_estados = px.bar(
    top_estados,
    x="Estado",
    y="Accidentes",
    title="Top 10 Estados"
)

st.plotly_chart(
    fig_estados,
    use_container_width=True
)

# ======================================
# 2. TOP MUNICIPIOS
# ======================================

st.header("Municipios con Más Accidentes")

top_municipios = (
    df["ID_MUNICIPIO"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_municipios.columns = [
    "Municipio",
    "Accidentes"
]

# TABLA
st.subheader("Tabla Comparativa")

st.dataframe(
    top_municipios,
    use_container_width=True
)

# GRÁFICA
fig_municipios = px.bar(
    top_municipios,
    x="Municipio",
    y="Accidentes",
    title="Top 10 Municipios"
)

st.plotly_chart(
    fig_municipios,
    use_container_width=True
)

# ======================================
# 3. ACCIDENTES POR HORA
# ======================================

st.header("Accidentes por Hora")

accidentes_hora = (
    df_horas["ID_HORA"]
    .value_counts()
    .sort_index()
    .reset_index()
)

accidentes_hora.columns = [
    "Hora",
    "Accidentes"
]

fig_horas = px.line(
    accidentes_hora,
    x="Hora",
    y="Accidentes",
    markers=True,
    title="Accidentes por Hora"
)

st.plotly_chart(
    fig_horas,
    use_container_width=True
)

# ======================================
# 4. CAUSAS MÁS FRECUENTES
# ======================================

st.header("Causas Más Frecuentes")

causas = (
    df["CAUSAACCI"]
    .value_counts()
    .head(10)
    .reset_index()
)

causas.columns = [
    "Causa",
    "Cantidad"
]

fig_causas = px.bar(
    causas,
    x="Causa",
    y="Cantidad",
    title="Causas Más Frecuentes"
)

st.plotly_chart(
    fig_causas,
    use_container_width=True
)


# ======================================
# 5. ACCIDENTES POR MES
# ======================================

st.header("Accidentes por Mes")

meses = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

accidentes_mes = (
    df_meses["MES"]
    .value_counts()
    .sort_index()
    .reset_index()
)

accidentes_mes.columns = [
    "Mes",
    "Accidentes"
]

accidentes_mes["Mes"] = accidentes_mes["Mes"].map(meses)

fig_meses = px.bar(
    accidentes_mes,
    x="Mes",
    y="Accidentes",
    title="Accidentes por Mes"
)

st.plotly_chart(
    fig_meses,
    use_container_width=True
)

# ======================================
# 6. ESTADOS CON MÁS HERIDOS Y FALLECIDOS
# ======================================

st.header("Estados con Más Heridos y Fallecidos")

# ======================================
# CONVERTIR COLUMNAS NUMÉRICAS
# ======================================

columnas_victimas = [
    "CONDHERIDO",
    "PASAHERIDO",
    "PEATHERIDO",
    "CICLHERIDO",
    "OTROHERIDO",
    "CONDMUERTO",
    "PASAMUERTO",
    "PEATMUERTO",
    "CICLMUERTO",
    "OTROMUERTO"
]

for columna in columnas_victimas:

    df[columna] = pd.to_numeric(
        df[columna],
        errors="coerce"
    ).fillna(0)

# ======================================
# CALCULAR HERIDOS Y FALLECIDOS
# ======================================

df["TOTAL_HERIDOS"] = (
    df["CONDHERIDO"] +
    df["PASAHERIDO"] +
    df["PEATHERIDO"] +
    df["CICLHERIDO"] +
    df["OTROHERIDO"]
)

df["TOTAL_FALLECIDOS"] = (
    df["CONDMUERTO"] +
    df["PASAMUERTO"] +
    df["PEATMUERTO"] +
    df["CICLMUERTO"] +
    df["OTROMUERTO"]
)

# ======================================
# AGRUPAR POR ESTADO
# ======================================

victimas_estado = (
    df.groupby("ESTADO")[
        ["TOTAL_HERIDOS", "TOTAL_FALLECIDOS"]
    ]
    .sum()
    .reset_index()
)

# TOP HERIDOS
top_heridos = (
    victimas_estado
    .sort_values(
        by="TOTAL_HERIDOS",
        ascending=False
    )
    .head(10)
)

# TOP FALLECIDOS
top_fallecidos = (
    victimas_estado
    .sort_values(
        by="TOTAL_FALLECIDOS",
        ascending=False
    )
    .head(10)
)

# ======================================
# GRÁFICA HERIDOS
# ======================================

fig_heridos = px.bar(
    top_heridos,
    x="ESTADO",
    y="TOTAL_HERIDOS",
    title="Estados con Más Heridos"
)

st.plotly_chart(
    fig_heridos,
    use_container_width=True
)

# ======================================
# GRÁFICA FALLECIDOS
# ======================================

fig_fallecidos = px.bar(
    top_fallecidos,
    x="ESTADO",
    y="TOTAL_FALLECIDOS",
    title="Estados con Más Fallecidos"
)

st.plotly_chart(
    fig_fallecidos,
    use_container_width=True
)



# ======================================
# 7. COMPARACIÓN PANDAS VS RAY
# ======================================

st.header("Comparación Pandas vs Ray")

# ======================================
# PANDAS
# ======================================

inicio_pandas = time.time()

resultado_pandas = (
    df.groupby("ID_ENTIDAD")
    .size()
)

fin_pandas = time.time()

tiempo_pandas = (
    fin_pandas - inicio_pandas
)

# ======================================
# RAY
# ======================================

ray.init(ignore_reinit_error=True)

# Guardar dataframe en memoria distribuida
df_ref = ray.put(df)

estados_ids = df["ID_ENTIDAD"].unique()

@ray.remote
def contar_accidentes(estado, dataframe):

    df_estado = dataframe[
        dataframe["ID_ENTIDAD"] == estado
    ]

    return len(df_estado)

inicio_ray = time.time()

futuros = [
    contar_accidentes.remote(
        estado,
        df_ref
    )
    for estado in estados_ids
]

resultados_ray = ray.get(futuros)

fin_ray = time.time()

tiempo_ray = (
    fin_ray - inicio_ray
)

# ======================================
# SPEEDUP
# ======================================

speedup = (
    tiempo_pandas / tiempo_ray
)

# ======================================
# TABLA
# ======================================

comparacion = pd.DataFrame({

    "Tecnología": [
        "Pandas",
        "Ray"
    ],

    "Tiempo": [
        tiempo_pandas,
        tiempo_ray
    ]
})

# ======================================
# GRÁFICA
# ======================================

fig_comparacion = px.bar(
    comparacion,
    x="Tecnología",
    y="Tiempo",
    title="Tiempo de Ejecución"
)

st.plotly_chart(
    fig_comparacion,
    use_container_width=True
)

# ======================================
# RESULTADOS
# ======================================

st.subheader("Resultados")

st.write(
    f"Tiempo Pandas: {tiempo_pandas:.6f} segundos"
)

st.write(
    f"Tiempo Ray: {tiempo_ray:.6f} segundos"
)

st.write(
    f"Speedup: {speedup:.6f}"
)

if speedup > 1:

    st.success(
        "Ray fue más rápido."
    )

else:

    st.info(
        "Pandas fue más rápido para este dataset."
    )

# ======================================
# CONCLUSIONES
# ======================================

st.header("Conclusiones")

st.markdown("""
- Pandas fue más rápido para datasets medianos.
- Ray introduce overhead de distribución.
- Parquet mejora almacenamiento y lectura.
- El procesamiento distribuido depende del tamaño del problema.
- Streamlit permitió visualizar los resultados de manera interactiva.
""")