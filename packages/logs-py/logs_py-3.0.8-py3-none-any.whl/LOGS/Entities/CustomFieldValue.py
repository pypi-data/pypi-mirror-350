from typing import TYPE_CHECKING, Any, Optional, Sequence, Union, cast

from LOGS.Auxiliary.Exceptions import IllegalFieldValueException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.CustomFieldModels import CustomFieldDataType, CustomFieldValueType
from LOGS.Entities.CustomFieldValueConverter import CustomFieldValueConverter
from LOGS.Entity.SerializableContent import SerializableContent

if TYPE_CHECKING:
    pass


class ICustomValue(SerializableContent):
    _name: Optional[str] = None
    _type: CustomFieldValueType = cast(CustomFieldValueType, None)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def type(self) -> CustomFieldValueType:
        return self._type

    @type.setter
    def type(self, value):
        value = self.checkAndConvert(value, CustomFieldValueType, "type")
        if value != self._type:
            raise IllegalFieldValueException(
                self, "type", value, f"Only value '{self._type}' allowed."
            )


class CustomFieldValue(ICustomValue):
    _type: CustomFieldValueType = CustomFieldValueType.CustomField

    _id: Optional[int] = None
    _dataType: Optional[CustomFieldDataType] = None
    _value: Optional[Any] = None

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, int, "id")

    @property
    def dataType(self) -> Optional[CustomFieldDataType]:
        return self._dataType

    @dataType.setter
    def dataType(self, value):
        self._dataType = self.checkAndConvertNullable(
            value, CustomFieldDataType, "dataType"
        )

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return Tools.ObjectToString(self)


class CustomSectionValue(ICustomValue):
    _type: CustomFieldValueType = CustomFieldValueType.CustomTypeSection

    _content: Optional[Sequence[Union[CustomFieldValue, "CustomSectionValue"]]] = None

    @property
    def content(
        self,
    ) -> Optional[Sequence[Union[CustomFieldValue, "CustomSectionValue"]]]:
        return self._content

    @content.setter
    def content(self, value):
        self._content = CustomFieldValueConverter.convert(value)
