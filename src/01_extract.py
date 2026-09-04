import os
import json
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BANXICO_TOKEN")

SERIE = "SF43718"
URL = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{SERIE}/datos/oportuno"

CARPETA_RAW = Path(__file__).parent.parent / "data" / "raw"


def extraer():
    respuesta = requests.get(URL, headers={"Bmx-Token": TOKEN}, timeout=30)
    respuesta.raise_for_status()
    return respuesta.json()


def guardar(datos):
    CARPETA_RAW.mkdir(parents=True, exist_ok=True)
    hoy = date.today().isoformat()
    ruta = CARPETA_RAW / f"banxico_{SERIE}_{hoy}.json"

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)

    return ruta


if __name__ == "__main__":
    datos = extraer()
    ruta = guardar(datos)
    print(f"Guardado en: {ruta}")