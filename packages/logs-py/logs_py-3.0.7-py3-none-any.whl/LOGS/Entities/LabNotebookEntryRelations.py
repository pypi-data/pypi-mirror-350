from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
    from LOGS.Entities.Person import Person
    from LOGS.Entities.Project import Project
    from LOGS.Entities.Sample import Sample


class LabNotebookEntryRelations(EntityRelations):
    """Relations of a LabNotebookEntry with other entities"""

    _datasets: Optional[EntityRelation["Dataset"]] = None
    _labNotebookEntries: Optional[EntityRelation["LabNotebookEntry"]] = None
    _persons: Optional[EntityRelation["Person"]] = None
    _samples: Optional[EntityRelation["Sample"]] = None
    _projects: Optional[EntityRelation["Project"]] = None

    @property
    def persons(self) -> Optional[EntityRelation["Person"]]:
        return self._persons

    @persons.setter
    def persons(self, value):
        from LOGS.Entities.Persons import Persons

        self._persons = self._entityConverter(value, Persons)

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

    @property
    def samples(self) -> Optional[EntityRelation["Sample"]]:
        return self._samples

    @samples.setter
    def samples(self, value):
        from LOGS.Entities.Samples import Samples

        self._samples = self._entityConverter(value, Samples)

    @property
    def projects(self) -> Optional[EntityRelation]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = self.checkAndConvertNullable(value, EntityRelation, "projects")
