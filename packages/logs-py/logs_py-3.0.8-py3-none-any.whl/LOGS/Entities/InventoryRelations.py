from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    pass


class InventoryRelations(EntityRelations):
    """Relations of a Inventory with other entities"""

    _labNotebookEntries: Optional[EntityRelation] = None

    @property
    def labNotebookEntries(self) -> Optional[EntityRelation]:
        return self._labNotebookEntries

    @labNotebookEntries.setter
    def labNotebookEntries(self, value):
        self._labNotebookEntries = self.checkAndConvertNullable(
            value, EntityRelation, "labNotebookEntries"
        )
