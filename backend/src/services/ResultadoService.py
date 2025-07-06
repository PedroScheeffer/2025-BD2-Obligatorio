from config.db import get_connection
import mysql.connector

class ResultadosService:
    @staticmethod
    def obtener_resultados(categoria: str):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if categoria == "circuito":
            query = """
                SELECT id_circuito AS nombre, 
                    SUM(CASE WHEN TV.tipo = 'valido' THEN 1 ELSE 0 END) AS votos_validos,
                    SUM(CASE WHEN TV.tipo = 'anulado' THEN 1 ELSE 0 END) AS votos_anulados,
                    SUM(CASE WHEN TV.tipo = 'blanco' THEN 1 ELSE 0 END) AS votos_blanco,
                    SUM(CASE WHEN V.es_observado = 1 THEN 1 ELSE 0 END) AS votos_observados
                FROM VOTO V
                JOIN TIPOVOTO TV ON V.id_tipo_voto = TV.id
                GROUP BY id_circuito
            """
        elif categoria == "departamento":
            query = """
                SELECT Z.departamento AS nombre,
                    SUM(CASE WHEN TV.tipo = 'valido' THEN 1 ELSE 0 END) AS votos_validos,
                    SUM(CASE WHEN TV.tipo = 'anulado' THEN 1 ELSE 0 END) AS votos_anulados,
                    SUM(CASE WHEN TV.tipo = 'blanco' THEN 1 ELSE 0 END) AS votos_blanco,
                    SUM(CASE WHEN V.es_observado = 1 THEN 1 ELSE 0 END) AS votos_observados
                FROM VOTO V
                JOIN TIPOVOTO TV ON V.id_tipo_voto = TV.id
                JOIN CIRCUITO C ON V.id_circuito = C.id
                JOIN ESTABLECIMIENTO E ON C.id_establecimiento = E.id
                JOIN ZONA Z ON E.id_zona = Z.id
                GROUP BY Z.departamento
            """
        elif categoria == "lista":
            query = """
                SELECT CONCAT(valor_lista) AS nombre,
                    SUM(CASE WHEN TV.tipo = 'valido' THEN 1 ELSE 0 END) AS votos_validos,
                    SUM(CASE WHEN TV.tipo = 'anulado' THEN 1 ELSE 0 END) AS votos_anulados,
                    SUM(CASE WHEN TV.tipo = 'blanco' THEN 1 ELSE 0 END) AS votos_blanco,
                    SUM(CASE WHEN V.es_observado = 1 THEN 1 ELSE 0 END) AS votos_observados
                FROM VOTO V
                JOIN TIPOVOTO TV ON V.id_tipo_voto = TV.id
                GROUP BY valor_lista, id_partido
            """
        elif categoria == "partidos":
            query = """
                SELECT P.nombre AS nombre,
                    SUM(CASE WHEN TV.tipo = 'valido' THEN 1 ELSE 0 END) AS votos_validos,
                    SUM(CASE WHEN TV.tipo = 'anulado' THEN 1 ELSE 0 END) AS votos_anulados,
                    SUM(CASE WHEN TV.tipo = 'blanco' THEN 1 ELSE 0 END) AS votos_blanco,
                    SUM(CASE WHEN V.es_observado = 1 THEN 1 ELSE 0 END) AS votos_observados
                FROM VOTO V
                JOIN TIPOVOTO TV ON V.id_tipo_voto = TV.id
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
