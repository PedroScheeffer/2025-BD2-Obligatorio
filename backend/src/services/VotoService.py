import mysql.connector
from config.db import get_connection
from datetime import date


class VotoService:
    @staticmethod
    def obtener_opciones(id_tipo_eleccion):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        hoy = date.today().strftime('%Y-%m-%d')

        # Get the election closest to today (before or after)
        query_eleccion = """
            SELECT id, id_tipo_eleccion, fecha
            FROM ELECCION
            WHERE id_tipo_eleccion = %s
            ORDER BY ABS(DATEDIFF(fecha, %s)) ASC
            LIMIT 1
        """
        cursor.execute(query_eleccion, (id_tipo_eleccion, hoy))
        eleccion = cursor.fetchone()

        if not eleccion:
            return []

        # Defensive: sometimes MySQL returns a dict, sometimes a tuple, sometimes a mix (esp. with date fields)
        eleccion_id = None
        if isinstance(eleccion, dict):
            eleccion_id = eleccion.get('id')
        elif isinstance(eleccion, (list, tuple)):
            # Try to find the int id (should not be a date)
            for v in eleccion:
                if isinstance(v, int):
                    eleccion_id = v
                    break
        if eleccion_id is None:
            return []
        eleccion_tipo = eleccion['id_tipo_eleccion'] if isinstance(
            eleccion, dict) else eleccion[1]
        eleccion_fecha = eleccion['fecha'] if isinstance(
            eleccion, dict) else eleccion[2]

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
            WHERE e.id = %s
        """
        # Ensure only int is passed to query (avoid date, etc)
        # Defensive: if eleccion_id is not int, try to convert, else skip (avoid date, etc)
        if not isinstance(eleccion_id, int):
            # Try to convert only if it's a string or float
            if isinstance(eleccion_id, (str, float)):
                try:
                    eleccion_id = int(eleccion_id)
                except Exception:
                    return []
            else:
                return []
        cursor.execute(query, (eleccion_id,))
        resultados = cursor.fetchall()

        print("Consulta ejecutada para elección id:",
              eleccion_id, "fecha:", eleccion_fecha)
        print("Resultados obtenidos:", resultados)

        if not resultados:
            return []

        opciones = []
        for r in resultados:
            # r is a dict if dictionary=True, else a tuple
            valor_lista = r['valor_lista'] if isinstance(r, dict) else r[0]
            id_partido = r['id_partido'] if isinstance(r, dict) else r[1]
            id_eleccion = r['id_eleccion'] if isinstance(r, dict) else r[2]
            id_tipo_eleccion = r['id_tipo_eleccion'] if isinstance(
                r, dict) else r[3]
            nombre_partido = r['nombre_partido'] if isinstance(
                r, dict) else r[4]
            opciones.append({
                "valor_lista": valor_lista,
                "id_partido": id_partido,
                "id_eleccion": id_eleccion,
                "id_tipo_eleccion": id_tipo_eleccion,
                "label": f"Lista {valor_lista} - {nombre_partido}",
                "id_tipo_voto": 1  # válido
            })

        opciones.append({
            "valor_lista": 0,
            "id_partido": 0,
            "id_eleccion": opciones[0]["id_eleccion"] if opciones else 1,
            "id_tipo_eleccion": opciones[0]["id_tipo_eleccion"] if opciones else 1,
            "label": "Blanco",
            "id_tipo_voto": 2  # blanco
        })

        opciones.append({
            "valor_lista": 0,
            "id_partido": 0,
            "id_eleccion": opciones[0]["id_eleccion"] if opciones else 1,
            "id_tipo_eleccion": opciones[0]["id_tipo_eleccion"] if opciones else 1,
            "label": "Anulado",
            "id_tipo_voto": 3  # anulado
        })

        return opciones

    @staticmethod
    def registrar_voto(data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT voto, id_circuito FROM VOTANTE WHERE cc = %s", (data["cc"],))
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

        cursor.execute(
            "UPDATE VOTANTE SET voto = TRUE WHERE cc = %s", (data["cc"],))

        conn.commit()
        return True
