from config.db import get_connection

class CircuitoService:
    @staticmethod
    def registrar_circuito(data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        insert = """
            INSERT INTO CIRCUITO (
                accesibilidad,
                id_establecimiento,
                id_zona,
                id_eleccion,
                id_tipo_eleccion
            ) VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            data["accesibilidad"],
            data["id_establecimiento"],
            data["id_zona"],
            data["id_eleccion"],
            data["id_tipo_eleccion"]
        )

        try:
            cursor.execute(insert, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar circuito: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
