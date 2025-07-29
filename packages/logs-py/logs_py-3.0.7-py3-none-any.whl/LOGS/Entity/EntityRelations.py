from typing import Any, Optional, Type, cast

from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.EntityConnector import EntityConnector
from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Interfaces.IRelationModel import IRelationModel
from LOGS.LOGSConnection import LOGSConnection


class EntityRelations(ConnectedEntity, IRelationModel):
    def _entityConverter(self, ref: Any, entityConnector: Type[EntityConnector]):
        result = self.checkAndConvertNullable(
            ref, EntityRelation, fieldName=type(entityConnector).__name__.lower()
        )
        result._entities = cast(Any, entityConnector(connection=self._connection))
        result._entities._firstUrl = result.link
        return result

    @property
    def connection(self) -> Optional[LOGSConnection]:
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = self.checkAndConvertNullable(
            value, LOGSConnection, "connection"
        )
        for k in self.__dict__:
            a = getattr(self, k)
            if issubclass(type(a), EntityRelation):
                e = cast(EntityRelation, a).entities
                if e:
                    e.connection = self.connection
