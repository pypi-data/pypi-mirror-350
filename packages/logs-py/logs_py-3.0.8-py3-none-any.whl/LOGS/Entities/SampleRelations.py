from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset


class SampleRelations(EntityRelations):
    """Relations of a Sample with other entities"""

    _datasets: Optional[EntityRelation["Dataset"]] = None
    _labNotebookEntries: Optional[EntityRelation] = None

    @property
    def datasets(self) -> Optional[EntityRelation["Dataset"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        from LOGS.Entities.Datasets import Datasets

        self._datasets = self._entityConverter(value, Datasets)

    @property
    def labNotebookEntries(self) -> Optional[EntityRelation]:
        return self._labNotebookEntries

    @labNotebookEntries.setter
    def labNotebookEntries(self, value):
        self._labNotebookEntries = self.checkAndConvertNullable(
            value, EntityRelation, "labNotebookEntries"
        )
