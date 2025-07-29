from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.Experiment import Experiment


class MethodRelations(EntityRelations):
    """Relations of a Method with other entities"""

    _datasets: Optional[EntityRelation["Dataset"]] = None
    _experiments: Optional[EntityRelation["Experiment"]] = None

    @property
    def datasets(self) -> Optional[EntityRelation["Dataset"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        from LOGS.Entities.Datasets import Datasets

        self._datasets = self._entityConverter(value, Datasets)

    @property
    def experiments(self) -> Optional[EntityRelation["Experiment"]]:
        return self._experiments

    @experiments.setter
    def experiments(self, value):
        from LOGS.Entities.Experiments import Experiments

        self._experiments = self._entityConverter(value, Experiments)
