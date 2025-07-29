from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IHierarchyType import IHierarchyTypeRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest


class InventoryOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"
    NUMBER_OF_ITEMS_ASC = "NUMBER_OF_ITEMS_ASC"
    NUMBER_OF_ITEMS_DESC = "NUMBER_OF_ITEMS_DESC"
    TYPE_ASC = "TYPE_ASC"
    TYPE_DESC = "TYPE_DESC"
    INVENTORY_NAME_ASC = "INVENTORY_NAME_ASC"
    INVENTORY_NAME_DESC = "INVENTORY_NAME_DESC"


@dataclass
class InventoryRequestParameter(
    EntityRequestParameter[InventoryOrder],
    IPaginationRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    ITypedEntityRequest,
    IHierarchyTypeRequest,
    IProjectBasedRequest,
    IPermissionedEntityRequest,
):
    childrenOfParentIds: Optional[List[int]] = None
    descendantsOfIds: Optional[List[int]] = None
    excludeHierarchyChildren: Optional[bool] = None
    isHierarchyRoot: Optional[bool] = None
    inventoryIds: Optional[List[int]] = None
