from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Optional

from LOGS.Auxiliary import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    pass


@dataclass
class ICustomFieldsRequest:
    includeCustomFields: Optional[bool] = None
    customFields: Optional[Dict[str, Any]] = None


class ICustomFields(IEntityInterface):
    _customFields: Optional[Dict[str, Any]] = None

    @property
    def customFields(self) -> Optional[Dict[str, Any]]:
        return self._customFields

    @customFields.setter
    def customFields(self, value):
        self._customFields = Tools.checkAndConvert(
            value, dict, "customFields", allowNone=True
        )
