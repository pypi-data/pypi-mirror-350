import os
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, cast

from deprecation import deprecated

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint, UiEndpoint
from LOGS.Auxiliary.Exceptions import (
    EntityFetchingException,
    EntityIncompleteException,
    LOGSException,
)
from LOGS.Auxiliary.MinimalModelGenerator import (
    BridgeMinimalFromDict,
    ExperimentMinimalFromDict,
    FormatMinimalFromDict,
    InstrumentMinimalFromDict,
    MethodMinimalFromDict,
    MinimalFromList,
    SampleMinimalFromDict,
)
from LOGS.Auxiliary.ParameterHelper import ParameterHelper
from LOGS.Auxiliary.Tools import Tools
from LOGS.Converter import Converter
from LOGS.Converter.Conversion import Conversion
from LOGS.Converter.ExportParameters import ExportParameters
from LOGS.Entities.DatasetInfo import DatasetInfo
from LOGS.Entities.DatasetModels import DatasetSourceType, ViewableEntityTypes
from LOGS.Entities.DatasetRelations import DatasetRelations
from LOGS.Entities.DatasetRequestParameter import ParsingStates
from LOGS.Entities.Datatrack import Datatrack
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.HierarchyNode import HierarchyNode
from LOGS.Entities.ParserLog import ParserLog
from LOGS.Entities.Track import Track
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Entity.SerializableContent import SerializableContent
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IProjectBased import IProjectBased
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection, ResponseTypes
from LOGS.Parameters.ParameterList import ParameterList

if TYPE_CHECKING:
    from LOGS.Entities.BridgeMinimal import BridgeMinimal
    from LOGS.Entities.EquipmentMinimal import EquipmentMinimal
    from LOGS.Entities.ExperimentMinimal import ExperimentMinimal
    from LOGS.Entities.FormatMinimal import FormatMinimal
    from LOGS.Entities.InstrumentMinimal import InstrumentMinimal
    from LOGS.Entities.MethodMinimal import MethodMinimal
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.SampleMinimal import SampleMinimal


class ParsedMetadata(SerializableContent):
    Parameters: bool = False
    Tracks: bool = False
    TrackCount: int = False
    TrackViewerTypes: List[str] = []


@dataclass
class DatasetSource:
    id: Optional[int] = None
    type: Optional[DatasetSourceType] = None
    name: Optional[str] = None


@Endpoint("datasets")
@UiEndpoint("#data")
class Dataset(
    IEntityWithIntId,
    GenericPermissionEntity,
    INamedEntity,
    IOwnedEntity,
    IProjectBased,
    IRelatedEntity[DatasetRelations],
    ISoftDeletable,
    ITypedEntity,
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
):
    _noInfo = True
    _noParameters = True
    _noExports = True
    _noParameterTree = True
    _relationType = DatasetRelations

    _acquisitionDate: Optional[datetime] = None
    _automaticName: Optional[str] = None
    _bridge: Optional["BridgeMinimal"] = None
    _claimed: Optional[bool] = None
    _customImport: Optional[EntityMinimalWithIntId] = None
    _datatracks: Optional[List[Datatrack]] = None
    _equipments: Optional[List["EquipmentMinimal"]] = None
    _experiment: Optional["ExperimentMinimal"] = None
    _exports: Optional[List[Converter]] = None
    _files: Optional[List[FileEntry]] = None
    _format: Optional["FormatMinimal"] = None
    _formatVersion: Optional[int] = None
    _instrument: Optional["InstrumentMinimal"] = None
    _isManuallyNamed: Optional[bool] = None
    _isViewableEntity: Optional[bool] = None
    _legacyId: Optional[str] = None
    _method: Optional["MethodMinimal"] = None
    _notes: Optional[str] = None
    _operators: Optional[List["PersonMinimal"]] = None
    _other: Optional[str] = None
    _parameterHelper: Optional[ParameterHelper] = None
    _parameters: Optional[Dict[str, Any]] = None
    _parameterTree: Optional[ParameterList] = None
    _parsedMetadata: Optional[ParsedMetadata] = None
    _parserLogs: Optional[List[ParserLog]] = None
    _parsingState: Optional[ParsingStates] = None
    _path: Optional[str] = None
    _sample: Optional["SampleMinimal"] = None
    _source: Optional[DatasetSource] = None
    _sourceBaseDirectory: Optional[str] = None
    _sourceRelativeDirectory: Optional[str] = None
    _tracks: Optional[List[Track]] = None
    _tracksHierarchy: Optional[HierarchyNode] = None
    _viewableEntityType: Optional[ViewableEntityTypes] = None
    _zipSize: Optional[int] = None

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        format: Optional[Union[str, "FormatMinimal"]] = None,
    ):
        super().__init__(ref=ref, id=id, connection=connection)

        t = type(self)
        self._noSerialize += [
            t.parameters.fget.__name__,  # type: ignore
            t.parameterTree.fget.__name__,  # type: ignore
            t.formatVersion.fget.__name__,  # type: ignore
            t.parserLogs.fget.__name__,  # type: ignore
            t.tracks.fget.__name__,  # type: ignore
            t.datatracks.fget.__name__,  # type: ignore
            t.tracksHierarchy.fget.__name__,  # type: ignore
            t.exports.fget.__name__,  # type: ignore
        ]

        if isinstance(ref, Dataset):
            self._format = ref._format

        if format:
            self.format = cast(Any, format)

        if files:
            if not self._format or not self._format.id:
                raise LOGSException(
                    "Cannot create %s object from files parameter without a format"
                    % type(self).__name__
                )

            self._files = FileEntry.entriesFromFiles(files)

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict):
            if "parameters" in ref:
                self._parameters = self.checkAndConvertNullable(
                    ref["parameters"], dict, "parameters"
                )
                self._noParameters = False
            if "parameterTree" in ref:
                self._parameterTree = self.checkAndConvertNullable(
                    ref["parameterTree"], ParameterList, "parameters"
                )
                self._noParameterTree = False

            infoFields = [
                "formatVersion",
                "parserLogs",
                "tracks",
                "datatracks",
                "tracksHierarchy",
                "parsingState",
            ]

            self._noInfo = not all(f in ref for f in infoFields)

            info = {}
            for field in infoFields:
                if field in ref:
                    info[field] = ref[field]
                    del ref[field]

        super().fromDict(ref=ref)
        self._setInfo(info)

    def fetchZipSize(self):
        connection, endpoint, id = self._getConnectionData()

        zip, responseError = connection.getEndpoint(
            endpoint + ["zip_size"], parameters={"ids": [self.id]}
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(zip, dict) and "size" in zip:
            self._zipSize = zip["size"]

    def fetchParameters(self):
        connection, endpoint, id = self._getConnectionData()

        parameters, responseError = connection.getEndpoint(
            endpoint + [id, "parameters"]
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(parameters, dict):
            if "url" in parameters:
                del parameters["url"]
            self._parameters = parameters
        else:
            self._parameters = {}

        self._parameterHelper = ParameterHelper(self._parameters)
        self._noParameters = False

    def fetchParameterTree(self):
        connection, endpoint, id = self._getConnectionData()

        parameters, responseError = connection.getEndpoint(
            endpoint + [id, "parameter_tree"]
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if parameters == "":
            parameters = None

        self._parameterTree = self.checkAndConvertNullable(
            parameters, ParameterList, "parameterTree"
        )

        self._noParameterTree = False

    def fetchExports(self):
        connection, endpoint, id = self._getConnectionData()

        exports, responseError = connection.getEndpoint(endpoint + [id, "exports"])
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        self.exports = exports
        self._noExports = False

    def _getDataDir(self):
        if self.cacheDir:
            if not os.path.isdir(self.cacheDir):
                raise LOGSException(
                    f"Specified cache directory '{self.cacheDir}' cannot be opened or is not a directory."
                )
            return self.cacheDir
        return None

    def clearCache(self):
        dataDir = self._getDataDir()
        if dataDir and os.path.exists(dataDir) and self.datatracks:
            for datatrack in self.datatracks:
                datatrack.clearCache()
            os.rmdir(dataDir)

    def _setInfo(self, data: dict):
        info = DatasetInfo(data)
        self._formatVersion = info.formatVersion
        self._parserLogs = info.parserLogs
        self._tracks = info.tracks
        self._datatracks = info.datatracks
        self._tracksHierarchy = info.tracksHierarchy
        self._parsingState = info.parsingState

        dataDir = self._getDataDir()

        trackLookup: Dict[str, Datatrack] = {}
        if self._datatracks:
            for datatrack in self._datatracks:
                datatrack.connection = self.connection
                datatrack.cacheDir = dataDir
                if datatrack.id:
                    trackLookup[datatrack.id] = datatrack

        if self._tracks:
            for track in self._tracks:
                track.connection = self.connection
                track.cacheDir = dataDir
                if track._dataIds:
                    track.datatracks = cast(
                        Any,
                        {
                            k: (trackLookup[v] if v in trackLookup else None)
                            for k, v in track._dataIds.items()
                        },
                    )

    def fetchInfo(self):
        connection, endpoint, id = self._getConnectionData()

        data, responseError = connection.getEndpoint(endpoint + [id, "info"])
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        dataDir = self._getDataDir()
        if dataDir and not os.path.exists(dataDir):
            os.mkdir(dataDir)

        self._setInfo(cast(dict, data))
        self._noInfo = False
        if self._datatracks:
            for datatrack in self._datatracks:
                datatrack._endpoint = (
                    endpoint + [str(id), "datatrack"] if endpoint else None
                )

    def fetchFull(self):
        self.fetchParameters()
        self.fetchInfo()
        self.fetchZipSize()
        self.fetchExports()

    def download(
        self,
        directory: Optional[str] = None,
        fileName: Optional[str] = None,
        overwrite=False,
    ):
        connection, endpoint, id = self._getConnectionData()

        if not directory:
            directory = os.curdir

        if not fileName:
            fileName = self.name if self.name and self.name != "" else "Dataset"
            fileName += ".zip"

        path = os.path.join(directory, Tools.sanitizeFileName(fileName=fileName))

        if overwrite:
            if os.path.exists(path) and not os.path.isfile(path):
                raise LOGSException("Path %a is not a file" % path)
        else:
            if os.path.exists(path):
                raise LOGSException("File %a already exists" % path)

        data, responseError = connection.getEndpoint(
            endpoint + [id, "files", "zip"], responseType=ResponseTypes.RAW
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        with open(path, mode="wb") as localfile:
            localfile.write(cast(bytes, data))

        return path

    def getParameter(self, key, removeUnit=False):
        if not self._parameterHelper:
            self._parameterHelper = ParameterHelper(self.parameters)
        return self._parameterHelper.get(key, removeUnit)

    def _requestReport(self, exportId: str, parameters: Optional[ExportParameters]):
        connection, endpoint, id = self._getConnectionData()
        converterEndpoint: Any = endpoint + [id, "exports", exportId]
        payload = parameters.toDict() if parameters else {}
        data, responseError = connection.postEndpoint(converterEndpoint, data=payload)
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        # TODO: create a report type to wait for the report to be generated
        # TODO: maybe a class "Conversion" can be created that has a state and also and automatic awaiter function or so
        conversion = self.checkAndConvert(data, Conversion, f"Conversion_to_{exportId}")
        conversion.connection = self.connection
        conversion._endpoint = converterEndpoint
        conversion._payload = payload
        conversion._parentEntity = self
        return conversion

    def exportTo(
        self, exportId: str, parameters: Optional[Union[ExportParameters, dict]] = None
    ):

        if self._noExports:
            self.fetchExports()

        if self.exports is None:
            raise LOGSException(f"Export id '{exportId}' not found in exports")

        exports = {e.exportId: e for e in self.exports}
        exports.update({e.id: e for e in self.exports})
        if exportId not in exports:
            raise LOGSException(f"Export id '{exportId}' not found in exports")

        export = exports[exportId]
        p = export.requestParameter
        if parameters is not None and p is not None:
            if isinstance(parameters, dict):
                p.fromDict(parameters)
            elif isinstance(parameters, ExportParameters):
                if parameters._parentId is None or parameters._parentId != p._parentId:
                    raise LOGSException(
                        f"The passed export parameters is not generated by and valid export format. (Expected class '{p.identifier}')"
                    )
            else:
                raise LOGSException(
                    f"Invalid parameter type '{type(parameters).__name__}'. (Expected 'dict' or '{ExportParameters.__name__}')"
                )

        return self._requestReport(exportId, p)

    @property
    def format(self) -> Optional["FormatMinimal"]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = FormatMinimalFromDict(
            value, "format", connection=self.connection
        )

    @property
    def acquisitionDate(self) -> Optional[datetime]:
        return self._acquisitionDate

    @acquisitionDate.setter
    def acquisitionDate(self, value):
        self._acquisitionDate = self.checkAndConvertNullable(
            value, datetime, "acquisitionDate"
        )

    @property
    def path(self) -> Optional[str]:
        return self._path

    @path.setter
    def path(self, value):
        self._path = self.checkAndConvertNullable(value, str, "path")

    @property
    def claimed(self) -> Optional[bool]:
        return self._claimed

    @claimed.setter
    def claimed(self, value):
        self._claimed = self.checkAndConvertNullable(value, bool, "claimed")

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def dateAdded(self) -> Optional[datetime]:
        return self._dateAdded

    @dateAdded.setter
    def dateAdded(self, value):
        self._dateAdded = self.checkAndConvertNullable(value, datetime, "dateAdded")

    @property
    def isDeleted(self) -> Optional[bool]:
        return self._isDeleted

    @isDeleted.setter
    def isDeleted(self, value):
        self._isDeleted = self.checkAndConvertNullable(value, bool, "isDeleted")

    @property
    def other(self) -> Optional[str]:
        return self._other

    @other.setter
    def other(self, value):
        self._other = self.checkAndConvertNullable(value, str, "other")

    @property
    def parsingState(self) -> Optional[ParsingStates]:
        return self._parsingState

    @parsingState.setter
    def parsingState(self, value):
        self._parsingState = cast(
            ParsingStates, self.checkAndConvertNullable(value, str, "parsingState")
        )

    @property
    def parsedMetadata(self) -> Optional[ParsedMetadata]:
        return self._parsedMetadata

    @parsedMetadata.setter
    def parsedMetadata(self, value):
        self._parsedMetadata = self.checkAndConvertNullable(
            value, ParsedMetadata, "parsedMetadata"
        )

    @property
    def parameters(self) -> Optional[Dict[str, Any]]:
        if self._noParameters:
            raise EntityIncompleteException(
                self,
                parameterName="parameters",
                functionName=f"{self.fetchParameters.__name__}()",
            )
        return self._parameters

    @property
    def parameterTree(self) -> Optional[ParameterList]:
        if self._noParameterTree:
            raise EntityIncompleteException(
                self,
                parameterName="parameterTree",
                functionName=f"{self.fetchParameterTree.__name__}()",
                hasFetchFull=False,
            )
        return self._parameterTree

    @property
    def formatVersion(self) -> Optional[int]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="formatVersion",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._formatVersion

    @property
    def parserLogs(self) -> Optional[List[ParserLog]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="parserLogs",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._parserLogs

    @property
    def tracks(self) -> Optional[List[Track]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="tracks",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._tracks

    @property
    def datatracks(self) -> Optional[List[Datatrack]]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="datatracks",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._datatracks

    @property
    def tracksHierarchy(self) -> Optional[HierarchyNode]:
        if self._noInfo:
            raise EntityIncompleteException(
                self,
                parameterName="tracksHierarchy",
                functionName=f"{self.fetchInfo.__name__}()",
            )
        return self._tracksHierarchy

    @property
    def zipSize(self) -> Optional[int]:
        if self._zipSize is None:
            raise EntityIncompleteException(
                self,
                parameterName="zipSize",
                functionName=f"{self.fetchZipSize.__name__}()",
            )
        return self._zipSize

    @property
    def bridge(self) -> Optional["BridgeMinimal"]:
        return self._bridge

    @bridge.setter
    def bridge(self, value):
        self._bridge = BridgeMinimalFromDict(
            value, "bridge", connection=self.connection
        )

    @property
    def bridgeId(self) -> Optional[int]:
        return self._bridge.id if self._bridge else None

    @bridgeId.setter
    def bridgeId(self, value):
        self._bridge = BridgeMinimalFromDict(
            value, "bridge", connection=self.connection
        )

    @property
    def equipments(self) -> Optional[List["EquipmentMinimal"]]:
        return self._equipments

    @equipments.setter
    def equipments(self, value):
        self._equipments = MinimalFromList(
            value, "EquipmentMinimal", "equipments", connection=self.connection
        )

    @property
    def equipmentIds(self) -> Optional[List[int]]:
        if self._equipments is None:
            return None
        return [e.id for e in self._equipments]

    @equipmentIds.setter
    def equipmentIds(self, value):
        self._equipments = MinimalFromList(
            value, "EquipmentMinimal", "equipments", connection=self.connection
        )

    @property
    def method(self) -> Optional["MethodMinimal"]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def methodId(self) -> Optional[int]:
        return self._method.id if self._method else None

    @property
    def experiment(self) -> Optional["ExperimentMinimal"]:
        return self._experiment

    @experiment.setter
    def experiment(self, value):
        self._experiment = ExperimentMinimalFromDict(
            value, "experiment", connection=self.connection
        )

    @property
    def sample(self) -> Optional["SampleMinimal"]:
        return self._sample

    @sample.setter
    def sample(self, value):
        self._sample = SampleMinimalFromDict(
            value, "sample", connection=self.connection
        )

    @property
    def sampleId(self) -> Optional[int]:
        return self._sample.id if self._sample else None

    @sampleId.setter
    def sampleId(self, value):
        self._sample = SampleMinimalFromDict(
            value, "sample", connection=self.connection
        )

    @property
    def operators(self) -> Optional[List["PersonMinimal"]]:
        return self._operators

    @operators.setter
    def operators(self, value):
        self._operators = MinimalFromList(
            value, "PersonMinimal", "operators", connection=self.connection
        )

    @property
    def operatorIds(self) -> Optional[List[int]]:
        if self._operators is None:
            return None
        return [e.id for e in self._operators]

    @operatorIds.setter
    def operatorIds(self, value):
        self._operators = MinimalFromList(
            value, "PersonMinimal", "operators", connection=self.connection
        )

    @property
    def instrument(self) -> Optional["InstrumentMinimal"]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", connection=self.connection
        )

    @property
    def instrumentId(self) -> Optional[int]:
        return self._instrument.id if self._instrument else None

    @instrumentId.setter
    def instrumentId(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", connection=self.connection
        )

    @property
    def legacyId(self) -> Optional[str]:
        return self._legacyId

    @legacyId.setter
    def legacyId(self, value):
        self._legacyId = self.checkAndConvertNullable(value, str, "legacyId")

    @property
    def sourceBaseDirectory(self) -> Optional[str]:
        return self._sourceBaseDirectory

    @sourceBaseDirectory.setter
    def sourceBaseDirectory(self, value):
        self._sourceBaseDirectory = self.checkAndConvertNullable(
            value, str, "sourceBaseDirectory"
        )

    @property
    def sourceRelativeDirectory(self) -> Optional[str]:
        return self._sourceRelativeDirectory

    @sourceRelativeDirectory.setter
    def sourceRelativeDirectory(self, value):
        self._sourceRelativeDirectory = self.checkAndConvertNullable(
            value, str, "sourceRelativeDirectory"
        )

    @property
    @deprecated(details="Please use property 'attachment'")
    def isViewableEntity(self) -> Optional[bool]:
        return self._isViewableEntity

    @isViewableEntity.setter
    @deprecated(details="Please use property 'attachment'")
    def isViewableEntity(self, value):
        self._isViewableEntity = self.checkAndConvertNullable(
            value, bool, "isViewableEntity"
        )

    @property
    def exports(self) -> Optional[List[Converter]]:
        if self._noExports:
            raise EntityIncompleteException(
                self,
                parameterName="exports",
                functionName=f"{self.fetchExports.__name__}()",
                hasFetchFull=True,
            )

        return self._exports

    @exports.setter
    def exports(self, value):
        self._exports = self.checkListAndConvertNullable(value, Converter, "exports")

    @property
    def viewableEntityType(self) -> Optional[ViewableEntityTypes]:
        return self._viewableEntityType

    @viewableEntityType.setter
    def viewableEntityType(self, value):
        self._viewableEntityType = self.checkAndConvertNullable(
            value, ViewableEntityTypes, "viewableEntityType"
        )

    @property
    def customImport(self) -> Optional[EntityMinimalWithIntId]:
        return self._customImport

    @customImport.setter
    def customImport(self, value):
        self._customImport = self.checkAndConvertNullable(
            value, EntityMinimalWithIntId, "customImport"
        )

    @property
    def source(self) -> Optional[DatasetSource]:
        return self._source

    @source.setter
    def source(self, value):
        self._source = self.checkAndConvertNullable(value, DatasetSource, "source")

    @property
    def isManuallyNamed(self) -> Optional[bool]:
        return self._isManuallyNamed

    @isManuallyNamed.setter
    def isManuallyNamed(self, value):
        self._isManuallyNamed = self.checkAndConvertNullable(
            value, bool, "isManuallyNamed"
        )

    @property
    def automaticName(self) -> Optional[str]:
        return self._automaticName

    @automaticName.setter
    def automaticName(self, value):
        self._automaticName = self.checkAndConvertNullable(value, str, "automaticName")
