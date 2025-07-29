from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class ExperimentOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    METHOD_ASC = "METHOD_ASC"
    METHOD_DESC = "METHOD_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"


@dataclass
class ExperimentRequestParameter(
    EntityRequestParameter[ExperimentOrder],
    IRelatedEntityRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
):
    name: Optional[str] = None
    methodIds: Optional[List[int]] = None
