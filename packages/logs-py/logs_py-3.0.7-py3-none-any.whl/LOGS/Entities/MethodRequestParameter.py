from dataclasses import dataclass
from enum import Enum

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreatedByRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class MethodOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    FULL_NAME_ASC = "FULL_NAME_ASC"
    FULL_NAME_DESC = "FULL_NAME_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"


# : GenericListRequestParameters<int, MethodSortingOptions>,
#     IRelationParameters,
#     IPaginationParameters,
#     IPermissionParameters,
#     ICreationRecordParameters,
#     IModificationRecordParameters


@dataclass
class MethodRequestParameter(
    EntityRequestParameter[MethodOrder],
    IPaginationRequest,
    ICreatedByRequest,
    IModificationRecord,
    INamedEntityRequest,
    IPermissionedEntityRequest,
):
    pass
