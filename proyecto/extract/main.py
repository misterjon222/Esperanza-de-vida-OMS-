from GestionArchivos import GestionArchivos
from datetime import datetime
import json

ENTORNO = "DESARROLLO"

with open('./config.json', 'r') as file:
    config = json.load(file)

print("Iniciando el proceso de Extracción...")

objGestionArchivos = GestionArchivos()

objGestionArchivos.download_archiverar_url(
    URL_DATOS_DOWNLOAD=config[ENTORNO]['URL_DATOS_DOWNLOAD'], RUTA_DOWNLOAD=config[ENTORNO]['RUTA_DOWNLOAD'])

objGestionArchivos.unRarFileDownload(
    RUTA_DOWNLOAD=config[ENTORNO]['RUTA_DOWNLOAD'], RUTA_DESCARGA=config[ENTORNO]['RUTA_DOWNLOAD'])
