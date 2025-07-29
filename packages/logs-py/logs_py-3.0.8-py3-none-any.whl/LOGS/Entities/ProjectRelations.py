from typing import Optional

from LOGS.Entities.Dataset import Dataset
from LOGS.Entities.Datasets import Datasets
from LOGS.Entities.Sample import Sample
from LOGS.Entities.Samples import Samples
from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations


class ProjectRelations(EntityRelations):
    """Relations of a Project with other entities"""

    _datasets: Optional[EntityRelation[Dataset]] = None
    _samples: Optional[EntityRelation[Sample]] = None
    _labNotebookEntries: Optional[EntityRelation] = None
    _labNotebooksEntryMentions: Optional[EntityRelation] = None

    @property
    def samples(self) -> Optional[EntityRelation[Sample]]:
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = self._entityConverter(value, Samples)

    @property
    def datasets(self) -> Optional[EntityRelation[Dataset]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
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
    def labNotebooksEntryMentions(self) -> Optional[EntityRelation]:
        return self._labNotebooksEntryMentions

    @labNotebooksEntryMentions.setter
    def labNotebooksEntryMentions(self, value):
        self._labNotebooksEntryMentions = self.checkAndConvertNullable(
            value, EntityRelation, "labNotebooksEntryMentions"
        )
