from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union, cast

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList
from LOGS.Entities.SampleRelations import SampleRelations
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.Project import Project
    from LOGS.Entities.ProjectMinimal import ProjectMinimal


@Endpoint("samples")
class Sample(
    IEntityWithIntId,
    INamedEntity,
    IOwnedEntity,
    IModificationRecord,
    ICreationRecord,
    IProjectBased,
    IRelatedEntity[SampleRelations],
    ITypedEntity,
    IUniqueEntity,
    ISoftDeletable,
    GenericPermissionEntity,
):
    _relationType = SampleRelations

    _discarded: Optional[bool] = None
    _discardedAt: Optional[datetime] = None
    _discardedBy: Optional[List["PersonMinimal"]] = None
    _notes: Optional[str] = None
    _preparedAt: Optional[datetime] = None
    _preparedBy: Optional[List["PersonMinimal"]] = None
    _sequenceNumber: Optional[int] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: str = "",
        preparedAt: Optional[datetime] = None,
        preparedBy: Optional[List["PersonMinimal"]] = None,
        projects: Optional[List[Union["ProjectMinimal", "Project"]]] = None,
    ):
        self._name = name
        self._preparedAt = preparedAt
        self._preparedBy = preparedBy
        self._projects = cast(Optional[List["ProjectMinimal"]], projects)

        if ref != None and isinstance(ref, (str, int, float)):
            ref = {"text": str(ref)}

        super().__init__(connection=connection, id=id, ref=ref)

    @property
    def fullName(self) -> Optional[str]:
        return self._fullName

    @fullName.setter
    def fullName(self, value):
        self._fullName = self.checkAndConvertNullable(value, str, "fullName")

    @property
    def createdAt(self) -> Optional[datetime]:
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.checkAndConvertNullable(value, datetime, "createdAt")

    @property
    def preparedAt(self) -> Optional[datetime]:
        return self._preparedAt

    @preparedAt.setter
    def preparedAt(self, value):
        self._preparedAt = self.checkAndConvert(value, datetime, "preparedAt")

    @property
    def discarded(self) -> Optional[bool]:
        return self._discarded

    @discarded.setter
    def discarded(self, value):
        self._discarded = self.checkAndConvertNullable(value, bool, "discarded")

    @property
    def discardedAt(self) -> Optional[datetime]:
        return self._discardedAt

    @discardedAt.setter
    def discardedAt(self, value):
        self._discardedAt = self.checkAndConvertNullable(value, datetime, "discardedAt")

    # @property
    # def discarded(self) -> Optional[bool]:
    #     return self._discarded

    # @discarded.setter
    # def discarded(self, value):
    #     self._discarded = self.checkAndConvertNullable(value, bool, "discarded")

    @property
    def other(self) -> Optional[str]:
        return self._other

    @other.setter
    def other(self, value):
        self._other = self.checkAndConvertNullable(value, str, "other")

    @property
    def preparedBy(self) -> Optional[List["PersonMinimal"]]:
        return self._preparedBy

    @preparedBy.setter
    def preparedBy(self, value):
        self._preparedBy = MinimalFromList(
            value, "PersonMinimal", "preparedBy", connection=self.connection
        )

    @property
    def discardedBy(self) -> Optional[List["PersonMinimal"]]:
        return self._discardedBy

    @discardedBy.setter
    def discardedBy(self, value):
        self._discardedBy = MinimalFromList(
            value, "PersonMinimal", "discardedBy", connection=self.connection
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def sequenceNumber(self) -> Optional[int]:
        return self._sequenceNumber

    @sequenceNumber.setter
    def sequenceNumber(self, value):
        self._sequenceNumber = self.checkAndConvertNullable(
            value, int, "sequenceNumber"
        )
