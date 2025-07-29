from typing import List, Optional, cast

from LOGS.Auxiliary.Exceptions import EntityNotConnectedException
from LOGS.Entity.SerializableContent import SerializableContent
from LOGS.LOGSConnection import LOGSConnection


class ConnectedEntity(SerializableContent):
    _connection: Optional[LOGSConnection]
    _endpoint: Optional[List[str]] = None
    _uiEndpoint: Optional[List[str]] = None
    _noSerialize = ["connection", "cachePath", "cacheId", "cacheDir"]
    _cacheDir: Optional[str] = None
    _cacheId: str = cast(str, None)

    def __init__(self, ref=None, connection: Optional[LOGSConnection] = None):
        self._connection = connection

        if not self._uiEndpoint and self._endpoint and len(self._endpoint) == 1:
            self._uiEndpoint = ["#" + self._endpoint[0]]

        super().__init__(ref=ref)

    def _getConnection(self):
        if not self._connection:
            raise EntityNotConnectedException(self)
        return self._connection

    def _getConnectionData(self):
        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for of entity type %a."
                % (
                    type(self).__name__
                    if type(self).__name__ != ConnectedEntity.__name__
                    else "unknown"
                )
            )

        return self._getConnection(), self._endpoint

    def clearCache(self):
        raise NotImplementedError(
            "Clearing cache of %a class is not implemented." % type(self).__name__
        )

    @property
    def connection(self) -> Optional[LOGSConnection]:
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = self.checkAndConvertNullable(
            value, LOGSConnection, "connection"
        )
        # print("set connection %a -> %a" % (type(self).__name__, type(self.connection).__name__))
        for k in self.__dict__:
            a = getattr(self, k)
            if issubclass(type(a), ConnectedEntity):
                # print("  => set connection %a" % (type(a).__name__, type(self.connection).__name__))
                cast(ConnectedEntity, a).connection = self.connection

    @property
    def identifier(self):
        return "%s" % (type(self).__name__)

    @property
    def cacheDir(self) -> Optional[str]:
        return self._cacheDir

    @cacheDir.setter
    def cacheDir(self, value):
        self._cacheDir = self.checkAndConvertNullable(value, str, "cacheDir")

    @property
    def cacheId(self) -> str:
        if self._cacheId is None:
            if not hasattr(self, "id"):
                setattr(self, "id", self.generateID())

            return f"{type(self).__name__}_{str(getattr(self, 'id'))}"
        else:
            return self._cacheId
