import os
import requests
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    def __init__(self):
        recurso = os.getenv("API_RESOURCE_ID", "gt2j-8ykr")
        self.url = f"https://www.datos.gov.co/resource/{recurso}.json"
        self.municipio = os.getenv("API_MUNICIPIO", "").strip()

    def obtener_registros(self, limite=100):
        parametros = {
            "$limit": limite,
            "$order": "fecha_reporte_web DESC",
        }
        if self.municipio:
            municipio = self.municipio.upper().replace("'", "''")
            parametros["$where"] = f"ciudad_municipio_nom = '{municipio}'"
        respuesta = requests.get(self.url, params=parametros, timeout=20)
        respuesta.raise_for_status()
        return respuesta.json()
