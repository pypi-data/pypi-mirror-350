from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity


@Endpoint("parser_formats")
class FormatFormat(INamedEntity, EntityWithStrId):

    _description: Optional[str]
    _formatVersion: Optional[List[str]]
    _isCustom: bool
    _hasVisualization: bool

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def formatVersion(self) -> Optional[List[str]]:
        return self._formatVersion

    @formatVersion.setter
    def formatVersion(self, value):
        self._formatVersion = self.checkListAndConvertNullable(
            value, str, "formatVersion"
        )

    @property
    def isCustom(self) -> Optional[bool]:
        return self._isCustom

    @isCustom.setter
    def isCustom(self, value):
        self._isCustom = self.checkAndConvertNullable(value, bool, "isCustom")

    @property
    def hasVisualization(self) -> Optional[bool]:
        return self._hasVisualization

    @hasVisualization.setter
    def hasVisualization(self, value):
        self._hasVisualization = self.checkAndConvertNullable(
            value, bool, "hasVisualization"
        )
