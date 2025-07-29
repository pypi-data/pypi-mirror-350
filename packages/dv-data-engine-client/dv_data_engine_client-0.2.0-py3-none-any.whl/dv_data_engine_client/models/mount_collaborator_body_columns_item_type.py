from enum import Enum


class MountCollaboratorBodyColumnsItemType(str, Enum):
    BOOLEAN = "BOOLEAN"
    DOUBLE = "DOUBLE"
    INTEGER = "INTEGER"
    TIMESTAMP = "TIMESTAMP"
    VARCHAR = "VARCHAR"

    def __str__(self) -> str:
        return str(self.value)
