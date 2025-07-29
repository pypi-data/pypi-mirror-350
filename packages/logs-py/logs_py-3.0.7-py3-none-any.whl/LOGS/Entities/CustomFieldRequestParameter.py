from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

from LOGS.Entities.CustomFieldModels import (
    CustomFieldDataType,
    CustomFieldValuesSearchPredicate,
)
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IRelationRequest import IRelationRequest


class CustomFieldOrder(Enum):
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
    DATATYPE_ASC = "DATATYPE_ASC"
    DATATYPE_DESC = "DATATYPE_DESC"


@dataclass
class CustomFieldValuesSearchParameters:
    values: Optional[List[Any]] = None
    dataType: Optional[CustomFieldDataType] = None
    customFieldIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    projectIds: Optional[List[int]] = None
    personIds: Optional[List[int]] = None
    inventoryIds: Optional[List[int]] = None
    facilityIds: Optional[List[int]] = None
    predicate: Optional[CustomFieldValuesSearchPredicate] = None


@dataclass
class ICustomFieldValuesSearchRequest:
    customFieldValues: Optional[List[CustomFieldValuesSearchParameters]] = None


@dataclass
class CustomFieldRequestParameter(
    EntityRequestParameter[CustomFieldOrder],
    IPaginationRequest,
    IRelationRequest,
    IPermissionedEntityRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    ICustomFieldValuesSearchRequest,
    IOwnedEntityRequest,
    INamedEntityRequest,
):
    dataTypes: Optional[List[CustomFieldDataType]] = None
    customFieldValues: Optional[List[CustomFieldValuesSearchParameters]] = None
