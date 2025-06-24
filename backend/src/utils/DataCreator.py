import json
from typing import List, Union
from model.schemas.Direccion import DireccionSchema
from model.relacion.CandidatoLista import CandidatoLista
from faker import Faker
from random import choice, randint
from datetime import date, timedelta
from model.personas.Persona import Persona
from model.personas.Policia import Policia
from model.personas.Votante import Votante
from model.personas.Funcionario import Funcionario
from model.personas.Presidente import Presidente
from model.personas.Secretario import Secretario
from model.personas.Vocal import Vocal
from model.personas.Candidato import Candidato
from model.Partido import Partido
from model.Lista import Lista
from model.Eleccion import Eleccion
from model.Voto import Voto
from model.ubicacion.Zona import Zona
from model.ubicacion.Establecimiento import Establecimiento, EstablecimientoSchema
from model.ubicacion.Circuito import Circuito
from model.ubicacion.Mesa import Mesa
from model.tipos.TipoCandidato import TipoCandidatoEnum
from model.tipos.TipoEleccion import TipoEleccionEnum
from model.tipos.TipoVoto import TipoVotoEnum

fake = Faker('es_ES')

# --- ZONA ---


def create_random_zona() -> Zona:
    # Use province() if available, else fallback to state() or a US state
    if hasattr(fake, "province"):
        departamento = fake.province()
    elif hasattr(fake, "state"):
        departamento = fake.state()
    else:
        # fallback to en_US state
        fake_en = Faker('en_US')
        departamento = fake_en.state()
    return Zona(
        id=None,
        paraje=fake.word(),
        ciudad=fake.city(),
        departamento=departamento,
        municipio=fake.city()
    )


def create_and_insert_zonas(n: int = 5) -> List[int]:
    zonas = []
    ids = []
    for _ in range(n):
        zona = create_random_zona()
        zona.crud().insert(zona)
        zonas.append(zona)
        ids.append(zona.id)
    return ids

# --- ESTABLECIMIENTO ---


def create_random_establecimiento(zona_id: int) -> Establecimiento:
    direccion = DireccionSchema(
        calle=fake.street_name(),
        numero=fake.building_number(),
        ciudad=fake.city(),
        departamento=fake.city(),
        codigo_postal=fake.postcode()
    )
    schema = EstablecimientoSchema(
        id=None,
        tipo=fake.word(),
        direccion=direccion,
        id_zona=zona_id)
    return Establecimiento(**schema.model_dump())


def create_and_insert_establecimientos(zonas_ids: List[int], n: int = 10) -> List[int]:
    ids = []
    for _ in range(n):
        z_id = choice(zonas_ids)
        est = create_random_establecimiento(z_id)
        est.crud().insert(est)
        ids.append(est.id)
    return ids

# --- PERSONA ---


def create_random_persona() -> Persona:
    cc = fake.bothify(text='??? #####')
    ci = fake.random_number(digits=8, fix_len=True)
    nombre = fake.name()
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=90)
    fecha_nacimiento_str = fecha_nacimiento.strftime(
        '%Y-%m-%d')  # Convert to string
    return Persona(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento_str)


def create_and_insert_personas(n: int = 20) -> List[str]:
    personas = []
    ccs = []
    for _ in range(n):
        persona = create_random_persona()
        persona.crud().insert(persona)
        personas.append(persona)
        ccs.append(persona.cc)
    return ccs

# --- PARTIDO ---


def create_random_partido() -> Partido:
    nombre = fake.company()
    direccion_sede = {
        "calle": fake.street_name(),
        "numero": fake.building_number(),
        "barrio": fake.city(),
        "entre_calles": f"{fake.street_name()} y {fake.street_name()}"
    }
    # Convert dict to JSON string
    import json
    direccion_sede_json = json.dumps(direccion_sede)
    return Partido(id=None, nombre=nombre, direccion_sede=direccion_sede_json)


def create_and_insert_partidos(n: int = 5) -> List[int]:
    partidos = []
    ids = []
    for _ in range(n):
        partido = create_random_partido()
        partido.crud().insert(partido)
        partidos.append(partido)
        ids.append(partido.id)
    return ids

# --- ELECCION ---


def create_random_eleccion() -> Eleccion:
    fecha = fake.date_between(start_date='-5y', end_date='+1y')
    fecha_str = fecha.strftime('%Y-%m-%d')  # Convert to string format
    tipo = randint(1, 5)  # Assuming 5 types in master data
    return Eleccion(id=None, fecha=fecha_str, id_tipo_eleccion=tipo)


def create_and_insert_elecciones(n: int = 5) -> List[int]:
    elecciones = []
    ids = []
    for _ in range(n):
        eleccion = create_random_eleccion()
        eleccion.crud().insert(eleccion)
        elecciones.append(eleccion)
        ids.append(eleccion.id)
    return ids

# --- CIRCUITO ---


def create_random_circuito(est_id: int, eleccion_id: int, tipo_eleccion_id: int) -> Circuito:
    return Circuito(
        id=None,
        accesibilidad=fake.boolean(),
        id_establecimiento=est_id,
        id_eleccion=eleccion_id,
        id_tipo_eleccion=tipo_eleccion_id
    )


def create_and_insert_circuitos(est_ids: List[int], eleccion_ids: List[int], tipo_eleccion_ids: List[int], n: int = 10) -> List[int]:
    ids = []
    for _ in range(n):
        circuito = create_random_circuito(
            choice(est_ids),
            choice(eleccion_ids),
            choice(tipo_eleccion_ids)
        )
        circuito.crud().insert(circuito)
        ids.append(circuito.id)
    return ids

# --- MESA ---


def create_random_mesa(circuito_id: int, vocal_cc: str, secretario_cc: str, presidente_cc: str) -> Mesa:
    return Mesa(
        id=None,
        id_circuito=circuito_id,
        cc_vocal=vocal_cc,
        cc_secretario=secretario_cc,
        cc_presidente=presidente_cc
    )


def create_and_insert_mesas(circuito_ids: List[int], vocal_ccs: List[str], secretario_ccs: List[str], presidente_ccs: List[str], n: int = 10) -> List[int]:
    mesas = []
    ids = []
    for _ in range(n):
        mesa = create_random_mesa(
            choice(circuito_ids),
            choice(vocal_ccs),
            choice(secretario_ccs),
            choice(presidente_ccs)
        )
        mesa.crud().insert(mesa)
        mesas.append(mesa)
        ids.append(mesa.id)
    return ids

# --- VOTANTE ---


def create_random_votante(cc_persona: str, circuito_id: int) -> Votante:
    return Votante(
        cc_persona=cc_persona,
        voto=fake.boolean(),
        id_circuito=circuito_id
    )


def create_and_insert_votantes(persona_ccs: List[str], circuito_ids: List[int], n: int = 10) -> List[str]:
    votantes = []
    ccs = []
    for _ in range(n):
        votante = create_random_votante(
            choice(persona_ccs),
            choice(circuito_ids)
        )
        votante.crud().insert(votante)
        votantes.append(votante)
        ccs.append(votante.cc_persona)
    return ccs

# --- POLICIA ---


def create_random_policia(cc_persona: str, est_id: int) -> Policia:
    return Policia(
        cc_persona=cc_persona,
        comisaria=fake.word(),
        fk_id_establecimiento=est_id
    )


def create_and_insert_policias(persona_ccs: List[str], est_ids: List[int], n: int = 5) -> List[str]:
    policias = []
    ccs = []
    for _ in range(n):
        policia = create_random_policia(
            choice(persona_ccs),
            choice(est_ids)
        )
        policia.crud().insert(policia)
        policias.append(policia)
        ccs.append(policia.cc_persona)
    return ccs

# --- FUNCIONARIO ---


def create_random_funcionario(cc_persona: str) -> Funcionario:
    return Funcionario(cc_persona=cc_persona)


def create_and_insert_funcionarios(persona_ccs: List[str], n: int = 5) -> List[str]:
    funcionarios = []
    ccs = []
    for _ in range(n):
        funcionario = create_random_funcionario(choice(persona_ccs))
        funcionario.crud().insert(funcionario)
        funcionarios.append(funcionario)
        ccs.append(funcionario.cc_persona)
    return ccs

# --- PRESIDENTE ---


def create_random_presidente(cc_persona: str) -> Presidente:
    return Presidente(cc_persona=cc_persona)


def create_and_insert_presidentes(funcionario_ccs: List[str], n: int = 2) -> List[str]:
    presidentes = []
    ccs = []
    for _ in range(n):
        presidente = create_random_presidente(choice(funcionario_ccs))
        presidente.crud().insert(presidente)
        presidentes.append(presidente)
        ccs.append(presidente.cc_persona)
    return ccs

# --- SECRETARIO ---


def create_random_secretario(cc_persona: str) -> Secretario:
    return Secretario(cc_persona=cc_persona)


def create_and_insert_secretarios(funcionario_ccs: List[str], n: int = 2) -> List[str]:
    secretarios = []
    ccs = []
    for _ in range(n):
        secretario = create_random_secretario(choice(funcionario_ccs))
        secretario.crud().insert(secretario)
        secretarios.append(secretario)
        ccs.append(secretario.cc_persona)
    return ccs

# --- VOCAL ---


def create_random_vocal(cc_persona: str) -> Vocal:
    return Vocal(cc_persona=cc_persona)


def create_and_insert_vocales(funcionario_ccs: List[str], n: int = 2) -> List[str]:
    vocales = []
    ccs = []
    for _ in range(n):
        vocal = create_random_vocal(choice(funcionario_ccs))
        vocal.crud().insert(vocal)
        vocales.append(vocal)
        ccs.append(vocal.cc_persona)
    return ccs

# --- CANDIDATO ---


def create_random_candidato(cc_persona: str) -> Candidato:
    tipo = randint(1, 4)  # Assuming 4 types in master data
    return Candidato(cc_persona=cc_persona, id_tipo=tipo)


def create_and_insert_candidatos(persona_ccs: List[str], n: int = 5) -> List[str]:
    candidatos = []
    ccs = []
    for _ in range(n):
        candidato = create_random_candidato(choice(persona_ccs))
        candidato.crud().insert(candidato)
        candidatos.append(candidato)
        ccs.append(candidato.cc_persona)
    return ccs

# --- LISTA ---


def create_random_lista(partido_id: int, eleccion_id: int) -> Lista:
    return Lista(
        valor=randint(1, 9999),
        id_partido=partido_id,
        id_eleccion=eleccion_id
    )


def create_and_insert_listas(partido_ids: List[int], eleccion_ids: List[int], n: int = 5) -> List[tuple]:
    pk_tuples = []
    for _ in range(n):
        lista = create_random_lista(
            choice(partido_ids),
            choice(eleccion_ids)
        )
        lista.crud().insert(lista)
        pk_tuples.append((lista.valor, lista.id_partido, lista.id_eleccion))
    return pk_tuples

# --- VOTO ---


def create_random_voto(lista: Lista, circuito_id: int) -> Voto:
    fecha = fake.date_between(start_date='-5y', end_date='today')
    fecha_str = fecha.strftime('%Y-%m-%d')  # Convert to string
    return Voto(
        id=None,
        valor_lista=lista.valor,
        id_partido=lista.id_partido,
        id_eleccion=lista.id_eleccion,
        es_observado=fake.boolean(),
        id_tipo_voto=randint(1, 3),  # Assuming 3 types in master data
        id_circuito=circuito_id,
        fecha=fecha_str
    )


def create_and_insert_votos(listas: List[tuple], circuito_ids: List[int], n: int = 10) -> List[int]:
    ids = []
    for _ in range(n):
        valor, id_partido, id_eleccion = choice(listas)
        lista_obj = Lista(valor=valor, id_partido=id_partido,
                          id_eleccion=id_eleccion)
        voto = create_random_voto(lista_obj, choice(circuito_ids))
        voto.crud().insert(voto)
        ids.append(voto.id)
    return ids


# --- CANDIDATO_LISTA ---


def create_random_candidato_lista(cc_persona: str, lista: Lista) -> CandidatoLista:
    return CandidatoLista(
        cc_persona=cc_persona,
        valor_lista=lista.valor,
        id_partido=lista.id_partido,
        id_eleccion=lista.id_eleccion
    )


def create_and_insert_candidato_listas(persona_ccs: List[str], listas: List[tuple], n: int = 5) -> List[str]:
    ccs = []
    for _ in range(n):
        valor, id_partido, id_eleccion = choice(listas)
        lista_obj = Lista(valor=valor, id_partido=id_partido,
                          id_eleccion=id_eleccion)
        candidato_lista = create_random_candidato_lista(
            choice(persona_ccs), lista_obj)
        candidato_lista.crud().insert(candidato_lista)
        ccs.append(candidato_lista.cc_persona)
    return ccs
