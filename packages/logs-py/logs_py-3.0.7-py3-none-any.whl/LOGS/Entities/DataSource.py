from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import EntityAPIException
from LOGS.Auxiliary.MinimalModelGenerator import (
    BridgeMinimalFromDict,
    FormatMinimalFromDict,
    InstrumentMinimalFromDict,
    MethodMinimalFromDict,
    MinimalFromList,
)
from LOGS.Entities.BridgeMinimal import BridgeMinimal
from LOGS.Entities.DataSourceRelations import DataSourceRelations
from LOGS.Entities.DataSourceStatus import DataSourceStatus
from LOGS.Entities.FileExcludePattern import FileExcludePattern
from LOGS.Entities.Format import Format
from LOGS.Entities.FormatMinimal import FormatMinimal
from LOGS.Entities.InstrumentMinimal import InstrumentMinimal
from LOGS.Entities.MethodMinimal import MethodMinimal
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.LOGSConnection import LOGSConnection


class DataSourceType(Enum):
    Crawler = "Crawler"
    IconNMR = "IconNMR"


@Endpoint("data_sources")
class DataSource(
    IEntityWithIntId,
    INamedEntity,
    ICreationRecord,
    IModificationRecord,
    IRelatedEntity[DataSourceRelations],
    GenericPermissionEntity,
):
    _relationType = DataSourceRelations

    _relations: DataSourceRelations

    _type: Optional[DataSourceType]
    _bridge: Optional[BridgeMinimal]
    _format: Optional[FormatMinimal]
    _customImport: Optional[EntityMinimalWithStrId]
    _enabled: Optional[bool]
    _bridgeId: Optional[int]
    _formats: Optional[List[FormatMinimal]]
    _directories: Optional[List[str]]
    _intervalInSeconds: Optional[int]
    _method: Optional[MethodMinimal]
    _instrument: Optional[InstrumentMinimal]
    _cutoffDate: Optional[datetime]
    _fileExcludePatterns: Optional[List[FileExcludePattern]]
    _formatDefinitions: Optional[Dict[str, Format]]
    _status: Optional[DataSourceStatus]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._type = None
        self._bridge = None
        self._format = None
        self._customImport = None
        self._enabled = None
        self._bridgeId = None
        self._formats = None
        self._directories = None
        self._intervalInSeconds = None
        self._method = None
        self._instrument = None
        self._cutoffDate = None
        self._customImportId = None
        self._status = None

        super().__init__(ref=ref, id=id, connection=connection)

    def triggerAutoload(self):
        connection, endpoint, id = self._getConnectionData()

        _, responseError = connection.getEndpoint(endpoint + [id, "trigger_autoload"])
        if responseError:
            raise EntityAPIException(entity=self, responseError=responseError)

    @property
    def enabled(self) -> Optional[bool]:
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = self.checkAndConvertNullable(value, bool, "enabled")

    @property
    def formats(self) -> Optional[List[FormatMinimal]]:
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = MinimalFromList(
            value, "FormatMinimal", "formats", connection=self.connection
        )

    @property
    def directories(self) -> Optional[List[str]]:
        return self._directories

    @directories.setter
    def directories(self, value):
        self._directories = self.checkListAndConvertNullable(value, str, "directories")

    @property
    def intervalInSeconds(self) -> Optional[int]:
        return self._intervalInSeconds

    @intervalInSeconds.setter
    def intervalInSeconds(self, value):
        self._intervalInSeconds = self.checkAndConvertNullable(
            value, int, "intervalInSeconds"
        )

    @property
    def method(self) -> Optional[MethodMinimal]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(value, "method", self.connection)

    @property
    def instrument(self) -> Optional[InstrumentMinimal]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", self.connection
        )

    @property
    def cutoffDate(self) -> Optional[datetime]:
        return self._cutoffDate

    @cutoffDate.setter
    def cutoffDate(self, value):
        self._cutoffDate = self.checkAndConvertNullable(value, datetime, "cutoffDate")

    @property
    def fileExcludePatterns(self) -> Optional[List[FileExcludePattern]]:
        return self._fileExcludePatterns

    @fileExcludePatterns.setter
    def fileExcludePatterns(self, value):
        self._fileExcludePatterns = self.checkListAndConvertNullable(
            value, FileExcludePattern, "fileExcludePatterns"
        )

    @property
    def customImportId(self) -> Optional[str]:
        return self._customImportId

    @customImportId.setter
    def customImportId(self, value):
        print("customImportId", value)
        self._customImportId = self.checkAndConvertNullable(
            value, str, "customImportId"
        )

    @property
    def status(self) -> Optional[DataSourceStatus]:
        return self._status

    @status.setter
    def status(self, value):
        self._status = self.checkAndConvertNullable(value, DataSourceStatus, "status")

    @property
    def type(self) -> Optional[DataSourceType]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, DataSourceType, "type")

    @property
    def bridge(self) -> Optional[BridgeMinimal]:
        return self._bridge

    @bridge.setter
    def bridge(self, value):
        self._bridge = BridgeMinimalFromDict(value, "bridge", self.connection)

    @property
    def format(self) -> Optional[FormatMinimal]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = FormatMinimalFromDict(value, "format", self.connection)

    @property
    def customImport(self) -> Optional[EntityMinimalWithStrId]:
        return self._customImport

    @customImport.setter
    def customImport(self, value):
        self._customImport = self.checkAndConvertNullable(
            value, EntityMinimalWithStrId, "customImport"
        )
