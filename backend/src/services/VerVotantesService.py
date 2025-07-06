from config.db import get_connection

class VerVotantesService:
    @staticmethod
    def obtener_votantes_por_circuito(id_circuito: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                P.cc,
                P.nombre,
                P.ci,
                DATE_FORMAT(P.fecha_nacimiento, '%Y-%m-%d') AS fecha_nacimiento,
                V.voto
            FROM VOTANTE V
            JOIN PERSONA P ON V.cc = P.cc
            WHERE V.id_circuito = %s
            ORDER BY P.nombre
        """
        cursor.execute(query, (id_circuito,))
        votantes = cursor.fetchall()

        cursor.close()
        conn.close()
        return votantes
