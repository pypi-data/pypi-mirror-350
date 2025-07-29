from dataclasses import dataclass
from enum import Enum
from typing import Optional

from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class RoleOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    IS_INTERNAL_ASC = "IS_INTERNAL_ASC"
    IS_INTERNAL_DESC = "IS_INTERNAL_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"


@dataclass
class RoleRequestParameter(
    EntityRequestParameter[RoleOrder],
    IRelatedEntityRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
):
    name: Optional[str] = None
    roleId: Optional[str] = None
