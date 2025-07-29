from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.LabNotebookModels import LabNotebookStatus
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.IVersionedEntity import IVersionedEntity


@Endpoint("lab_notebooks")
class LabNotebook(
    IEntityWithIntId,
    INamedEntity,
    GenericPermissionEntity,
    IVersionedEntity,
    IProjectBased,
):
    _description: Optional[str] = None
    _status: Optional[LabNotebookStatus] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def status(self) -> Optional[LabNotebookStatus]:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = self.checkAndConvertNullable(value, LabNotebookStatus, "status")
