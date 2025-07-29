from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.CustomTypeEntityType import CustomTypeEntityType
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IRelationRequest import IRelationRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest


class CustomTypeOrder(Enum):
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
    INVENTORY_NAME_ASC = "INVENTORY_NAME_ASC"
    INVENTORY_NAME_DESC = "INVENTORY_NAME_DESC"
    LAYOUT_ASC = "LAYOUT_ASC"
    LAYOUT_DESC = "LAYOUT_DESC"


@dataclass
class CustomTypeRequestParameter(
    EntityRequestParameter[CustomTypeOrder],
    IRelationRequest,
    IPaginationRequest,
    IPermissionedEntityRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    INamedEntityRequest,
):
    excludeDisabled: Optional[bool] = None
    isEnabled: Optional[bool] = None
    customFieldIds: Optional[List[int]] = None
    entityTypes: Optional[List[CustomTypeEntityType]] = None
    extendSearchToInventoryItems: Optional[bool] = None
    parentTypeIds: Optional[List[int]] = None
    hasRestrictedAddPermission: Optional[bool] = None
    hasRestrictedEditPermission: Optional[bool] = None
    hasRestrictedReadPermission: Optional[bool] = None
    rootHierarchyIds: Optional[List[int]] = None
    isInventory: Optional[bool] = None
    isHierarchyRoot: Optional[bool] = None
    inventoryNames: Optional[List[str]] = None
    excludeNonInventories: Optional[bool] = None
