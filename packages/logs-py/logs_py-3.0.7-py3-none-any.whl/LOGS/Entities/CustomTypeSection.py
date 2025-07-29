from typing import List, Optional

from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.ILiterarTypedEntity import ILiterarTypedEntity
from LOGS.Entity.SerializableContent import SerializableContent


class CustomTypeSection(SerializableContent, ILiterarTypedEntity):
    _name: Optional[str] = None
    _isFolded: Optional[bool] = None
    _customFields: Optional[List[CustomField]] = None

    _type = "CustomTypeSection"

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def isFolded(self) -> Optional[bool]:
        return self._isFolded

    @isFolded.setter
    def isFolded(self, value):
        self._isFolded = self.checkAndConvertNullable(value, bool, "isFolded")

    @property
    def customFields(self) -> Optional[List[CustomField]]:
        return self._customFields

    @customFields.setter
    def customFields(self, value):
        self._customFields = self.checkListAndConvertNullable(
            value, CustomField, "customFields"
        )
