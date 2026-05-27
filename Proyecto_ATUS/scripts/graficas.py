import pandas as pd
import matplotlib.pyplot as plt

print("GENERANDO GRÁFICAS...")

# ======================================
# CARGAR DATASET
# ======================================

df = pd.read_parquet(
    "../data/raw/atus_anual_2024.parquet"
)

print("DATASET CARGADO")

# ======================================
# TOP ESTADOS
# ======================================

top_estados = (
    df["ID_ENTIDAD"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10,5))

top_estados.plot(kind='bar')

plt.title("Top 10 Estados con Más Accidentes")

plt.xlabel("Estado")

plt.ylabel("Accidentes")

plt.tight_layout()

plt.savefig("../graficas/top_estados.png")

plt.close()

print("Gráfica estados generada")

# ======================================
# ACCIDENTES POR HORA
# ======================================

accidentes_hora = (
    df["ID_HORA"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(12,5))

accidentes_hora.plot(kind='line')

plt.title("Accidentes por Hora")

plt.xlabel("Hora")

plt.ylabel("Cantidad")

plt.grid(True)

plt.tight_layout()

plt.savefig("../graficas/accidentes_hora.png")

plt.close()

print("Gráfica horas generada")

# ======================================
# CAUSAS MÁS FRECUENTES
# ======================================

causas = (
    df["CAUSAACCI"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10,5))

causas.plot(kind='bar')

plt.title("Causas Más Frecuentes")

plt.xlabel("Causa")

plt.ylabel("Cantidad")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("../graficas/causas.png")

plt.close()

print("Gráfica causas generada")

# ======================================
# ACCIDENTES POR MES
# ======================================

accidentes_mes = (
    df["MES"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10,5))

accidentes_mes.plot(kind='bar')

plt.title("Accidentes por Mes")

plt.xlabel("Mes")

plt.ylabel("Cantidad")

plt.tight_layout()

plt.savefig("../graficas/meses.png")

plt.close()

print("Gráfica meses generada")

# ======================================
# COMPARACIÓN PANDAS VS RAY
# ======================================

tecnologias = ["Pandas", "Ray"]

tiempos = [0.014, 4.23]

plt.figure(figsize=(6,5))

plt.bar(tecnologias, tiempos)

plt.title("Comparación de Tiempo de Ejecución")

plt.ylabel("Segundos")

plt.tight_layout()

plt.savefig("../graficas/comparacion.png")

plt.close()

print("Gráfica comparación generada")

print("\nTODAS LAS GRÁFICAS FUERON GENERADAS")