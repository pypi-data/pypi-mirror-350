from typing import TYPE_CHECKING, List, Optional

from LOGS.Entities.CustomField import CustomField
from LOGS.Entity.SerializableContent import SerializableContent
from LOGS.Interfaces.INamedEntity import INamedEntity

if TYPE_CHECKING:
    pass


class CustomSchemaSection(SerializableContent, INamedEntity):
    _isFolded: Optional[bool]
    _children: Optional[List[CustomField]]

    def __init__(
        self,
        ref=None,
        name: str = "",
    ):
        self._name = name
        self._isFolded = False
        self._children = None

        super().__init__(ref=ref)

    @property
    def isFolded(self) -> Optional[bool]:
        return self._isFolded

    @isFolded.setter
    def isFolded(self, value):
        self._isFolded = self.checkAndConvertNullable(value, bool, "isRequired")

    @property
    def children(self) -> Optional[List[CustomField]]:
        return self._children

    @children.setter
    def children(self, value):
        self._children = self.checkListAndConvertNullable(
            value, CustomField, "children"
        )
