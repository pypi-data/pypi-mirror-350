from typing import Optional
from uuid import UUID

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("origins")
class Origin(IEntityWithIntId, INamedEntity, IModificationRecord, ICreationRecord):
    _url: Optional[str]
    _uid: Optional[UUID]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        uid: Optional[UUID] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        self._name = name
        self._url = url
        self._createdOn = None
        self._createdBy = None
        self._modifiedOn = None
        self._modifiedBy = None
        self._uid = uid

        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def url(self) -> Optional[str]:
        return self._url

    @url.setter
    def url(self, value):
        self._url = self.checkAndConvertNullable(value, str, "url")

    @property
    def uid(self) -> Optional[UUID]:
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = self.checkAndConvertNullable(value, UUID, "uid")
