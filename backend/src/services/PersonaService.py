from typing import List, Optional
from model.personas.Persona import Persona, PersonaSchema
from utils.Validator import Validator
from model.personas.Candidato import Candidato, CandidatoSchema
from model.personas.Funcionario import Funcionario, FuncionarioSchema
from model.personas.Policia import Policia, PoliciaSchema
from model.personas.Presidente import Presidente, PresidenteSchema
from model.personas.Secretario import Secretario, SecretarioSchema
from model.personas.Vocal import Vocal, VocalSchema
from model.personas.Votante import Votante, VotanteSchema
from enum import Enum

# Esta clase se encarga de persona y sus genericaciones
class PersonaRol(str, Enum):
    CANDIDATO = "Candidato"
    FUNCIONARIO = "Funcionario"
    POLICIA = "Policia"
    PRESIDENTE = "Presidente"
    SECRETARIO = "Secretario"
    VOCAL = "Vocal"
    VOTANTE = "Votante"


class PersonaService:
    @staticmethod
    def create_persona(persona_data: PersonaSchema, rol, headers: dict) -> dict:
        """Create a new persona with validation"""
        if not Validator.is_admin(headers=headers):
            raise Exception("User is not authorized to create personas")

        existing_persona = Persona.crud().get_by_id(persona_data.cc)
        if existing_persona:
            raise Exception(
                f"Persona with CC {persona_data.cc} already exists")


        persona = Persona(**persona_data.model_dump())
        success = persona.crud().insert()

        if not success:
            raise Exception("Failed to create persona in database")
        return persona

    @staticmethod
    def get_persona_by_cc(cc: str, headers: dict) -> dict:
        """Get persona by cc"""
        if not Validator.is_admin(headers=headers):
            raise Exception("User is not authorized to view personas")

        persona_data = Persona.get_persona(cc)
        if not persona_data:
            raise Exception(f"Persona with CC {cc} not found")

        return persona_data

    @staticmethod
    def get_all_personas(headers: dict) -> List[dict]:
        """Get all personas"""
        if not Validator.is_admin(headers=headers):
            raise Exception("User is not authorized to view personas")

        return Persona.get_all_personas()

    @staticmethod
    def update_persona(cc: str, persona_data: PersonaSchema, headers: dict) -> dict:
        """Update an existing persona"""
        if not Validator.is_admin(headers=headers):
            raise Exception("User is not authorized to update personas")

        # Get existing persona
        existing_persona_data = Persona.get_persona(cc)
        if not existing_persona_data:
            raise Exception(f"Persona with CC {cc} not found")

        # Create updated persona object
        updated_persona = Persona(
            cc=persona_data.cc,
            ci=persona_data.ci,
            nombre=persona_data.nombre,
            fecha_nacimiento=persona_data.fecha_nacimiento
        )

        success = updated_persona.update()
        if not success:
            raise Exception("Failed to update persona in database")

        return {"message": "Persona updated successfully", "cc": updated_persona.cc}

    @staticmethod
    def delete_persona(cc: str, headers: dict) -> dict:
        """Delete a persona"""
        if not Validator.is_admin(headers=headers):
            raise Exception("User is not authorized to delete personas")

        # Get existing persona to create object for deletion
        existing_persona_data = Persona.get_persona(cc)
        if not existing_persona_data:
            raise Exception(f"Persona with CC {cc} not found")

        persona = Persona(
            cc=existing_persona_data["cc"],
            ci=existing_persona_data["ci"],
            nombre=existing_persona_data["nombre"],
            fecha_nacimiento=existing_persona_data["fecha_nacimiento"]
        )

        success = persona.delete()
        if not success:
            raise Exception("Failed to delete persona from database")

        return {"message": "Persona deleted successfully"}
    

        