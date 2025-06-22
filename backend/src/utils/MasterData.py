from typing import List, Dict, Optional
from services.orm_casero.CRUDBase import CRUDBase
from model.tipos.TipoEleccion import TipoEleccion
from model.tipos.TipoCandidato import TipoCandidato
from model.tipos.TipoVoto import TipoVoto


class MasterData:
    def __init__(self):
        self.tipo_eleccion_crud = CRUDBase(TipoEleccion, "TIPOELECCION", "id")
        self.tipo_candidato_crud = CRUDBase(TipoCandidato, "TIPOCANDIDATO", "id")
        self.tipo_voto_crud = CRUDBase(TipoVoto, "TIPOVOTO", "id")
    
    # TipoEleccion methods
    def get_all_tipos_eleccion(self) -> List[Dict]:
        """Get all election types"""
        return self.tipo_eleccion_crud.get_all()
    
    def get_tipo_eleccion_by_id(self, id: int) -> Optional[Dict]:
        """Get election type by id"""
        return self.tipo_eleccion_crud.get_by_id(id)
    
    def get_tipo_eleccion_by_name(self, tipo: str) -> Optional[Dict]:
        """Get election type by name"""
        return self.tipo_eleccion_crud.get_by_field("tipo", tipo)
    
    # TipoCandidato methods
    def get_all_tipos_candidato(self) -> List[Dict]:
        """Get all candidate types"""
        return self.tipo_candidato_crud.get_all()
    
    def get_tipo_candidato_by_id(self, id: int) -> Optional[Dict]:
        """Get candidate type by id"""
        return self.tipo_candidato_crud.get_by_id(id)
    
    def get_tipo_candidato_by_name(self, tipo: str) -> Optional[Dict]:
        """Get candidate type by description"""
        return self.tipo_candidato_crud.get_by_field("tipo", tipo)
    
    # TipoVoto methods
    def get_all_tipos_voto(self) -> List[Dict]:
        """Get all vote types"""
        return self.tipo_voto_crud.get_all()
    
    def get_tipo_voto_by_id(self, id: int) -> Optional[Dict]:
        """Get vote type by id"""
        return self.tipo_voto_crud.get_by_id(id)
    
    def get_tipo_voto_by_name(self, tipo: str) -> Optional[Dict]:
        """Get vote type by name"""
        return self.tipo_voto_crud.get_by_field("tipo", tipo)
    
    def get_tipo_eleccion_id_by_name(self, tipo: str) -> Optional[int]:
        """Get just the ID of an election type by name"""
        result = self.get_tipo_eleccion_by_name(tipo)
        return result['id'] if result else None
    
    def get_tipo_candidato_id_by_name(self, tipo: str) -> Optional[int]:
        """Get just the ID of a candidate type by description"""
        result = self.get_tipo_candidato_by_name(tipo)
        return result['id'] if result else None
    
    def get_tipo_voto_id_by_name(self, tipo: str) -> Optional[int]:
        """Get just the ID of a vote type by name"""
        result = self.get_tipo_voto_by_name(tipo)
        return result['id'] if result else None