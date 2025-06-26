from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
import logging

# servicios.
from model.personas.Persona import PersonaSchema
from services.PersonaService import PersonaService

# MODEL PARA CHECKEAR CONEXIÓN A LA BASE DE DATOS.
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner

from services.CircuitoService import CircuitoService
from services.ListaService import ListaService
from services.EleccionesService import EleccionesService
from services.CandidatoService import CandidatoService

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


## PERSONA 
@router.get("/personas/{cc}")
async def get_persona_by_cc(cc: str, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.get_persona_by_cc(cc, headers)
    except Exception as e:
        logging.error(f"Error getting persona by CC {cc}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/personas")
async def get_all_personas(headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.get_all_personas(headers)
    except Exception as e:
        logging.error(f"Error getting all personas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/personas")
async def create_persona(persona_data: PersonaSchema, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.create_persona(persona_data, headers)
    except Exception as e:
        logging.error(f"Error creating persona: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/personas/{cc}")
async def update_persona(cc: str, persona_data: PersonaSchema, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.update_persona(cc, persona_data, headers)
    except Exception as e:
        logging.error(f"Error updating persona with CC {cc}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/personas/{cc}")
async def delete_persona(cc: str, headers: dict = Depends(get_auth_headers)):
    try:
        return PersonaService.delete_persona(cc, headers)
    except Exception as e:
        logging.error(f"Error deleting persona with CC {cc}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

from services.CircuitoService import CircuitoService  # Asegurate de importar correctamente

@router.post("/circuitos")
async def registrar_circuito(circuito_data: dict):
    try:
        exito = CircuitoService.registrar_circuito(circuito_data)
        if exito:
            return {"message": "Circuito registrado correctamente"}
        else:
            raise HTTPException(status_code=500, detail="No se pudo registrar el circuito")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/listas")
async def crear_lista(data: dict):
    from services.ListaService import ListaService
    if ListaService.registrar_lista(data):
        return {"message": "Lista registrada exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="Error al registrar la lista")


@router.post("/elecciones")
async def crear_eleccion(data: dict):
    try:
        exito = EleccionesService.registrar_eleccion(data)
        if exito:
            return {"message": "Elección registrada correctamente"}
        else:
            raise HTTPException(status_code=500, detail="No se pudo registrar la elección")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/candidatos")
async def registrar_candidato(candidato_data: dict):
    try:
        exito = CandidatoService.registrar_candidato(candidato_data)
        if exito:
            return {"message": "Candidato registrado correctamente"}
        else:
            raise HTTPException(status_code=500, detail="No se pudo registrar el candidato")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))