import json
from pathlib import Path

import pandas as pd

carpeta = Path("data/raw")
archivo = sorted(carpeta.glob("*.json"))[-1]

with open(archivo, encoding="utf-8") as f:
    datos = json.load(f)

serie = datos["bmx"]["series"][0]
df = pd.DataFrame(serie["datos"])

df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
df["dato"] = pd.to_numeric(df["dato"], errors="coerce")

print()
print(df)
print()
print(df.dtypes)
print(df["dato"].isna().sum())