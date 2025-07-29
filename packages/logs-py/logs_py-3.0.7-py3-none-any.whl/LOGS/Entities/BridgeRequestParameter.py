from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entities.BridgeType import BridgeType
from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import DefaultOrder, EntityRequestParameter
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


@dataclass
class BridgeRequestParameter(
    EntityRequestParameter[DefaultOrder],
    INamedEntityRequest,
    IRelatedEntityRequest,
    IPermissionedEntityRequest,
):
    hostnames: Optional[List[str]] = None
    usernames: Optional[List[str]] = None
    ipAddresses: Optional[List[str]] = None
    dataSourceIds: Optional[List[int]] = None
    types: Optional[List[BridgeType]] = None
    isConfigured: Optional[bool] = None
