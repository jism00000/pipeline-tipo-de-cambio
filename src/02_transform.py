import json
from pathlib import Path

import pandas as pd

CARPETA_RAW = Path(__file__).parent.parent / "data" / "raw"


def cargar_json_mas_reciente():
    archivos = sorted(CARPETA_RAW.glob("*.json"))
    if not archivos:
        raise FileNotFoundError("No hay archivos en data/raw. Corre 01_extract.py primero.")
    with open(archivos[-1], encoding="utf-8") as f:
        return json.load(f)


def limpiar(datos):
    serie = datos["bmx"]["series"][0]
    df = pd.DataFrame(serie["datos"])

    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
    df["dato"] = pd.to_numeric(df["dato"], errors="coerce")

    df = df.dropna(subset=["dato"])
    df = df.rename(columns={"dato": "tipo_cambio"})
    df = df.sort_values("fecha").reset_index(drop=True)

    df["fecha_carga"] = pd.Timestamp.now()

    return df


if __name__ == "__main__":
    datos = cargar_json_mas_reciente()
    df = limpiar(datos)
    print(df.head())
    print(f"\n{len(df)} filas limpias")