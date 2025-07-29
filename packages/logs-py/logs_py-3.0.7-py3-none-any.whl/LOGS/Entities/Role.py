from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.RoleRelations import RoleRelations
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    pass


@Endpoint("roles")
class Role(
    IEntityWithIntId,
    INamedEntity,
    ICreationRecord,
    IModificationRecord,
    IRelatedEntity[RoleRelations],
    GenericPermissionEntity,
):
    _relationType = RoleRelations

    _roleId: Optional[str] = None
    _description: Optional[str] = None
    _isDefault: Optional[bool]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        if isinstance(ref, str):
            ref = {"roleId": ref}

        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def roleId(self) -> Optional[str]:
        return self._roleId

    @roleId.setter
    def roleId(self, value):
        self._roleId = self.checkAndConvertNullable(value, str, "roleId")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def isDefault(self) -> Optional[bool]:
        return self._isDefault

    @isDefault.setter
    def isDefault(self, value):
        self._isDefault = self.checkAndConvertNullable(value, bool, "isDefault")
