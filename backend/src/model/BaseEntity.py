from typing import List, Self


class BaseEntity:
    table_name: str = ""
    values_needed: list[str] = []
    primary_key: str = "id"

    @classmethod
    def crud(cls):
        from services.orm_casero.CRUDBase import CRUDBase
        return CRUDBase(
            model_class=cls,
            table_name=cls.table_name,
            primary_key=cls.primary_key
        )

    def insert(self) -> Self | None:
        """Insert this entity instance into the database"""
        return self.crud().insert(self)

    def update(self, filter_value) -> Self | None:
        """Update this entity instance in the database"""
        return self.crud().update(self, filter_value)

    def delete(self, filter_value) -> bool:
        """Delete this entity instance from the database"""
        return self.crud().delete(filter_value)

    @classmethod
    def get_by_id(cls, id_value) -> Self | None:
        """Get an entity by its ID"""
        return cls.crud().get_by_id(id_value)

    @classmethod
    def get_by_field(cls, field_name, field_value) -> Self | None:
        """Get an entity by a specific field"""
        return cls.crud().get_by_field(field_name, field_value)

    @classmethod
    def get_all(cls) -> List[Self]:
        """Get all entities"""
        return cls.crud().get_all()

    @classmethod
    def get_multiple_by_field(cls, field_name, field_value) -> List[Self]:
        """Get multiple entities by a specific field"""
        return cls.crud().get_multiple_by_field(field_name, field_value)
