import os
import json
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    servidor = os.getenv("DB_SERVER")
    base_datos = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    trusted = os.getenv("DB_TRUSTED", "yes").lower() == "yes"
    if trusted:
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
    else:
        usuario = os.getenv("DB_USER")
        clave = os.getenv("DB_PASSWORD")
        cadena = (
            f"DRIVER={{{driver}}};"
            f"SERVER={servidor};"
            f"DATABASE={base_datos};"
            f"UID={usuario};PWD={clave};"
            "TrustServerCertificate=yes;"
        )
    return pyodbc.connect(cadena)


def _a_entero(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def guardar_registros(registros):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    insertados = 0
    try:
        for registro in registros:
            identificador = str(registro.get("id_de_caso") or "").strip()
            if not identificador:
                continue
            cursor.execute(
                "SELECT 1 FROM RegistrosAPI WHERE id_api = ?",
                identificador,
            )
            if cursor.fetchone():
                continue
            cursor.execute(
                """
                INSERT INTO RegistrosAPI
                (id_api, departamento, municipio, edad, sexo, estado,
                 recuperado, fecha_reporte, json_original)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                identificador,
                registro.get("departamento_nom"),
                registro.get("ciudad_municipio_nom"),
                _a_entero(registro.get("edad")),
                registro.get("sexo"),
                registro.get("estado"),
                registro.get("recuperado"),
                registro.get("fecha_reporte_web"),
                json.dumps(registro, ensure_ascii=False),
            )
            insertados += 1
        conexion.commit()
        return insertados
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def consultar_registros(filtro=""):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        if filtro:
            cursor.execute(
                """
                SELECT TOP 100 id_api, departamento, municipio, edad,
                       sexo, estado, recuperado, fecha_reporte
                FROM RegistrosAPI
                WHERE municipio LIKE ?
                   OR departamento LIKE ?
                   OR estado LIKE ?
                ORDER BY fecha_reporte DESC
                """,
                f"%{filtro}%",
                f"%{filtro}%",
                f"%{filtro}%",
            )
        else:
            cursor.execute(
                """
                SELECT TOP 100 id_api, departamento, municipio, edad,
                       sexo, estado, recuperado, fecha_reporte
                FROM RegistrosAPI
                ORDER BY fecha_reporte DESC
                """
            )
        columnas = [columna[0] for columna in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def obtener_resumen():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT COUNT(*), AVG(CAST(edad AS FLOAT)), MIN(edad), MAX(edad)
            FROM RegistrosAPI
            """
        )
        total, promedio, minima, maxima = cursor.fetchone()
        cursor.execute(
            """
            SELECT ISNULL(sexo, 'Sin dato'), COUNT(*)
            FROM RegistrosAPI
            GROUP BY sexo
            ORDER BY COUNT(*) DESC
            """
        )
        por_sexo = [(fila[0], fila[1]) for fila in cursor.fetchall()]
        return {
            "total": total,
            "promedio_edad": round(promedio, 1) if promedio is not None else None,
            "edad_minima": minima,
            "edad_maxima": maxima,
            "por_sexo": por_sexo,
        }
    finally:
        cursor.close()
        conexion.close()
