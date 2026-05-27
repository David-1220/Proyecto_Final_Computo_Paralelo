import pandas as pd
import time

print("INICIANDO CONVERSIÓN A PARQUET...")

inicio = time.time()

# Leer CSV
ruta_csv = "../data/raw/atus_anual_2024.csv"

df = pd.read_csv(ruta_csv, encoding='utf-8')

print("CSV CARGADO")

# Guardar en parquet
ruta_parquet = "../data/raw/atus_anual_2024.parquet"

df.to_parquet(ruta_parquet)

fin = time.time()

print("\nARCHIVO PARQUET GENERADO")

print(f"\nTiempo total: {fin - inicio:.2f} segundos")