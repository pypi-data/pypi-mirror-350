from typing import TYPE_CHECKING, Any, Optional, Sequence, Union, cast

from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.CustomFieldModels import CustomFieldValueType

if TYPE_CHECKING:
    from LOGS.Entities.CustomFieldValue import CustomFieldValue, CustomSectionValue


class CustomFieldValueConverter:
    @classmethod
    def convert(
        cls,
        value: Any,
        fieldName: Optional[str] = None,
    ) -> Optional[Sequence[Union["CustomFieldValue", "CustomSectionValue"]]]:
        from LOGS.Entities.CustomFieldValue import CustomFieldValue, CustomSectionValue

        if value is None:
            return None

        if isinstance(value, list):
            g = [cls.convert(v, f"{fieldName}[{i}]") for i, v in enumerate(value)]
            return cast(Any, g)

        if isinstance(value, CustomFieldValue):
            return cast(Any, value)

        if isinstance(value, CustomSectionValue):
            if value.content:
                value.content = [
                    cls.convert(v, f"{fieldName}.content[{i}]")
                    for i, v in enumerate(value.content)
                ]
            return cast(Any, value)

        if isinstance(value, dict):
            if "type" not in value:
                raise Exception(
                    "Field %a cannot be converted because field 'type' is missing."
                    % (fieldName)
                )

            t = Tools.checkAndConvert(
                value["type"],
                CustomFieldValueType,
                fieldName,
            )
            if t == CustomFieldValueType.CustomField:
                return cast(
                    Any, Tools.checkAndConvert(value, CustomFieldValue, fieldName)
                )
            elif t == CustomFieldValueType.CustomTypeSection:
                return cast(
                    Any, Tools.checkAndConvert(value, CustomSectionValue, fieldName)
                )

            if isinstance(value, CustomFieldValue):
                return cast(Any, value)

            if isinstance(value, CustomSectionValue):
                if value.content:
                    value.content = [
                        cls.convert(v, f"{fieldName}.content[{i}]")
                        for i, v in enumerate(value.content)
                    ]
                return cast(Any, value)

            raise Exception(
                "Field %a cannot contain element of type %a."
                % (fieldName, type(value).__name__)
            )

        return None
