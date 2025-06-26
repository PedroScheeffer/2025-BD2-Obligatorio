from config.db import get_connection
import mysql.connector

class ResultadosService:
    @staticmethod
    def obtener_resultados(categoria: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if categoria == "circuito":
            query = """
                SELECT id_circuito AS nombre, COUNT(*) AS votos
                FROM VOTO
                GROUP BY id_circuito
            """
        elif categoria == "departamento":
            query = """
                SELECT Z.departamento AS nombre, COUNT(*) AS votos
                FROM VOTO V
                JOIN CIRCUITO C ON V.id_circuito = C.id
                JOIN ESTABLECIMIENTO E ON C.id_establecimiento = E.id
                JOIN ZONA Z ON E.id_zona = Z.id
                GROUP BY Z.departamento
            """
        elif categoria == "lista":
            query = """
                SELECT CONCAT(valor_lista) AS nombre, COUNT(*) AS votos
                FROM VOTO
                GROUP BY valor_lista, id_partido
            """
        elif categoria == "partidos":
            query = """
                SELECT P.nombre AS nombre, COUNT(*) AS votos
                FROM VOTO V
                JOIN PARTIDO P ON V.id_partido = P.id
                GROUP BY P.nombre
            """
        else:
            raise ValueError("Categoría inválida")

        cursor.execute(query)
        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultados
