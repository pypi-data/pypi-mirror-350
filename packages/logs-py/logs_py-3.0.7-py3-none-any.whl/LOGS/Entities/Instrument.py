from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MethodMinimalFromDict
from LOGS.Entities.InstrumentRelations import InstrumentRelations
from LOGS.Entities.MethodMinimal import MethodMinimal
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreatedOn
from LOGS.Interfaces.IModificationRecord import IModifiedOn
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("instruments")
class Instrument(
    IEntityWithIntId,
    IRelatedEntity[InstrumentRelations],
    INamedEntity,
    IOwnedEntity,
    IUniqueEntity,
    ICreatedOn,
    IModifiedOn,
    GenericPermissionEntity,
):
    _relationType = InstrumentRelations

    _serialnumber: Optional[str]
    _room: Optional[str]
    _notes: Optional[str]
    _model: Optional[str]
    _method: Optional[MethodMinimal]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""
        self._method = None
        self._notes = None
        self._serialnumber = None
        self._room = None
        self._model = None

        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def method(self) -> Optional["MethodMinimal"]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def methodId(self) -> Optional[int]:
        return self._method.id if self._method else None

    @methodId.setter
    def methodId(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def serialnumber(self) -> Optional[str]:
        return self._serialnumber

    @serialnumber.setter
    def serialnumber(self, value):
        self._serialnumber = self.checkAndConvertNullable(value, str, "serialnumber")

    @property
    def room(self) -> Optional[str]:
        return self._room

    @room.setter
    def room(self, value):
        self._room = self.checkAndConvertNullable(value, str, "room")

    @property
    def model(self) -> Optional[str]:
        return self._model

    @model.setter
    def model(self, value):
        self._model = self.checkAndConvertNullable(value, str, "model")
