from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from contextlib import asynccontextmanager


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
    create_and_insert_candidato_listas
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Only for dev/demo! Remove or guard for production!
    zonas = create_and_insert_zonas(5)
    establecimientos = create_and_insert_establecimientos(zonas, 10)
    personas = create_and_insert_personas(20)
    partidos = create_and_insert_partidos(5)
    elecciones = create_and_insert_elecciones(2)
    cant_circuito_mesas = 10
    circuitos = create_and_insert_circuitos(
        establecimientos, zonas, elecciones, [1, 2, 3, 4, 5], cant_circuito_mesas)
    mesas = create_and_insert_mesas(
        circuitos, personas, personas, personas, cant_circuito_mesas)
    votantes = create_and_insert_votantes(personas, circuitos, 10)
    policias = create_and_insert_policias(personas, establecimientos, zonas, 5)
    funcionarios = create_and_insert_funcionarios(personas, 5)
    presidentes = create_and_insert_presidentes(funcionarios, 2)
    secretarios = create_and_insert_secretarios(funcionarios, 2)
    vocales = create_and_insert_vocales(funcionarios, 2)
    candidatos = create_and_insert_candidatos(personas, 5)
    listas = create_and_insert_listas(
        partidos, elecciones, [1, 2, 3, 4, 5], 5)
    votos = create_and_insert_votos(listas, circuitos, 10)
    candidato_listas = create_and_insert_candidato_listas(personas, listas, 5)
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
