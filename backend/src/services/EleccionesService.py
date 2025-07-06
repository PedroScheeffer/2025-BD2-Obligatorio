from config.db import get_connection
from model.Eleccion import Eleccion, EleccionConCircuitosSchema
from services.CircuitoService import CircuitoService
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner


class EleccionesService:
    @staticmethod
    def get_all_elecciones():
        script = f"SELECT * FROM {Eleccion.table_name}"
        results = MySQLScriptRunner.run_script_to_query_database(script)
        if results:
            return [Eleccion(**row) for row in results]
        return []

    @staticmethod
    def get_all_elecciones_con_circuitos() -> list[EleccionConCircuitosSchema]:
        elecciones = EleccionesService.get_all_elecciones()
        elecciones_con_circuitos = []
        for eleccion in elecciones:
            if eleccion.id is None:
                continue
            circuitos_objects = CircuitoService.get_circuitos_by_eleccion(
                eleccion.id)
            circuitos_data = [c.__dict__ for c in circuitos_objects]

            fecha_str = eleccion.fecha.isoformat() if hasattr(
                eleccion.fecha, 'isoformat') else str(eleccion.fecha)

            eleccion_con_circuitos = EleccionConCircuitosSchema(
                id=eleccion.id,
                fecha=fecha_str,
                id_tipo_eleccion=eleccion.id_tipo_eleccion,
                circuitos=circuitos_data
            )
            elecciones_con_circuitos.append(eleccion_con_circuitos)
        return elecciones_con_circuitos

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
