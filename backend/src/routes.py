from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
import logging

# servicios.
from model.personas.Persona import PersonaSchema
from services.PersonaService import PersonaService

# MODEL PARA CHECKEAR CONEXIÓN A LA BASE DE DATOS.
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner

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
        logging.error(f"Error en login con cc={cc}, rol={rol}: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/opciones-voto")
async def obtener_opciones_voto():
    try:
        opciones = VotoService.obtener_opciones()
        return opciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo opciones: {e}")
    
@router.post("/votos")
async def registrar_voto(voto_data: dict):
    try:
        resultado = VotoService.registrar_voto(voto_data)
        return {"message": "Voto registrado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar voto: {e}")

@router.get("/resultados/{categoria}")
def get_resultados(categoria: str):
    try:
        return ResultadosService.obtener_resultados(categoria)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener resultados")