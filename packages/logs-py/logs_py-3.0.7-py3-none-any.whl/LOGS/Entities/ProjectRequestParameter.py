from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class ProjectOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    DATASET_COUNT_ASC = "DATASET_COUNT_ASC"
    DATASET_COUNT_DESC = "DATASET_COUNT_DESC"
    SAMPLE_COUNT_ASC = "SAMPLE_COUNT_ASC"
    SAMPLE_COUNT_DESC = "SAMPLE_COUNT_DESC"
    LAB_NOTEBOOK_COUNT_ASC = "LAB_NOTEBOOK_COUNT_ASC"
    LAB_NOTEBOOK_COUNT_DESC = "LAB_NOTEBOOK_COUNT_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"


@dataclass
class ProjectRequestParameter(
    EntityRequestParameter[ProjectOrder],
    IRelatedEntityRequest,
    IOwnedEntityRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    INamedEntityRequest,
    IPermissionedEntityRequest,
):
    typeIds: Optional[List[str]] = None
    notes: Optional[str] = None
    projectTagIds: Optional[List[int]] = None
    projectTags: Optional[List[str]] = None
    personIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    mediaIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
