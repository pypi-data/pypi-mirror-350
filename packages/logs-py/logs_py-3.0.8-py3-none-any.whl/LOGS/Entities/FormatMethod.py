from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.FormatMethodMinimal import FormatMethodMinimal


@Endpoint("parser_methods")
class FormatMethod(EntityWithStrId, INamedEntity):
    _fullName: Optional[str]
    _description: Optional[str]
    _parent: Optional[List["FormatMethodMinimal"]]

    def __init__(
        self,
        ref=None,
        id: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        self._fullName = None
        self._description = None
        self._parent = None

        super().__init__(ref=ref, id=id, connection=connection)

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict) and "from" in ref:
            ref["parent"] = ref["from"]

        super().fromDict(ref=ref)

    @property
    def fullName(self) -> Optional[str]:
        return self._fullName

    @fullName.setter
    def fullName(self, value):
        self._fullName = self.checkAndConvertNullable(value, str, "fullName")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def parent(self) -> Optional[List["FormatMethodMinimal"]]:
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = MinimalFromList(
            value, "FormatMethodMinimal", "parent", connection=self.connection
        )
