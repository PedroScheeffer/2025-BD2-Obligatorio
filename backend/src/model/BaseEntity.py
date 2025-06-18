class BaseEntity:
    table_name = None
    values_needed = []
    primary_key = "id"

    @classmethod
    def crud(cls):
        from services.orm_casero.CRUDBase import CRUDBase
        return CRUDBase(
            model_class=cls,
            table_name=cls.table_name,
            primary_key=cls.primary_key
        )
