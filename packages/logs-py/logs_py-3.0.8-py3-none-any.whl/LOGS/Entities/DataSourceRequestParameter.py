from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entities.DataSource import DataSourceType
from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


class DataSourceOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    TYPE_ASC = "TYPE_ASC"
    TYPE_DESC = "TYPE_DESC"
    BRIDGE_ASC = "BRIDGE_ASC"
    BRIDGE_DESC = "BRIDGE_DESC"
    INTERVAL_ASC = "INTERVAL_ASC"
    INTERVAL_DESC = "INTERVAL_DESC"
    ENABLED_ASC = "ENABLED_ASC"
    ENABLED_DESC = "ENABLED_DESC"
    METHOD_ASC = "METHOD_ASC"
    METHOD_DESC = "METHOD_DESC"
    INSTRUMENT_ASC = "INSTRUMENT_ASC"
    INSTRUMENT_DESC = "INSTRUMENT_DESC"


@dataclass
class DataSourceRequestParameter(
    EntityRequestParameter[DataSourceOrder],
    INamedEntityRequest,
    IRelatedEntityRequest,
    IPermissionedEntityRequest,
):
    enabled: Optional[bool] = None
    bridgeIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    formatIds: Optional[List[str]] = None
    customImportIds: Optional[List[str]] = None
    directories: Optional[List[str]] = None
    methodIds: Optional[List[int]] = None
    instrumentIds: Optional[List[int]] = None
    sourceHostnames: Optional[List[str]] = None
    sourceIpAddresses: Optional[List[str]] = None
    types: Optional[List[DataSourceType]] = None
