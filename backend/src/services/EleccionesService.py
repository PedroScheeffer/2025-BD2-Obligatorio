from config.db import get_connection

class EleccionesService:
    @staticmethod
    def registrar_eleccion(data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Primero obtenemos el id_tipo_eleccion correspondiente al nombre recibido
        obtener_tipo_query = "SELECT id FROM TIPOELECCION WHERE tipo = %s"
        cursor.execute(obtener_tipo_query, (data["tipo"],))
        tipo_result = cursor.fetchone()

        if not tipo_result:
            raise Exception("Tipo de elección no válido")

        id_tipo_eleccion = tipo_result["id"]

        insert_query = """
            INSERT INTO ELECCION (fecha, id_tipo_eleccion)
            VALUES (%s, %s)
        """

        values = (data["fecha"], id_tipo_eleccion)

        try:
            cursor.execute(insert_query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar elección: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
