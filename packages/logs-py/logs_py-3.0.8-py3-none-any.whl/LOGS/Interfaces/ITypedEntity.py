from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Sequence, Union

from LOGS.Auxiliary import Tools
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromSingle
from LOGS.Entities.CustomFieldValue import (
    CustomFieldValue,
    CustomSectionValue,
    ICustomValue,
)
from LOGS.Entities.CustomFieldValueConverter import CustomFieldValueConverter
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.CustomTypeMinimal import CustomTypeMinimal


@dataclass
class ITypedEntityRequest:
    includeCustomFields: Optional[List[bool]] = None


class ITypedEntity(IEntityInterface):
    _customType: Optional["CustomTypeMinimal"] = None
    _customValues: Optional[
        Sequence[Union["CustomFieldValue", "CustomSectionValue"]]
    ] = None

    def _customValueConverter(self, value):
        return Tools.checkListAndConvert(
            value, ICustomValue, "customValues", allowNone=True
        )

    @property
    def customType(self) -> Optional["CustomTypeMinimal"]:
        return self._customType

    @customType.setter
    def customType(self, value):
        self._customType = MinimalFromSingle(value, "CustomTypeMinimal", "customType")

    @property
    def customValues(
        self,
    ) -> Optional[
        Union[
            Sequence[Union["CustomFieldValue", "CustomSectionValue"]],
            Union["CustomFieldValue", "CustomSectionValue"],
        ]
    ]:
        return self._customValues

    @customValues.setter
    def customValues(self, value):
        self._customValues = CustomFieldValueConverter.convert(value, "customValues")

    def _extractCustomFieldValue(
        self,
        value: Union[
            CustomFieldValue,
            CustomSectionValue,
            Sequence[Union[CustomFieldValue, CustomSectionValue]],
        ],
    ) -> List[CustomFieldValue]:
        if isinstance(value, list):
            result: List[CustomFieldValue] = []
            for v in value:
                result += self._extractCustomFieldValue(v)
            return result
        if isinstance(value, CustomFieldValue):
            return [value]
        if isinstance(value, CustomSectionValue):
            if value.content:
                return self._extractCustomFieldValue(value.content)

        return []

    @property
    def customFieldValues(
        self,
    ) -> Optional[List["CustomFieldValue"]]:
        if self.customValues == None:
            return None

        return self._extractCustomFieldValue(self.customValues)
