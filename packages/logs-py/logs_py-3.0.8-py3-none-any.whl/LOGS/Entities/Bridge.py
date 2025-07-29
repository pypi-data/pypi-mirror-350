from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import LOGSMultilineException
from LOGS.Entities.AutoloadClientInfo import AutoloadClientInfo
from LOGS.Entities.AutoloadFileInfo import AutoloadFileInfo
from LOGS.Entities.BridgeRelations import BridgeRelations
from LOGS.Entities.BridgeType import BridgeType
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("bridges")
class Bridge(
    IEntityWithIntId,
    INamedEntity,
    IRelatedEntity[BridgeRelations],
    GenericPermissionEntity,
):
    _relationType = BridgeRelations

    _type: Optional[BridgeType]
    _hostname: Optional[str]
    _ipAddress: Optional[str]
    _description: Optional[str]
    _username: Optional[str]
    _port: Optional[int]
    _connectedClients: Optional[List[AutoloadClientInfo]]
    _isConnected: Optional[bool]
    _areMultipleClientsConnected: Optional[bool]

    _password: Optional[str]
    _privateKey: Optional[str]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: str = "",
    ):
        self._type = None
        self._hostname = None
        self._ipAddress = None
        self._description = None
        self._username = None
        self._port = None
        self._connectedClients = None
        self._isConnected = None
        self._areMultipleClientsConnected = None
        self._name = name
        self._password = None
        self._privateKey = None

        super().__init__(connection=connection, id=id, ref=ref)

    def readDirectory(self):
        connection, endpoint, id = self._getConnectionData()

        data, responseError = connection.postEndpoint(endpoint + [id, "read_directory"])
        if responseError:
            raise LOGSMultilineException(responseError=responseError)

        return self.checkListAndConvertNullable(
            data, AutoloadFileInfo, "directory content"
        )

    @property
    def url(self):
        return "{type}://{user}@{host}{port}".format(
            type=str(self.type.name if self.type else "").lower(),
            user=self.username,
            host=self.hostname,
            port=":%d" % self.port if self.port else ":22",
        )

    @property
    def type(self) -> Optional[BridgeType]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, BridgeType, "type")

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        self._hostname = self.checkAndConvertNullable(value, str, "hostname")

    @property
    def ipAddress(self) -> Optional[str]:
        return self._ipAddress

    @ipAddress.setter
    def ipAddress(self, value):
        self._ipAddress = self.checkAndConvertNullable(value, str, "ipAddress")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value):
        self._username = self.checkAndConvertNullable(value, str, "username")

    @property
    def port(self) -> Optional[int]:
        return self._port

    @port.setter
    def port(self, value):
        self._port = self.checkAndConvertNullable(value, int, "port")

    @property
    def connectedClients(self) -> Optional[List[AutoloadClientInfo]]:
        return self._connectedClients

    @connectedClients.setter
    def connectedClients(self, value):
        self._connectedClients = self.checkListAndConvertNullable(
            value, AutoloadClientInfo, "connectedClients"
        )

    @property
    def isConnected(self) -> Optional[bool]:
        return self._isConnected

    @isConnected.setter
    def isConnected(self, value):
        self._isConnected = self.checkAndConvertNullable(value, bool, "isConnected")

    @property
    def areMultipleClientsConnected(self) -> Optional[bool]:
        return self._areMultipleClientsConnected

    @areMultipleClientsConnected.setter
    def areMultipleClientsConnected(self, value):
        self._areMultipleClientsConnected = self.checkAndConvertNullable(
            value, bool, "areMultipleClientsConnected"
        )

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.checkAndConvertNullable(value, str, "password")

    @property
    def privateKey(self) -> Optional[str]:
        return self._privateKey

    @privateKey.setter
    def privateKey(self, value):
        self._privateKey = self.checkAndConvertNullable(value, str, "privateKey")
