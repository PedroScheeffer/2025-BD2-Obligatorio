from fastapi import APIRouter, HTTPException, Header, Depends, Request, logger
from typing import Optional
from config.logger import logger
# servicios.
from model.personas.Persona import PersonaSchema
from services.PersonaService import PersonaService
from services.VotoService import VotoService
from services.ResultadoService import ResultadosService
from services.VerVotantesService import VerVotantesService

# MODEL PARA CHECKEAR CONEXIÓN A LA BASE DE DATOS.
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner

from services.CircuitoService import CircuitoService
from services.ListaService import ListaService
from services.EleccionesService import EleccionesService
from services.CandidatoService import CandidatoService
from config.db import get_connection
from model.Eleccion import EleccionConCircuitosSchema

# Crea un router para organizar las rutas
router = APIRouter()

# Dependency to get headers for authentication


async def get_auth_headers(
    correo: Optional[str] = Header(None),
    contrasena: Optional[str] = Header(None)
):
    return {"correo": correo, "contrasena": contrasena}

# PRINCIPAL.


@router.get("/")
async def home():
    return {"message": "Aplicacion de votos"}

# PARA CHECKEAR CONEXIÓN A LA BASE DE DATOS.


@router.get("/ping")
async def check_database_connection():
    status = MySQLScriptRunner.get_database_connection_status()

    if status:
        return {"message": "Conexión exitosa a la base de datos"}
    else:
        raise HTTPException(
            status_code=500, detail="Conexión NO exitosa a la base de datos")


# PERSONA
@router.get("/personas/{cc}")
async def get_persona_by_cc(cc: str, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.get_persona_by_cc(cc, headers)
    except Exception as e:
        logger.error(f"Error getting persona by CC {cc}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/personas")
async def get_all_personas(headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.get_all_personas(headers)
    except Exception as e:
        logger.error(f"Error getting all personas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personas")
async def create_persona(persona_data: PersonaSchema):
    try:
        return PersonaService.create_persona(persona_data)
    except Exception as e:
        logger.error(f"Error creating persona: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/personas/{cc}")
async def update_persona(cc: str, persona_data: PersonaSchema, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.update_persona(cc, persona_data, headers)
    except Exception as e:
        logger.error(f"Error updating persona with CC {cc}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/personas/{cc}")
async def delete_persona(cc: str, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.delete_persona(cc, headers)
    except Exception as e:
        logger.error(f"Error deleting persona with CC {cc}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/circuitos")
async def registrar_circuito(circuito_data: dict):
    try:
        exito = CircuitoService.registrar_circuito(circuito_data)
        if exito:
            return {"message": "Circuito registrado correctamente"}
        else:
            raise HTTPException(
                status_code=500, detail="No se pudo registrar el circuito")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/elecciones-con-circuitos", response_model=list[EleccionConCircuitosSchema])
async def get_elecciones_con_circuitos():
    try:
        return EleccionesService.get_all_elecciones_con_circuitos()
    except Exception as e:
        logger.error(f"Error getting elecciones con circuitos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/listas")
async def registrar_lista(lista_data: dict):
    from services.ListaService import ListaService
    if ListaService.registrar_lista(lista_data):
        return {"message": "Lista registrada exitosamente"}
    else:
        raise HTTPException(
            status_code=400, detail="Error al registrar la lista")


@router.post("/elecciones")
async def crear_eleccion(data: dict):
    try:
        exito = EleccionesService.registrar_eleccion(data)
        if exito:
            return {"message": "Elección registrada correctamente"}
        else:
            raise HTTPException(
                status_code=500, detail="No se pudo registrar la elección")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/candidatos")
async def registrar_candidato(candidato_data: dict):
    try:
        exito = CandidatoService.registrar_candidato(candidato_data)
        if exito:
            return {"message": "Candidato registrado correctamente"}
        else:
            raise HTTPException(
                status_code=500, detail="No se pudo registrar el candidato")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(request: Request):
    data = await request.json()
    cc = data.get("credencial")
    contrasena = data.get("contrasena")
    rol = data.get("rol")

    try:
        result = PersonaService.login(cc, contrasena, rol)
        return result
    except Exception as e:
        logger.error(f"Error en login con cc={cc}, rol={rol}: {e}")
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/opciones-voto/{id_tipo_eleccion}")
async def obtener_opciones(id_tipo_eleccion: int):
    try:
        opciones = VotoService.obtener_opciones(id_tipo_eleccion)
        return opciones
    except Exception as e:
        print("Error en obtener_opciones_voto:", str(e))
        raise HTTPException(
            status_code=500, detail=f"Error obteniendo opciones: {e}")


@router.post("/votos")
async def registrar_voto(voto_data: dict):
    try:
        resultado = VotoService.registrar_voto(voto_data)
        return {"message": "Voto registrado con éxito"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error al registrar voto: {e}")


@router.get("/resultados/{categoria}")
def get_resultados(categoria: str):
    try:
        print(f"Categoría solicitada: {categoria}")
        resultados = ResultadosService.obtener_resultados(categoria)
        print(f"Resultados obtenidos: {resultados}")
        return resultados
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("Error en get_resultados:", str(e))
        raise HTTPException(
            status_code=500, detail="Error al obtener resultados")


@router.get("/partidos")
def obtener_partidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre FROM PARTIDO")
    partidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return partidos


@router.get("/votantes/circuito/{id_circuito}")
def get_votantes(id_circuito: int):
    return VerVotantesService.obtener_votantes_por_circuito(id_circuito)


@router.get("/{id_eleccion}/circuitos")
def get_circuitos(id_eleccion: int):
    try:
        return CircuitoService.get_circuitos_by_eleccion(id_eleccion)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(
            f"Error al obtener circuitos para la elección {id_eleccion}: {e}")
        raise HTTPException(
            status_code=500, detail="Error interno del servidor")
