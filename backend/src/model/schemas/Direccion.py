import pydantic
from pydantic import BaseModel, Field, field_validator

class DireccionSchema(BaseModel):
    calle: str = Field(..., description="Nombre de la calle")
    numero: str = Field(..., description="Número de la casa o edificio")
    ciudad: str = Field(..., description="Ciudad donde se encuentra la dirección")
    departamento: str = Field(..., description="Departamento o estado de la dirección")
    codigo_postal: str = Field(..., description="Código postal de la dirección")