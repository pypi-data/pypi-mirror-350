from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest


class SampleOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    PREPARATION_DATE_ASC = "PREPARATION_DATE_ASC"
    PREPARATION_DATE_DESC = "PREPARATION_DATE_DESC"
    TYPE_ASC = "TYPE_ASC"
    TYPE_DESC = "TYPE_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"
    DISCARDED_DATE_ASC = "DISCARDED_DATE_ASC"
    DISCARDED_DATE_DESC = "DISCARDED_DATE_DESC"


@dataclass
class SampleRequestParameter(
    EntityRequestParameter[SampleOrder],
    ICreationRecordRequest,
    IModificationRecordRequest,
    INamedEntityRequest,
    IOwnedEntityRequest,
    IPaginationRequest,
    IPermissionedEntityRequest,
    ISoftDeletableRequest,
    ITypedEntityRequest,
):
    discardedByIds: Optional[List[int]] = None
    discardedAtFrom: Optional[datetime] = None
    discardedAtTo: Optional[datetime] = None
    excludeDiscarded: Optional[bool] = None
    includeTags: Optional[bool] = None
    organizationIds: Optional[List[int]] = None
    participatedPersonIds: Optional[List[int]] = None
    preparedAtFrom: Optional[datetime] = None
    preparedAtTo: Optional[datetime] = None
    preparedByIds: Optional[List[int]] = None
    projectIds: Optional[List[int]] = None
    typeIds: Optional[List[str]] = None
    searchTermIncludeNotes: Optional[bool] = None
