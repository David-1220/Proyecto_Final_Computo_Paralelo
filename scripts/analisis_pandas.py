import pandas as pd
import matplotlib.pyplot as plt

print("INICIANDO ANÁLISIS...")

# Leer dataset
ruta = "../data/raw/atus_anual_2024.csv"

df = pd.read_csv(ruta, encoding='utf-8')

print("DATASET CARGADO")

# =========================
# ACCIDENTES POR ESTADO
# =========================

accidentes_estado = df.groupby("ID_ENTIDAD").size()
accidentes_estado = accidentes_estado.sort_values(ascending=False)

print("\nTOP 10 ESTADOS CON MÁS ACCIDENTES:\n")
print(accidentes_estado.head(10))

# =========================
# ACCIDENTES POR HORA
# =========================

accidentes_hora = df.groupby("ID_HORA").size()

print("\nACCIDENTES POR HORA:\n")
print(accidentes_hora)

# =========================
# CAUSAS MÁS FRECUENTES
# =========================

causas = df.groupby("CAUSAACCI").size()
causas = causas.sort_values(ascending=False)

print("\nCAUSAS MÁS FRECUENTES:\n")
print(causas.head(10))

# =========================
# TOTAL HERIDOS
# =========================

total_heridos = (
    df["CONDHERIDO"].sum()
    + df["PASAHERIDO"].sum()
    + df["PEATHERIDO"].sum()
    + df["CICLHERIDO"].sum()
    + df["OTROHERIDO"].sum()
)

print("\nTOTAL DE HERIDOS:")
print(total_heridos)

# =========================
# TOTAL FALLECIDOS
# =========================

total_fallecidos = (
    df["CONDMUERTO"].sum()
    + df["PASAMUERTO"].sum()
    + df["PEATMUERTO"].sum()
    + df["CICLMUERTO"].sum()
    + df["OTROMUERTO"].sum()
)

print("\nTOTAL DE FALLECIDOS:")
print(total_fallecidos)

# =========================
# GRÁFICA
# =========================

accidentes_estado.head(10).plot(kind='bar')

plt.title("Top 10 Estados con Más Accidentes")
plt.xlabel("Estado")
plt.ylabel("Número de Accidentes")

plt.tight_layout()
plt.show()

print("\nANÁLISIS TERMINADO")