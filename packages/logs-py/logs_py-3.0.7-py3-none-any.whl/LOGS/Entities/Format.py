from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.FormatMetaData import FormatMetaData
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("parsers")
class Format(INamedEntity, EntityWithStrId):
    _formatVersion: str
    _vendors: List[str]
    _method: List[str]
    _format: List[str]
    _instruments: List[str]
    _metaData: List[FormatMetaData]

    def __init__(
        self,
        ref=None,
        id: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._formatVersion = "0.0"
        self._vendor = []
        self._method = []
        self._format = []
        self._instruments = []
        self._metaData = []

        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def formatVersion(self) -> Optional[str]:
        return self._formatVersion

    @formatVersion.setter
    def formatVersion(self, value):
        self._formatVersion = self.checkAndConvert(value, str, "formatVersion")

    @property
    def vendor(self) -> List[str]:
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = self.checkListAndConvert(value, str, "vendor")

    @property
    def method(self) -> List[str]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = self.checkListAndConvert(value, str, "method")

    @property
    def format(self) -> List[str]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = self.checkListAndConvert(value, str, "format")

    @property
    def instruments(self) -> List[str]:
        return self._instruments

    @instruments.setter
    def instruments(self, value):
        self._instruments = self.checkListAndConvert(value, str, "instruments")

    @property
    def metaData(self) -> List[FormatMetaData]:
        return self._metaData

    @metaData.setter
    def metaData(self, value):
        self._metaData = self.checkListAndConvert(
            value,
            FormatMetaData,
            "metaData",
            converter=lambda ref: FormatMetaData(ref, connection=self.connection),
        )
