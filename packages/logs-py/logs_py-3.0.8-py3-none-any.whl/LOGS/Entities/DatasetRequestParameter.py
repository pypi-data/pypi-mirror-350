from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Sequence

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entities.DatasetModels import ViewableEntityTypes
from LOGS.Entities.ICustomSchemaRequest import ICustomSchemaRequest
from LOGS.Entities.IRelatedEntityRequest import IRelatedEntityRequest
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICreationRecord import ICreationRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest

ParsingStates = Literal[
    "ParsedSuccessfully", "NotParseable", "ParsingFailed", "NotYetParsed"
]


class DatasetOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    ACQUISITION_DATE_ASC = "ACQUISITION_DATE_ASC"
    ACQUISITION_DATE_DESC = "ACQUISITION_DATE_DESC"
    METHOD_ASC = "METHOD_ASC"
    METHOD_DESC = "METHOD_DESC"
    EXPERIMENT_ASC = "EXPERIMENT_ASC"
    EXPERIMENT_DESC = "EXPERIMENT_DESC"
    CREATED_ON_ASC = "CREATED_ON_ASC"
    CREATED_ON_DESC = "CREATED_ON_DESC"
    CREATED_BY_ASC = "CREATED_BY_ASC"
    CREATED_BY_DESC = "CREATED_BY_DESC"
    MODIFIED_ON_ASC = "MODIFIED_ON_ASC"
    MODIFIED_ON_DESC = "MODIFIED_ON_DESC"
    MODIFIED_BY_ASC = "MODIFIED_BY_ASC"
    MODIFIED_BY_DESC = "MODIFIED_BY_DESC"
    INSTRUMENT_ASC = "INSTRUMENT_ASC"
    INSTRUMENT_DESC = "INSTRUMENT_DESC"
    SAMPLE_ASC = "SAMPLE_ASC"
    SAMPLE_DESC = "SAMPLE_DESC"
    PARSING_STATE_ASC = "PARSING_STATE_ASC"
    PARSING_STATE_DESC = "PARSING_STATE_DESC"
    FORMAT_ID_ASC = "FORMAT_ID_ASC"
    FORMAT_ID_DESC = "FORMAT_ID_DESC"
    TYPE_ASC = "TYPE_ASC"
    TYPE_DESC = "TYPE_DESC"


@dataclass
class DatasetRequestParameter(
    EntityRequestParameter[DatasetOrder],
    IRelatedEntityRequest,
    ITypedEntityRequest,
    ISoftDeletableRequest,
    ICustomSchemaRequest,
    IProjectBasedRequest,
    IOwnedEntityRequest,
    INamedEntityRequest,
    IUniqueEntityRequest,
    ICreationRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
):

    acquisitionDateFrom: Optional[datetime] = None
    acquisitionDateTo: Optional[datetime] = None
    autoloadServerIds: Optional[List[int]] = None
    bridgeIds: Optional[List[int]] = None
    dataSourceIds: Optional[List[int]] = None
    equipmentIds: Optional[List[int]] = None
    excludeUndeleted: Optional[bool] = None
    experimentIds: Optional[List[int]] = None
    files: Optional[Sequence[Constants.FILE_TYPE]] = None
    formatIds: Optional[List[str]] = None
    hasExperiment: Optional[bool] = None
    hashes: Optional[List[str]] = None
    hasOperator: Optional[bool] = None
    includeParameters: Optional[bool] = None
    includeParsingInfo: Optional[bool] = None
    includeSoftDeleted: Optional[Optional[bool]] = None
    includeUnclaimed: Optional[Optional[bool]] = None
    instrumentIds: Optional[List[int]] = None
    isClaimed: Optional[Optional[bool]] = None
    isReferencedByLabNotebook: Optional[Optional[bool]] = None
    isViewableEntity: Optional[bool] = None
    methodIds: Optional[List[int]] = None
    names: Optional[List[str]] = None
    operatorIds: Optional[List[int]] = None
    organizationIds: Optional[List[int]] = None
    originIds: Optional[List[int]] = None
    parameters: Optional[Dict[str, Any]] = None
    parsingState: Optional[List[ParsingStates]] = None
    participatedPersonIds: Optional[List[int]] = None
    pathContains: Optional[str] = None
    sampleIds: Optional[List[int]] = None
    searchTermIncludeNotes: Optional[bool] = None
    searchTermIncludeParameters: Optional[bool] = None
    searchTermIncludePaths: Optional[bool] = None
    viewableEntityTypes: Optional[List[ViewableEntityTypes]] = None
