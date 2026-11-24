import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from api.api_client import APIClient
from models.datos_model import (
    guardar_registros,
    consultar_registros,
    obtener_resumen,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave-local-de-desarrollo")


@app.route("/", methods=["GET"])
def inicio():
    filtro = request.args.get("q", "").strip()
    try:
        registros = consultar_registros(filtro)
        resumen = obtener_resumen()
    except Exception as error:
        flash(f"No fue posible consultar SQL Server: {error}", "error")
        registros = []
        resumen = None
    return render_template(
        "index.html",
        registros=registros,
        filtro=filtro,
        resumen=resumen,
    )


@app.route("/sincronizar", methods=["POST"])
def sincronizar():
    try:
        cliente = APIClient()
        datos = cliente.obtener_registros(100)
        cantidad = guardar_registros(datos)
        flash(
            f"Consulta terminada. Registros recibidos: {len(datos)}. "
            f"Nuevos guardados: {cantidad}",
            "success",
        )
    except Exception as error:
        flash(f"No fue posible consultar o guardar los datos: {error}", "error")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
