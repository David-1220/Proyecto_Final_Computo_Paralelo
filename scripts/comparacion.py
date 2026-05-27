import pandas as pd
import ray
import time

print("INICIANDO COMPARACIÓN...")

# ======================================
# CARGAR DATASET
# ======================================

ruta = "../data/raw/atus_anual_2024.csv"

df = pd.read_csv(ruta, encoding='utf-8')

print("DATASET CARGADO")

# ======================================
# PANDAS SECUENCIAL
# ======================================

inicio_pandas = time.time()

resultado_pandas = df.groupby("ID_ENTIDAD").size()

fin_pandas = time.time()

tiempo_pandas = fin_pandas - inicio_pandas

print("\nPANDAS TERMINADO")

# ======================================
# RAY DISTRIBUIDO
# ======================================

ray.init(ignore_reinit_error=True)

estados = df["ID_ENTIDAD"].unique()

@ray.remote
def contar_accidentes(estado, dataframe):

    df_estado = dataframe[dataframe["ID_ENTIDAD"] == estado]

    return len(df_estado)

inicio_ray = time.time()

futuros = [
    contar_accidentes.remote(estado, df)
    for estado in estados
]

resultados_ray = ray.get(futuros)

fin_ray = time.time()

tiempo_ray = fin_ray - inicio_ray

print("RAY TERMINADO")

# ======================================
# SPEEDUP
# ======================================

speedup = tiempo_pandas / tiempo_ray

# ======================================
# RESULTADOS
# ======================================

print("\n========== RESULTADOS ==========\n")

print(f"Tiempo Pandas: {tiempo_pandas:.6f} segundos")

print(f"Tiempo Ray: {tiempo_ray:.6f} segundos")

print(f"Speedup: {speedup:.6f}")

# ======================================
# INTERPRETACIÓN
# ======================================

if speedup > 1:
    print("\nRay fue más rápido.")
elif speedup < 1:
    print("\nPandas fue más rápido.")
else:
    print("\nAmbos tuvieron rendimiento similar.")

print("\nCOMPARACIÓN FINALIZADA")