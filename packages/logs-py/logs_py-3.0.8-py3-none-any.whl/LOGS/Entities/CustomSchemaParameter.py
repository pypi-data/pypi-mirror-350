from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest


class CustomSchemaOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    TYPE_ASC = "TYPE_ASC"
    TYPE_DESC = "TYPE_DESC"
    OWNER_ASC = "OWNER_ASC"
    OWNER_DESC = "OWNER_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"


_Sorting = TypeVar("_Sorting", bound=Enum)


@dataclass
class CustomSchemaParameter(
    Generic[_Sorting],
    EntityRequestParameter[_Sorting],
    IPaginationRequest,
    IOwnedEntityRequest,
    INamedEntityRequest,
):
    name: Optional[str] = None
    ownerIds: Optional[List[int]] = None
    creationDateFrom: Optional[datetime] = None
    creationDateTo: Optional[datetime] = None
    customFieldIds: Optional[List[str]] = None
    isEnabled: Optional[bool] = None
