from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.LabNotebookModels import LabNotebookStatus
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import (
    GenericPermissionEntity,
    IPermissionedEntityRequest,
)
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.IVersionedEntity import IVersionedEntityRequest


class LabNotebookOrder(Enum):
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    STATUS_ASC = "STATUS_ASC"
    STATUS_DESC = "STATUS_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"
    VERSION_ASC = "VERSION_ASC"
    VERSION_DESC = "VERSION_DESC"


@dataclass
class LabNotebookRequestParameter(
    EntityRequestParameter[LabNotebookOrder],
    IPermissionedEntityRequest,
    IVersionedEntityRequest[int],
    IProjectBasedRequest,
    GenericPermissionEntity,
    INamedEntityRequest,
):
    status: Optional[List[LabNotebookStatus]] = None
