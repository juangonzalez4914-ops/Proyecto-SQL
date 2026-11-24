import json
import os
from api.api_client import APIClient

cliente = APIClient()
datos = cliente.obtener_registros(5)
print("Cantidad recibida:", len(datos))
print(datos[0] if datos else "La API no devolvió registros")

os.makedirs("evidencias", exist_ok=True)
with open("evidencias/respuesta_api.json", "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, ensure_ascii=False, indent=2)
print("Evidencia guardada en evidencias/respuesta_api.json")
