from config.db import get_connection


class CandidatoService:
    @staticmethod
    def registrar_candidato(data):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM PERSONA WHERE cc = %s", (data["cc"],))
            persona = cursor.fetchone()

            if not persona:
                insert_persona = """
                    INSERT INTO PERSONA (cc, nombre, fecha_nacimiento)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_persona, (
                    data["cc"],
                    data["nombre"],
                    data["fecha_nacimiento"]
                ))

            insert_candidato = """
                INSERT INTO CANDIDATO (cc, id_tipo)
                VALUES (%s, %s)
            """
            cursor.execute(insert_candidato, (
                data["cc"],
                data["id_tipo"]
            ))

            conn.commit()
            return True
        except Exception as e:
            print("Error al registrar candidato:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
