import mysql.connector
from config.db import get_connection
from datetime import date

class VotoService:
    @staticmethod
    def obtener_opciones():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        hoy = date.today()

        query = """
            SELECT 
                l.valor AS valor_lista,
                p.id AS id_partido,
                e.id AS id_eleccion,
                e.id_tipo_eleccion,
                p.nombre AS nombre_partido
            FROM LISTA l
            JOIN PARTIDO p ON l.id_partido = p.id
            JOIN ELECCION e ON l.id_eleccion = e.id
            WHERE e.fecha = '2025-06-25'
        """

        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            return []  

        opciones = []

        for r in resultados:
            opciones.append({
                "valor_lista": r["valor_lista"],
                "id_partido": r["id_partido"],
                "id_eleccion": r["id_eleccion"],
                "id_tipo_eleccion": r["id_tipo_eleccion"],
                "label": f"Lista {r['valor_lista']} - {r['nombre_partido']}",
                "id_tipo_voto": 1  # válido
            })

        opciones.append({
            "valor_lista": 0,
            "id_partido": 0,
            "id_eleccion": resultados[0]["id_eleccion"] if resultados else 1,
            "id_tipo_eleccion": resultados[0]["id_tipo_eleccion"] if resultados else 1,
            "label": "Blanco",
            "id_tipo_voto": 2  # blanco
        })

        opciones.append({
            "valor_lista": 0,
            "id_partido": 0,
            "id_eleccion": resultados[0]["id_eleccion"] if resultados else 1,
            "id_tipo_eleccion": resultados[0]["id_tipo_eleccion"] if resultados else 1,
            "label": "Anulado",
            "id_tipo_voto": 3  # anulado
        })

        return opciones

    @staticmethod
    def registrar_voto(data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT voto, id_circuito FROM VOTANTE WHERE cc_persona = %s", (data["cc_persona"],))
        votante = cursor.fetchone()

        if not votante:
            raise Exception("La persona no está registrada como votante")

        if votante["voto"]:
            raise Exception("La persona ya votó")

        voto_observado = votante["id_circuito"] != data["id_circuito"]

        insert = """
            INSERT INTO VOTO (
                valor_lista, id_partido, id_eleccion,
                id_tipo_eleccion, id_tipo_voto,
                id_circuito, fecha, es_observado
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            data["valor_lista"],
            data["id_partido"],
            data["id_eleccion"],
            data["id_tipo_eleccion"],
            data["id_tipo_voto"],
            data["id_circuito"],
            data["fecha"],
            voto_observado
        )

        cursor.execute(insert, values)

        cursor.execute("UPDATE VOTANTE SET voto = TRUE WHERE cc_persona = %s", (data["cc_persona"],))

        conn.commit()
        return True