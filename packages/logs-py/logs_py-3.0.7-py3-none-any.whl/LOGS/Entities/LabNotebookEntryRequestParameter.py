from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest


class LabNotebookEntryOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    LAB_NOTEBOOK_ID_ASC = "LAB_NOTEBOOK_ID_ASC"
    LAB_NOTEBOOK_ID_DESC = "LAB_NOTEBOOK_ID_DESC"
    LAB_NOTEBOOK_NAME_ASC = "LAB_NOTEBOOK_NAME_ASC"
    LAB_NOTEBOOK_NAME_DESC = "LAB_NOTEBOOK_NAME_DESC"
    LAB_NOTEBOOK_EXPERIMENT_ID_ASC = "LAB_NOTEBOOK_EXPERIMENT_ID_ASC"
    LAB_NOTEBOOK_EXPERIMENT_ID_DESC = "LAB_NOTEBOOK_EXPERIMENT_ID_DESC"
    LAB_NOTEBOOK_EXPERIMENT_NAME_ASC = "LAB_NOTEBOOK_EXPERIMENT_NAME_ASC"
    LAB_NOTEBOOK_EXPERIMENT_NAME_DESC = "LAB_NOTEBOOK_EXPERIMENT_NAME_DESC"
    ENTRY_DATE_ASC = "ENTRY_DATE_ASC"
    ENTRY_DATE_DESC = "ENTRY_DATE_DESC"
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
class LabNotebookEntryRequestParameter(
    EntityRequestParameter[LabNotebookEntryOrder],
    IRelatedEntityRequest,
    ISoftDeletableRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
    INamedEntityRequest,
):
    includeContent: Optional[bool] = None

    labNotebookExperimentIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    mediaIds: Optional[List[int]] = None
    personIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    projectIds: Optional[List[int]] = None
    labNotebookIds: Optional[List[int]] = None
    entryDateFrom: Optional[date] = None
    entryDateTo: Optional[date] = None
    createdFrom: Optional[datetime] = None
    createdTo: Optional[datetime] = None
    createdByIds: Optional[List[int]] = None
    modifiedFrom: Optional[datetime] = None
    modifiedTo: Optional[datetime] = None
    modifiedByIds: Optional[List[int]] = None
    orderBy: Optional[LabNotebookEntryOrder] = None
    originalIds: Optional[List[int]] = None
    versionIds: Optional[List[int]] = None
    versions: Optional[List[int]] = None
    searchTermFullText: Optional[str] = None
