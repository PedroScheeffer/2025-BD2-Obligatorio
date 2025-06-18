from typing import List
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
from model.ubicacion.Establecimiento import Establecimiento
from model.ubicacion.Circuito import Circuito
from model.ubicacion.Mesa import Mesa
from model.tipos.TipoCandidato import TipoCandidatoEnum
from model.tipos.TipoEleccion import TipoEleccionEnum
from model.tipos.TipoVoto import TipoVotoEnum

fake = Faker('es_ES')

# --- ZONA ---


def create_random_zona():
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


def create_and_insert_zonas(n=5):
    zonas = []
    for _ in range(n):
        zona = create_random_zona()
        zona.crud().insert(zona)
        zonas.append(zona)
    return zonas

# --- ESTABLECIMIENTO ---


def create_random_establecimiento(zona_id):
    direccion = {
        "calle": fake.street_name(),
        "numero": fake.building_number(),
        "barrio": fake.city(),
        "entre_calles": f"{fake.street_name()} y {fake.street_name()}"
    }
    return Establecimiento(
        id=None,
        tipo=fake.word(),
        direccion=direccion,
        id_zona=zona_id
    )


def create_and_insert_establecimientos(zonas, n=10):
    establecimientos = []
    for _ in range(n):
        zona = choice(zonas)
        est = create_random_establecimiento(zona.id)
        est.crud().insert(est)
        establecimientos.append(est)
    return establecimientos

# --- PERSONA ---


def create_random_persona():
    cc = fake.bothify(text='??? #####')
    ci = fake.random_number(digits=8, fix_len=True)
    nombre = fake.name()
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=90)
    fecha_nacimiento_str = fecha_nacimiento.strftime(
        '%Y-%m-%d')  # Convert to string
    return Persona(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento_str)


def create_and_insert_personas(n=20):
    personas = []
    for _ in range(n):
        persona = create_random_persona()
        persona.crud().insert(persona)
        personas.append(persona)
    return personas

# --- PARTIDO ---


def create_random_partido():
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


def create_and_insert_partidos(n=5):
    partidos = []
    for _ in range(n):
        partido = create_random_partido()
        partido.crud().insert(partido)
        partidos.append(partido)
    return partidos

# --- ELECCION ---


def create_random_eleccion():
    fecha = fake.date_between(start_date='-5y', end_date='+1y')
    fecha_str = fecha.strftime('%Y-%m-%d')  # Convert to string format
    tipo = randint(1, 5)  # Assuming 5 types in master data
    return Eleccion(id=None, fecha=fecha_str, id_tipo_eleccion=tipo)


def create_and_insert_elecciones(n=5):
    elecciones = []
    for _ in range(n):
        eleccion = create_random_eleccion()
        eleccion.crud().insert(eleccion)
        elecciones.append(eleccion)
    return elecciones

# --- CIRCUITO ---


def create_random_circuito(est_id, zona_id, eleccion_id, tipo_eleccion_id):
    return Circuito(
        id=None,
        accesibilidad=fake.boolean(),
        id_establecimiento=est_id,
        id_zona=zona_id,
        id_eleccion=eleccion_id,
        id_tipo_eleccion=tipo_eleccion_id
    )


def create_and_insert_circuitos(est_ids, zona_ids, eleccion_ids, tipo_eleccion_ids, n=10):
    circuitos = []
    for _ in range(n):
        circuito = create_random_circuito(
            choice(est_ids),
            choice(zona_ids),
            choice(eleccion_ids),
            choice(tipo_eleccion_ids)
        )
        circuito.crud().insert(circuito)
        circuitos.append(circuito)
    return circuitos

# --- MESA ---


def create_random_mesa(circuito_id, vocal_cc, secretario_cc, presidente_cc):
    return Mesa(
        id=None,
        id_circuito=circuito_id,
        cc_vocal=vocal_cc,
        cc_secretario=secretario_cc,
        cc_presidente=presidente_cc
    )


def create_and_insert_mesas(circuito_ids, vocal_ccs, secretario_ccs, presidente_ccs, n=10):
    mesas = []
    for _ in range(n):
        mesa = create_random_mesa(
            choice(circuito_ids),
            choice(vocal_ccs),
            choice(secretario_ccs),
            choice(presidente_ccs)
        )
        mesa.crud().insert(mesa)
        mesas.append(mesa)
    return mesas

# --- VOTANTE ---


def create_random_votante(cc_persona: str, circuito_id):
    return Votante(
        cc_persona=cc_persona,
        voto=fake.boolean(),
        id_circuito=circuito_id
    )


def create_and_insert_votantes(persona_ccs: List[str], circuito_ids, n=10):
    votantes = []
    for _ in range(n):
        votante = create_random_votante(
            choice(persona_ccs),
            choice(circuito_ids)
        )
        votante.crud().insert(votante)
        votantes.append(votante)
    return votantes

# --- POLICIA ---


def create_random_policia(cc_persona, est_id, zona_id):
    return Policia(
        cc_persona=cc_persona,
        comisaria=fake.word(),
        fk_id_establecimiento=est_id,
        fk_id_zona=zona_id
    )


def create_and_insert_policias(persona_ccs, est_ids, zona_ids, n=5):
    policias = []
    for _ in range(n):
        policia = create_random_policia(
            choice(persona_ccs),
            choice(est_ids),
            choice(zona_ids)
        )
        policia.crud().insert(policia)
        policias.append(policia)
    return policias

# --- FUNCIONARIO ---


def create_random_funcionario(cc_persona):
    return Funcionario(cc_persona=cc_persona)


def create_and_insert_funcionarios(persona_ccs, n=5):
    funcionarios = []
    for _ in range(n):
        funcionario = create_random_funcionario(choice(persona_ccs))
        funcionario.crud().insert(funcionario)
        funcionarios.append(funcionario)
    return funcionarios

# --- PRESIDENTE ---


def create_random_presidente(cc_persona):
    return Presidente(cc_persona=cc_persona)


def create_and_insert_presidentes(funcionario_ccs, n=2):
    presidentes = []
    for _ in range(n):
        presidente = create_random_presidente(choice(funcionario_ccs))
        presidente.crud().insert(presidente)
        presidentes.append(presidente)
    return presidentes

# --- SECRETARIO ---


def create_random_secretario(cc_persona):
    return Secretario(cc_persona=cc_persona)


def create_and_insert_secretarios(funcionario_ccs, n=2):
    secretarios = []
    for _ in range(n):
        secretario = create_random_secretario(choice(funcionario_ccs))
        secretario.crud().insert(secretario)
        secretarios.append(secretario)
    return secretarios

# --- VOCAL ---


def create_random_vocal(cc_persona):
    return Vocal(cc_persona=cc_persona)


def create_and_insert_vocales(funcionario_ccs, n=2):
    vocales = []
    for _ in range(n):
        vocal = create_random_vocal(choice(funcionario_ccs))
        vocal.crud().insert(vocal)
        vocales.append(vocal)
    return vocales

# --- CANDIDATO ---


def create_random_candidato(cc_persona):
    tipo = randint(1, 4)  # Assuming 4 types in master data
    return Candidato(cc_persona=cc_persona, id_tipo=tipo)


def create_and_insert_candidatos(persona_ccs, n=5):
    candidatos = []
    for _ in range(n):
        candidato = create_random_candidato(choice(persona_ccs))
        candidato.crud().insert(candidato)
        candidatos.append(candidato)
    return candidatos

# --- LISTA ---


def create_random_lista(partido_id, eleccion_id, tipo_eleccion_id):
    return Lista(
        valor=randint(1, 9999),
        id_partido=partido_id,
        id_eleccion=eleccion_id,
        id_tipo_eleccion=tipo_eleccion_id
    )


def create_and_insert_listas(partido_ids, eleccion_ids, tipo_eleccion_ids, n=5):
    listas = []
    for _ in range(n):
        lista = create_random_lista(
            choice(partido_ids),
            choice(eleccion_ids),
            choice(tipo_eleccion_ids)
        )
        lista.crud().insert(lista)
        listas.append(lista)
    return listas

# --- VOTO ---


def create_random_voto(lista, circuito_id):
    fecha = fake.date_between(start_date='-5y', end_date='today')
    fecha_str = fecha.strftime('%Y-%m-%d')  # Convert to string
    return Voto(
        id=None,
        valor_lista=lista.valor,
        id_partido=lista.id_partido,
        id_eleccion=lista.id_eleccion,
        id_tipo_eleccion=lista.id_tipo_eleccion,
        es_observado=fake.boolean(),
        id_tipo_voto=randint(1, 3),  # Assuming 3 types in master data
        id_circuito=circuito_id,
        fecha=fecha_str
    )


def create_and_insert_votos(listas, circuito_ids, n=10):
    votos = []
    for _ in range(n):
        lista = choice(listas)
        voto = create_random_voto(lista, choice(circuito_ids))
        voto.crud().insert(voto)
        votos.append(voto)
    return votos


# --- CANDIDATO_LISTA ---


def create_random_candidato_lista(cc_persona, lista):
    return CandidatoLista(
        cc_persona=cc_persona,
        valor_lista=lista.valor,
        id_partido=lista.id_partido,
        id_eleccion=lista.id_eleccion,
        id_tipo_eleccion=lista.id_tipo_eleccion
    )


def create_and_insert_candidato_listas(persona_ccs, listas, n=5):
    candidato_listas = []
    for _ in range(n):
        candidato_lista = create_random_candidato_lista(
            choice(persona_ccs), choice(listas))
        candidato_lista.crud().insert(candidato_lista)
        candidato_listas.append(candidato_lista)
    return candidato_listas


# You can call these functions from a main or script section
if __name__ == "__main__":
    zonas = create_and_insert_zonas(5)
    establecimientos = create_and_insert_establecimientos(zonas, 10)
    personas = create_and_insert_personas(20)
    partidos = create_and_insert_partidos(5)
    elecciones = create_and_insert_elecciones(5)
    circuitos = create_and_insert_circuitos(
        [e.id for e in establecimientos], [z.id for z in zonas], [el.id for el in elecciones], [1, 2, 3, 4, 5], 10)
    mesas = create_and_insert_mesas(
        [c.id for c in circuitos], [p.cc for p in personas], [p.cc for p in personas], [p.cc for p in personas], 10)
    votantes = create_and_insert_votantes(
        [p.cc for p in personas], [c.id for c in circuitos], 10)
    policias = create_and_insert_policias([p.cc for p in personas], [
                                          e.id for e in establecimientos], [z.id for z in zonas], 5)
    funcionarios = create_and_insert_funcionarios([p.cc for p in personas], 5)
    presidentes = create_and_insert_presidentes(
        [f.cc_persona for f in funcionarios], 2)
    secretarios = create_and_insert_secretarios(
        [f.cc_persona for f in funcionarios], 2)
    vocales = create_and_insert_vocales(
        [f.cc_persona for f in funcionarios], 2)
    candidatos = create_and_insert_candidatos([p.cc for p in personas], 5)
    listas = create_and_insert_listas([pa.id for pa in partidos], [
                                      el.id for el in elecciones], [1, 2, 3, 4, 5], 5)
    votos = create_and_insert_votos(listas, [c.id for c in circuitos], 10)
    candidato_listas = create_and_insert_candidato_listas(
        [p.cc for p in personas], listas, 5)
