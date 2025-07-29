from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList, MinimalFromSingle
from LOGS.Entities.InventoryRelations import InventoryRelations
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IHierarchyType import IHierarchyType
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.InventoryMinimal import InventoryMinimal


@Endpoint("inventories")
class Inventory(
    IEntityWithIntId,
    INamedEntity,
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
    ISoftDeletable,
    IRelatedEntity[InventoryRelations],
    ITypedEntity,
    IProjectBased,
    IHierarchyType,
    GenericPermissionEntity,
):
    _relationType = InventoryRelations

    _rootCustomType: Optional["InventoryMinimal"] = None
    _isRootItem: Optional[bool] = None
    _isHierarchyItem: Optional[bool] = None
    _isDeleted: Optional[bool] = None
    _ancestors: Optional[List["InventoryMinimal"]] = None
    _parent: Optional["InventoryMinimal"] = None

    @property
    def rootCustomType(self) -> Optional["InventoryMinimal"]:
        return self._rootCustomType

    @rootCustomType.setter
    def rootCustomType(self, value):
        self._rootCustomType = MinimalFromSingle(
            value, "InventoryMinimal", "rootCustomType"
        )

    @property
    def isRootItem(self) -> Optional[bool]:
        return self._isRootItem

    @isRootItem.setter
    def isRootItem(self, value):
        self._isRootItem = self.checkAndConvertNullable(value, bool, "isRootItem")

    @property
    def isHierarchyItem(self) -> Optional[bool]:
        return self._isHierarchyItem

    @isHierarchyItem.setter
    def isHierarchyItem(self, value):
        self._isHierarchyItem = self.checkAndConvertNullable(
            value, bool, "isHierarchyItem"
        )

    @property
    def isDeleted(self) -> Optional[bool]:
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, value):
        self._isDeleted = self.checkAndConvertNullable(value, bool, "isDeleted")

    @property
    def ancestors(self) -> Optional[List["InventoryMinimal"]]:
        return self._ancestors

    @ancestors.setter
    def ancestors(self, value):
        self._ancestors = MinimalFromList(value, "InventoryMinimal", "ancestors")

    @property
    def parent(self) -> Optional["InventoryMinimal"]:
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = MinimalFromSingle(value, "InventoryMinimal", "parent")
