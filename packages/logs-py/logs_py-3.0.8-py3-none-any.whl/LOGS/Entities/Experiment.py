from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MethodMinimalFromDict
from LOGS.Entities.ExperimentRelations import ExperimentRelations
from LOGS.Entities.MethodMinimal import MethodMinimal
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("experiments")
class Experiment(
    IEntityWithIntId,
    INamedEntity,
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
    IOwnedEntity,
    IRelatedEntity[ExperimentRelations],
    GenericPermissionEntity,
):
    _relationType = ExperimentRelations

    _method: Optional[MethodMinimal]
    _notes: Optional[str]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._method = None
        self._notes = None

        super().__init__(ref=ref, id=id, connection=connection)

    def toDict(self):
        d = super().toDict()

        if self.method:
            d["measurementMethodId"] = self.method.id

        return d

    @property
    def method(self) -> Optional[MethodMinimal]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")
