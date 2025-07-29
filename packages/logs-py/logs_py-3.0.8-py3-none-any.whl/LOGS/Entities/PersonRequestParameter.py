from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest


class PersonOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    SALUTATION_ASC = "SALUTATION_ASC"
    SALUTATION_DESC = "SALUTATION_DESC"
    LAST_NAME_ASC = "LAST_NAME_ASC"
    LAST_NAME_DESC = "LAST_NAME_DESC"
    FIRST_NAME_ASC = "FIRST_NAME_ASC"
    FIRST_NAME_DESC = "FIRST_NAME_DESC"
    ORGANIZATION_ASC = "ORGANIZATION_ASC"
    ORGANIZATION_DESC = "ORGANIZATION_DESC"
    LOGIN_DISABLED_ASC = "LOGIN_DISABLED_ASC"
    LOGIN_DISABLED_DESC = "LOGIN_DISABLED_DESC"
    LOGIN_ASC = "LOGIN_ASC"
    LOGIN_DESC = "LOGIN_DESC"
    IS_SYSTEM_USER_ASC = "IS_SYSTEM_USER_ASC"
    IS_SYSTEM_USER_DESC = "IS_SYSTEM_USER_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"


@dataclass
class PersonRequestParameter(
    EntityRequestParameter[PersonOrder],
    IRelatedEntityRequest,
    ISoftDeletableRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
):
    personTagIds: Optional[List[int]] = None
    personTags: Optional[List[str]] = None
    organizationIds: Optional[List[int]] = None
    roleIds: Optional[List[int]] = None
    hasAccount: Optional[bool] = None
    isAccountEnabled: Optional[bool] = None
    includeSystemUsers: Optional[bool] = None
    logins: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    firstNames: Optional[List[str]] = None
    lastNames: Optional[List[str]] = None
