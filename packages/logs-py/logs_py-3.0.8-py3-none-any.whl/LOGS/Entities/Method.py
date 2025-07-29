from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.MethodRelations import MethodRelations
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity


@Endpoint("methods")
class Method(
    IEntityWithIntId,
    INamedEntity,
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
    IRelatedEntity[MethodRelations],
    GenericPermissionEntity,
):
    _relationType = MethodRelations

    _fullName: Optional[str] = None
    _description: Optional[str] = None

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
