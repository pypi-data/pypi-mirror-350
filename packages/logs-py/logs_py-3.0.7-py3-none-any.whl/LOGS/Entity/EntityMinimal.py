from typing import Generic, Optional, Type, TypeVar, cast
from uuid import UUID

from LOGS.Auxiliary.Exceptions import EntityNotConnectedException, LOGSException
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.Entity import Entity
from LOGS.LOGSConnection import LOGSConnection

_FULL_ENTITY = TypeVar("_FULL_ENTITY", bound=Entity)
_ID_TYPE = TypeVar("_ID_TYPE", int, str)


class EntityMinimal(Generic[_ID_TYPE, _FULL_ENTITY], ConnectedEntity):
    _id: Optional[_ID_TYPE]
    _name: Optional[str]
    _fullEntityType: Optional[_FULL_ENTITY] = None
    _uid: Optional[UUID] = None
    _version: Optional[int] = None

    def __init__(
        self,
        ref=None,
        id: Optional[_ID_TYPE] = None,
        name: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""
        self._id = id
        self._name = name
        self._uid = None
        self._version = None

        self._connection = connection
        if isinstance(ref, Entity):
            self._id = cast(_ID_TYPE, ref.id)
            if hasattr(ref, "name"):
                self._name = getattr(ref, "name")
            ref = None
        super().__init__(ref=ref, connection=connection)

    def __str__(self):
        s = " name:'%s'" % (self.name if self.name else "")
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)

    def _fetchEntity(self, connection: LOGSConnection):
        if not self._endpoint:
            raise NotImplementedError(
                "Fetching of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != EntityMinimal.__name__
                    else "unknown"
                )
            )

        if not self._fullEntityType:
            raise LOGSException("Full entity type of %a not set." % type(self).__name__)

        entity = cast(Type[_FULL_ENTITY], self._fullEntityType)(id=self.id)
        entity._connection = connection
        entity.fetch()
        return entity

    def fetchFullEntity(self):
        if not self._connection:
            raise EntityNotConnectedException(cast(Entity, self))
        return self._fetchEntity(self._connection)

    @property
    def identifier(self):
        name = self.name
        return "%s(id:%s) %s" % (
            type(self).__name__,
            str(self.id),
            "'" + name + "'" if name else "",
        )

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvert(value, str, "name", allowNone=True)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def uid(self) -> Optional[UUID]:
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = self.checkAndConvert(value, UUID, "uid", allowNone=True)

    @property
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvert(value, int, "uid", allowNone=True)
