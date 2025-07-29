from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary import Tools
from LOGS.Auxiliary.MinimalModelGenerator import PersonMinimalFromDict
from LOGS.Interfaces.IEntityInterface import IEntityInterface

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


class ICreatedOnRequest:
    createdFrom: Optional[datetime] = None
    createdTo: Optional[datetime] = None


class ICreatedByRequest:
    createdByIds: Optional[List[int]]


@dataclass
class ICreationRecordRequest(ICreatedOnRequest, ICreatedByRequest):
    createdFrom: Optional[datetime] = None
    createdTo: Optional[datetime] = None


class ICreatedOn(IEntityInterface):
    _createdOn: Optional[datetime] = None

    @property
    def createdOn(self) -> Optional[datetime]:
        return self._createdOn

    @createdOn.setter
    def createdOn(self, value):
        self._createdOn = Tools.checkAndConvert(
            value, datetime, "createdOn", allowNone=True
        )


class ICreatedBy(IEntityInterface):
    _createdBy: Optional["PersonMinimal"] = None

    @property
    def createdBy(self) -> Optional["PersonMinimal"]:
        return self._createdBy

    @createdBy.setter
    def createdBy(self, value):
        self._createdBy = PersonMinimalFromDict(
            value, "createdBy", self._getEntityConnection()
        )


class ICreationRecord(ICreatedOn, ICreatedBy):
    pass
