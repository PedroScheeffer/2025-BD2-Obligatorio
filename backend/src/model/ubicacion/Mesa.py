from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel


# CREATE TABLE MESA (
#     id INTEGER AUTO_INCREMENT PRIMARY KEY,
#     id_circuito INTEGER NOT NULL,
#     cc_vocal VARCHAR(15) NOT NULL,
#     cc_secretario VARCHAR(15) NOT NULL,
#     cc_presidente VARCHAR(15) NOT NULL,

#     FOREIGN KEY (id_circuito) REFERENCES CIRCUITO(id) ON DELETE CASCADE,
#     FOREIGN KEY (cc_vocal) REFERENCES VOCAL(cc_persona),
#     FOREIGN KEY (cc_secretario) REFERENCES SECRETARIO(cc_persona),
#     FOREIGN KEY (cc_presidente) REFERENCES PRESIDENTE(cc_persona)
# );

class MesaSchema(BaseModel):
    id: Optional[int]
    id_circuito: int
    cc_vocal: str
    cc_secretario: str
    cc_presidente: str


class Mesa(BaseModel):
    table_name = "MESA"
    values_needed = [
        "id",
        "id_circuito",
        "cc_vocal",
        "cc_secretario",
        "cc_presidente"
    ]

    def __init__(self, id: int, id_circuito: int, cc_vocal: str, cc_secretario: str, cc_presidente: str):
        self.id = id
        self.id_circuito = id_circuito
        self.cc_vocal = cc_vocal
        self.cc_secretario = cc_secretario
        self.cc_presidente = cc_presidente

    def insert(self) -> bool:
        try:
            script, params = Querier.create_insert_script(
                entity=self,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params)
            return status
        except Exception as e:
            print(f"Error inserting Mesa: {e}")
            return False

    def update(self) -> bool:
        try:
            script, params = Querier.create_update_script(
                entity=self,
                filter_key="id",
                filter_value=self.id,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params)
            return status
        except Exception as e:
            print(f"Error updating Mesa: {e}")
            return False

    def delete(self) -> bool:
        try:
            script, params = Querier.create_delete_script(
                filter_key="id",
                filter_value=self.id,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params)
            return status
        except Exception as e:
            print(f"Error deleting Mesa: {e}")
            return False
