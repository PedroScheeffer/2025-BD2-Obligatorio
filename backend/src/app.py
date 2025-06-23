from random import choice
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from contextlib import asynccontextmanager
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
import sys
import time

# RUTAS.
from routes import router

# Data creation for dev/demo
from utils.DataCreator import (
    create_and_insert_zonas,
    create_and_insert_establecimientos,
    create_and_insert_personas,
    create_and_insert_partidos,
    create_and_insert_elecciones,
    create_and_insert_circuitos,
    create_and_insert_mesas,
    create_and_insert_votantes,
    create_and_insert_policias,
    create_and_insert_funcionarios,
    create_and_insert_presidentes,
    create_and_insert_secretarios,
    create_and_insert_vocales,
    create_and_insert_candidatos,
    create_and_insert_listas,
    create_and_insert_votos,
    create_and_insert_candidato_listas,
    create_random_lista
)

from config.logger import logger
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Wait for DB connection before any inserts
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        if MySQLScriptRunner.get_database_connection_status():
            break
        logger.warning(
            f"Waiting for database to be online... (attempt {attempt+1}/{max_attempts})")
        attempt += 1
        time.sleep(2 * attempt)  # Exponential backoff
    else:
        print("ERROR: Database is not available after waiting. Exiting app startup.")
        sys.exit(1)

    zonas = create_and_insert_zonas(5)  # List[int]
    establecimientos = create_and_insert_establecimientos(
        zonas, 10)  # List[int]
    personas = create_and_insert_personas(20)  # List[str]
    partidos = create_and_insert_partidos(5)  # List[int]
    elecciones = create_and_insert_elecciones(5)  # List[int]
    circuitos = create_and_insert_circuitos(
        establecimientos, elecciones, [1, 2, 3, 4, 5], 10)  # List[int]
    mesas = create_and_insert_mesas(
        circuitos, personas, personas, personas, 10)  # List[int]
    votantes = create_and_insert_votantes(
        personas, circuitos, 10)  # List[str]
    policias = create_and_insert_policias(
        personas, establecimientos, 5)  # List[str]
    funcionarios = create_and_insert_funcionarios(personas, 5)  # List[str]
    presidentes = create_and_insert_presidentes(
        funcionarios, 2)  # List[str]
    secretarios = create_and_insert_secretarios(
        funcionarios, 2)  # List[str]
    vocales = create_and_insert_vocales(
        funcionarios, 2)  # List[str]
    candidatos = create_and_insert_candidatos(personas, 5)  # List[str]
    # Create Lista objects and their IDs
    lista_objs = []
    for _ in range(5):
        lista = create_random_lista(choice(partidos), choice(elecciones))
        lista.crud().insert(lista)
        lista_objs.append(lista)
    listas_tuples = [(l.valor, l.id_partido, l.id_eleccion)
                     for l in lista_objs]
    votos = create_and_insert_votos(listas_tuples, circuitos, 10)  # List[int]
    candidato_listas = create_and_insert_candidato_listas(
        personas, listas_tuples, 5)  # List[str]

    yield


# Inicialización de la aplicación FastAPI.
app = FastAPI(
    title="API de votaciones",
    description="API for managing voting system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Registro de las rutas
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
