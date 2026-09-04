import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BANXICO_TOKEN")

url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
headers = {"Bmx-Token": token}

respuesta = requests.get(url, headers=headers)
respuesta.raise_for_status()

print(respuesta.json())