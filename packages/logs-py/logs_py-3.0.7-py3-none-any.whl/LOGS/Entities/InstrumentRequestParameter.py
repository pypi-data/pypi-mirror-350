from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreatedOnRequest
from LOGS.Interfaces.IModificationRecord import IModifiedOnRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class InstrumentOrder(Enum):
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
    IS_OBSOLETE_ASC = "IS_OBSOLETE_ASC"
    IS_OBSOLETE_DESC = "IS_OBSOLETE_DESC"


@dataclass
class InstrumentRequestParameter(
    EntityRequestParameter[InstrumentOrder],
    IRelatedEntityRequest,
    ICreatedOnRequest,
    IModifiedOnRequest,
    IOwnedEntityRequest,
    IPermissionedEntityRequest,
):
    name: Optional[str] = None
    methodIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
