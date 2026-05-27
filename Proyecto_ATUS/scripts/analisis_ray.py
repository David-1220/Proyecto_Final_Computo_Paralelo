import pandas as pd
import ray
import time

print("INICIANDO RAY...")

# Inicializar Ray
ray.init()

# Leer dataset
ruta = "../data/raw/atus_anual_2024.csv"

df = pd.read_csv(ruta, encoding='utf-8')

print("DATASET CARGADO")

# Obtener estados únicos
estados = df["ID_ENTIDAD"].unique()

# ====================================
# FUNCIÓN DISTRIBUIDA
# ====================================

@ray.remote
def analizar_estado(estado, dataframe):

    df_estado = dataframe[dataframe["ID_ENTIDAD"] == estado]

    total_accidentes = len(df_estado)

    total_heridos = (
        df_estado["CONDHERIDO"].sum()
        + df_estado["PASAHERIDO"].sum()
        + df_estado["PEATHERIDO"].sum()
        + df_estado["CICLHERIDO"].sum()
        + df_estado["OTROHERIDO"].sum()
    )

    total_fallecidos = (
        df_estado["CONDMUERTO"].sum()
        + df_estado["PASAMUERTO"].sum()
        + df_estado["PEATMUERTO"].sum()
        + df_estado["CICLMUERTO"].sum()
        + df_estado["OTROMUERTO"].sum()
    )

    return {
        "estado": estado,
        "accidentes": total_accidentes,
        "heridos": total_heridos,
        "fallecidos": total_fallecidos
    }

# ====================================
# MEDIR TIEMPO
# ====================================

inicio = time.time()

# Lanzar tareas distribuidas
futuros = [
    analizar_estado.remote(estado, df)
    for estado in estados
]

# Obtener resultados
resultados = ray.get(futuros)

fin = time.time()

# ====================================
# MOSTRAR RESULTADOS
# ====================================

print("\nRESULTADOS POR ESTADO:\n")

for r in resultados[:10]:
    print(r)

print("\nTIEMPO DE EJECUCIÓN:")
print(fin - inicio, "segundos")

print("\nANÁLISIS DISTRIBUIDO TERMINADO")