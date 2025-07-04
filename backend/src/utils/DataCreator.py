import json
from typing import List, Union
from model.schemas.Direccion import DireccionSchema
from model.relacion.CandidatoLista import CandidatoLista
from faker import Faker
from random import choice, randint
from datetime import date, timedelta
from model.personas.Persona import Persona, PersonaSchema
from model.personas.Policia import Policia, PoliciaSchema
from model.personas.Votante import Votante
from model.personas.Funcionario import Funcionario, FuncionarioSchema
from model.personas.Presidente import Presidente, PresidenteSchema
from model.personas.Secretario import Secretario, SecretarioSchema
from model.personas.Vocal import Vocal
from model.personas.Candidato import Candidato, CandidatoSchema
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
        persona.insert()
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


def create_random_circuito(est_id: int, eleccion_id: int) -> Circuito:
    return Circuito(
        id=None,
        accesibilidad=fake.boolean(),
        id_establecimiento=est_id,
        id_eleccion=eleccion_id
    )


def create_and_insert_circuitos(est_ids: List[int], eleccion_ids: List[int], n: int = 10) -> List[int]:
    ids = []
    for _ in range(n):
        circuito = create_random_circuito(
            choice(est_ids),
            choice(eleccion_ids)
        )
        circuito.insert()
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


def create_random_votante(cc: str, circuito_id: int) -> Votante:
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__

    return Votante(
        voto=fake.boolean(),
        id_circuito=circuito_id,
        **persona_dict
    )


def create_and_insert_votantes(persona_ccs: List[str], circuito_ids: List[int], n: int = 10) -> List[str]:
    votantes = []
    ccs = []
    # Ensure there are circuits to assign votantes to
    if not circuito_ids:
        print("Warning: No circuit IDs provided to create_and_insert_votantes. Skipping.")
        return ccs
    if not persona_ccs:
        print("Warning: No persona_ccs provided to create_and_insert_votantes. Skipping.")
        return ccs

    for _ in range(n):
        votante = create_random_votante(
            choice(persona_ccs),
            choice(circuito_ids)
        )
        votante.insert()
        votantes.append(votante)
        ccs.append(votante.cc)
    return ccs

# --- POLICIA ---


def create_random_policia(cc: str, est_id: int) -> Policia:
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__
    persona_validated = PersonaSchema.model_validate(persona_dict).model_dump()

    return Policia(
        comisaria=fake.word(),
        fk_id_establecimiento=est_id,
        **persona_validated
    )


def create_and_insert_policias(persona_ccs: List[str], est_ids: List[int], n: int = 5) -> List[str]:
    policias = []
    ccs = []
    if not persona_ccs:
        print("Warning: No persona_ccs provided to create_and_insert_policias. Skipping.")
        return ccs
    if not est_ids:
        print("Warning: No est_ids provided to create_and_insert_policias. Skipping.")
        return ccs
    for _ in range(n):
        policia = create_random_policia(
            choice(persona_ccs),
            choice(est_ids),
        )
        policia.crud().insert(policia)
        policias.append(policia)
        ccs.append(policia.cc)
    return ccs

# --- FUNCIONARIO ---


def create_random_funcionario(cc: str) -> Funcionario:
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__
    persona_validated = PersonaSchema.model_validate(persona_dict).model_dump()

    return Funcionario(**persona_validated)


def create_and_insert_funcionarios(persona_ccs: List[str], n: int = 5) -> List[str]:
    funcionarios = []
    ccs = []
    if not persona_ccs:
        print(
            "Warning: No persona_ccs provided to create_and_insert_funcionarios. Skipping.")
        return ccs
    for _ in range(n):
        funcionario = create_random_funcionario(choice(persona_ccs))
        funcionario.insert()
        funcionarios.append(funcionario)
        ccs.append(funcionario.cc)
    return ccs

# --- PRESIDENTE ---


def create_random_presidente(cc: str) -> Presidente:
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__
    persona_validated = PersonaSchema.model_validate(persona_dict).model_dump()

    return Presidente(**persona_validated)


def create_and_insert_presidentes(funcionario_ccs: List[str], n: int = 2) -> List[str]:
    presidentes = []
    ccs = []
    if not funcionario_ccs:
        print("Warning: No funcionario_ccs provided to create_and_insert_presidentes. Skipping.")
        return ccs
    for _ in range(n):
        presidente = create_random_presidente(choice(funcionario_ccs))
        presidente.crud().insert(presidente)
        presidentes.append(presidente)
        ccs.append(presidente.cc)
    return ccs

# --- SECRETARIO ---


def create_random_secretario(cc: str) -> Secretario:
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__
    persona_validated = PersonaSchema.model_validate(persona_dict).model_dump()

    return Secretario(**persona_validated)


def create_and_insert_secretarios(funcionario_ccs: List[str], n: int = 2) -> List[str]:
    secretarios = []
    ccs = []
    if not funcionario_ccs:
        print("Warning: No funcionario_ccs provided to create_and_insert_secretarios. Skipping.")
        return ccs
    for _ in range(n):
        secretario = create_random_secretario(choice(funcionario_ccs))
        secretario.crud().insert(secretario)
        secretarios.append(secretario)
        ccs.append(secretario.cc)
    return ccs

# --- VOCAL ---


def create_random_vocal(cc: str) -> Vocal:
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__
    return Vocal(**persona_dict)


def create_and_insert_vocales(funcionario_ccs: List[str], n: int = 2) -> List[str]:
    vocales = []
    ccs = []
    if not funcionario_ccs:
        print(
            "Warning: No funcionario_ccs provided to create_and_insert_vocales. Skipping.")
        return ccs
    for _ in range(n):
        vocal = create_random_vocal(choice(funcionario_ccs))
        vocal.crud().insert(vocal)
        vocales.append(vocal)
        ccs.append(vocal.cc)
    return ccs

# --- CANDIDATO ---


def create_random_candidato(cc: str) -> Candidato:
    tipo = randint(1, 4)  # Assuming 4 types in master data
    persona = Persona.get_by_id(cc)  # Ensure the persona exists
    if not persona:
        raise ValueError(f"Persona with cc {cc} does not exist.")
    persona_dict = persona.__dict__
    persona_validated = CandidatoSchema.model_validate(
        persona_dict).model_dump()

    return Candidato(**persona_validated, id_tipo=tipo)


def create_and_insert_candidatos(persona_ccs: List[str], n: int = 5) -> List[str]:
    candidatos = []
    ccs = []
    if not persona_ccs:
        print("Warning: No persona_ccs provided to create_and_insert_candidatos. Skipping.")
        return ccs
    for _ in range(n):
        candidato = create_random_candidato(choice(persona_ccs))
        candidato.crud().insert(candidato)
        candidatos.append(candidato)
        ccs.append(candidato.cc)
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


def create_random_candidato_lista(cc: str, lista: Lista) -> CandidatoLista:
    return CandidatoLista(
        cc=cc,
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
        ccs.append(candidato_lista.cc)
    return ccs
