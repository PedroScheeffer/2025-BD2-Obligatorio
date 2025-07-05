from config.db import get_connection


class ListaService:
    @staticmethod
    def registrar_lista(data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Obtener el id_tipo_eleccion a partir del id_eleccion
            query_tipo = "SELECT id_tipo_eleccion FROM ELECCION WHERE id = %s"
            cursor.execute(query_tipo, (data["id_eleccion"],))
            tipo_result = cursor.fetchone()

            if not tipo_result:
                raise Exception("Elección no encontrada")

            id_tipo_eleccion = tipo_result["id_tipo_eleccion"]

            # Insertar en la tabla LISTA
            insert_lista = """
                INSERT INTO LISTA (
                    valor,
                    id_partido,
                    id_eleccion
                ) VALUES (%s, %s, %s)
            """

            valores_lista = (
                data["numero"],
                data["id_partido"],
                data["id_eleccion"]
            )

            cursor.execute(insert_lista, valores_lista)

            # Insertar en la tabla CANDIDATO_LISTA por cada candidato
            candidatos = data["candidatos"].split(",")  # e.g. "ABC123,DEF456"
            for cc in candidatos:
                insert_candidato_lista = """
                    INSERT INTO CANDIDATO_LISTA (
                        cc,
                        valor_lista,
                        id_partido,
                        id_eleccion
                    ) VALUES (%s, %s, %s, %s)
                """

                valores_candidato = (
                    cc.strip(),                     # cc
                    data["numero"],                # valor_lista
                    data["id_partido"],
                    data["id_eleccion"]
                )

                cursor.execute(insert_candidato_lista, valores_candidato)

            conn.commit()
            return True

        except Exception as e:
            print(f"Error al registrar lista: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
