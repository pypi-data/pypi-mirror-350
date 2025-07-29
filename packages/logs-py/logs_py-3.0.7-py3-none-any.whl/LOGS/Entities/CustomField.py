from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList
from LOGS.Entities.CustomFieldModels import CustomFieldDataType
from LOGS.Entities.CustomFieldRelations import CustomFieldRelations
from LOGS.Entities.ILiterarTypedEntity import ILiterarTypedEntity
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal


@Endpoint("custom_fields")
class CustomField(
    IEntityWithIntId,
    IOwnedEntity,
    INamedEntity,
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
    IRelatedEntity[CustomFieldRelations],
    ILiterarTypedEntity,
    GenericPermissionEntity,
):
    _relationType = CustomFieldRelations
    _type = "CustomField"

    _customTypeConstraint: Optional[List["CustomTypeMinimal"]] = None
    _dataType: Optional[CustomFieldDataType] = None
    _defaultValue: Optional[str] = None
    _description: Optional[str] = None
    _enumOptions: Optional[List[str]] = None
    _enumOptionsFromValues: Optional[bool] = None
    _placeholder: Optional[str] = None
    _readOnly: Optional[bool] = None
    _required: Optional[bool] = None
    _showAsTextArea: Optional[bool] = None
    _validationMessage: Optional[str] = None
    _validationRegexp: Optional[str] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        if ref != None and isinstance(ref, (str, int, float)):
            ref = {"text": str(ref)}

        super().__init__(connection=connection, id=id, ref=ref)

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict) and "type" in ref and isinstance(ref["type"], int):
            del ref["type"]
        if isinstance(ref, dict) and "widget" in ref and isinstance(ref["widget"], int):
            del ref["widget"]

        super().fromDict(ref=ref)

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def defaultValue(self) -> Optional[str]:
        return self._defaultValue

    @defaultValue.setter
    def defaultValue(self, value):
        self._defaultValue = self.checkAndConvertNullable(value, str, "defaultValue")

    @property
    def readOnly(self) -> Optional[bool]:
        return self._readOnly

    @readOnly.setter
    def readOnly(self, value):
        self._readOnly = self.checkAndConvertNullable(value, bool, "readOnly")

    @property
    def required(self) -> Optional[bool]:
        return self._required

    @required.setter
    def required(self, value):
        self._required = self.checkAndConvertNullable(value, bool, "required")

    @property
    def validationRegexp(self) -> Optional[str]:
        return self._validationRegexp

    @validationRegexp.setter
    def validationRegexp(self, value):
        self._validationRegexp = self.checkAndConvertNullable(
            value, str, "validationRegexp"
        )

    @property
    def validationMessage(self) -> Optional[str]:
        return self._validationMessage

    @validationMessage.setter
    def validationMessage(self, value):
        self._validationMessage = self.checkAndConvertNullable(
            value, str, "validationMessage"
        )

    @property
    def enumOptions(self) -> Optional[List[str]]:
        return self._enumOptions

    @enumOptions.setter
    def enumOptions(self, value):
        if value == None:
            self._enumOptions = None
            return
        self._enumOptions = self.checkListAndConvertNullable(value, str, "enumOptions")

    @property
    def customTypeConstraint(self) -> Optional[List["CustomTypeMinimal"]]:
        return self._customTypeConstraint

    @customTypeConstraint.setter
    def customTypeConstraint(self, value):
        self._customTypeConstraint = MinimalFromList(
            value, "CustomTypeMinimal", "customTypeConstraint"
        )

    @property
    def dataType(self) -> Optional[CustomFieldDataType]:
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = self.checkAndConvertNullable(
            value, CustomFieldDataType, "dataType"
        )

    @property
    def enumOptionsFromValues(self) -> Optional[bool]:
        return self._enumOptionsFromValues

    @enumOptionsFromValues.setter
    def enumOptionsFromValues(self, value):
        self._enumOptionsFromValues = self.checkAndConvertNullable(
            value, bool, "enumOptionsFromValues"
        )

    @property
    def placeholder(self) -> Optional[str]:
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = self.checkAndConvertNullable(value, str, "placeholder")

    @property
    def showAsTextArea(self) -> Optional[bool]:
        return self._showAsTextArea

    @showAsTextArea.setter
    def showAsTextArea(self, value):
        self._showAsTextArea = self.checkAndConvertNullable(
            value, bool, "showAsTextArea"
        )
