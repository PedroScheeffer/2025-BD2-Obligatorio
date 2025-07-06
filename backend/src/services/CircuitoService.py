from config.db import get_connection
from model.ubicacion.Circuito import Circuito
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner

from config.logger import logger


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
            logger.error(f"Error al registrar circuito: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_circuito_by_id(circuito_id: int):
        script, params = MySQLScriptGenerator.create_select_all_columns_script(
            filter_key="id",
            filter_value=circuito_id,
            table_name=Circuito.table_name
        )
        result = MySQLScriptRunner.run_script_to_query_database(script, params)
        if result:
            return Circuito(**result[0])
        return None

    @staticmethod
    def get_circuitos_by_eleccion(eleccion_id: int):
        try:
            script, params = MySQLScriptGenerator.create_select_all_columns_script(
                filter_key="id_eleccion",
                filter_value=eleccion_id,
                table_name=Circuito.table_name
            )
            results = MySQLScriptRunner.run_script_to_query_database(
                script, params)
            if not results:
                return []  # Return an empty list if no circuits are found
            return [Circuito(**row) for row in results]
        except Exception as e:
            logger.error(f"Error al obtener circuitos por elección: {e}")
            raise
