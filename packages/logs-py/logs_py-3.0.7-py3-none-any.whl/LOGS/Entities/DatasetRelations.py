from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
    from LOGS.Entities.Project import Project


class DatasetRelations(EntityRelations):
    """Relations of a Dataset with other entities"""

    _labNotebookEntries: Optional[EntityRelation["LabNotebookEntry"]] = None
    _projects: Optional[EntityRelation["Project"]] = None

    @property
    def labNotebookEntries(self) -> Optional[EntityRelation]:
        return self._labNotebookEntries

    @labNotebookEntries.setter
    def labNotebookEntries(self, value):
        self._labNotebookEntries = self.checkAndConvertNullable(
            value, EntityRelation, "labNotebookEntries"
        )

    @property
    def projects(self) -> Optional[EntityRelation]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = self.checkAndConvertNullable(value, EntityRelation, "projects")
