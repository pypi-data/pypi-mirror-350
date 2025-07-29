from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.LabNotebookModels import LabNotebookExperimentStatus
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import (
    GenericPermissionEntity,
    IPermissionedEntityRequest,
)
from LOGS.Interfaces.IVersionedEntity import IVersionedEntityRequest


class LabNotebookExperimentOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    STATUS_ASC = "STATUS_ASC"
    STATUS_DESC = "STATUS_DESC"
    LAB_NOTEBOOK_ID_ASC = "LAB_NOTEBOOK_ID_ASC"
    LAB_NOTEBOOK_ID_DESC = "LAB_NOTEBOOK_ID_DESC"
    LAB_NOTEBOOK_NAME_ASC = "LAB_NOTEBOOK_NAME_ASC"
    LAB_NOTEBOOK_NAME_DESC = "LAB_NOTEBOOK_NAME_DESC"
    LAB_NOTEBOOK_EXPERIMENT_NAME_ASC = "LAB_NOTEBOOK_EXPERIMENT_NAME_ASC"
    LAB_NOTEBOOK_EXPERIMENT_NAME_DESC = "LAB_NOTEBOOK_EXPERIMENT_NAME_DESC"
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
class LabNotebookExperimentRequestParameter(
    EntityRequestParameter[LabNotebookExperimentOrder],
    IPermissionedEntityRequest,
    IVersionedEntityRequest[int],
    GenericPermissionEntity,
    INamedEntityRequest,
):
    status: Optional[List[LabNotebookExperimentStatus]] = None
    labNotebookIds: Optional[List[int]] = None
