from typing import Optional

from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.LabNotebook import LabNotebook
from LOGS.Entities.LabNotebookModels import LabNotebookStatus
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(LabNotebook)
class LabNotebookMinimal(EntityMinimalWithIntId[LabNotebook]):
    _status: Optional[LabNotebookStatus] = None

    @property
    def status(self) -> Optional[LabNotebookStatus]:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = self.checkAndConvertNullable(value, LabNotebookStatus, "status")
