from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.MinimalModelGenerator import PersonMinimalFromDict
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


@dataclass
class IOwnedEntityRequest:
    ownerIds: Optional[List[int]] = None


class IOwnedEntity(IEntityInterface):
    _owner: Optional["PersonMinimal"] = None

    @property
    def owner(self) -> Optional["PersonMinimal"]:
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = PersonMinimalFromDict(value, "owner", self._getEntityConnection())
