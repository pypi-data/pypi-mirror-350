from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
    from LOGS.Entities.Sample import Sample

    # public EntityRelation LabNotebooks { get; set; }
    # public EntityRelation LabNotebookExperiments { get; set; }
    # public EntityRelation LabNotebooksEntries { get; set; }
    # public EntityRelation LabNotebooksEntryMentions { get; set; }


class PersonRelations(EntityRelations):
    """Relations of a Person with other entities"""

    _datasets: Optional[EntityRelation["Dataset"]] = None
    _samples: Optional[EntityRelation["Sample"]] = None
    _labNotebooksEntries: Optional[EntityRelation["LabNotebookEntry"]] = None
    _labNotebooksEntryMentions: Optional[EntityRelation["LabNotebookEntry"]] = None

    @property
    def samples(self) -> Optional[EntityRelation["Sample"]]:
        return self._samples

    @samples.setter
    def samples(self, value):
        from LOGS.Entities.Samples import Samples

        self._samples = self._entityConverter(value, Samples)

    @property
    def datasets(self) -> Optional[EntityRelation["Dataset"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        from LOGS.Entities.Datasets import Datasets

        self._datasets = self._entityConverter(value, Datasets)

    @property
    def labNotebooksEntries(self) -> Optional[EntityRelation["LabNotebookEntry"]]:
        return self._labNotebooksEntries

    @labNotebooksEntries.setter
    def labNotebooksEntries(self, value):
        from LOGS.Entities import LabNotebookEntries

        self._labNotebooksEntries = self._entityConverter(value, LabNotebookEntries)

    @property
    def labNotebooksEntryMentions(self) -> Optional[EntityRelation["LabNotebookEntry"]]:
        return self._labNotebooksEntryMentions

    @labNotebooksEntryMentions.setter
    def labNotebooksEntryMentions(self, value):
        from LOGS.Entities import LabNotebookEntries

        self._labNotebooksEntryMentions = self._entityConverter(
            value, LabNotebookEntries
        )
