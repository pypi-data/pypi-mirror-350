from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Person import Person


class RoleRelations(EntityRelations):
    """Relations of a Role with other entities"""

    _persons: Optional[EntityRelation["Person"]] = None

    @property
    def persons(self) -> Optional[EntityRelation["Person"]]:
        return self._persons

    @persons.setter
    def persons(self, value):
        from LOGS.Entities.Persons import Persons

        self._persons = self._entityConverter(value, Persons)
