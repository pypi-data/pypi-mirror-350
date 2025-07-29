#!/usr/bin/env python3
"""
A library to access the LOGS API via Python
"""

import json
import os
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from uuid import UUID

from LOGS.Auxiliary import (
    Constants,
    EntityCreatingException,
    EntityDeletingException,
    EntityNotFoundException,
    EntityUpdatingException,
    LOGSException,
    Tools,
    formatErrorMessage,
)
from LOGS.Entities.Bridge import Bridge
from LOGS.Entities.BridgeRequestParameter import BridgeRequestParameter
from LOGS.Entities.Bridges import Bridges
from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.CustomFieldRequestParameter import CustomFieldRequestParameter
from LOGS.Entities.CustomFields import CustomFields
from LOGS.Entities.CustomType import CustomType
from LOGS.Entities.CustomTypeRequestParameter import CustomTypeRequestParameter
from LOGS.Entities.CustomTypes import CustomTypes
from LOGS.Entities.Dataset import Dataset
from LOGS.Entities.DatasetCreator import DatasetCreator
from LOGS.Entities.DatasetMatching import DatasetMatching
from LOGS.Entities.DatasetMatchTypes import DatasetsUpdatableFiles
from LOGS.Entities.DatasetRequestParameter import DatasetRequestParameter
from LOGS.Entities.Datasets import Datasets
from LOGS.Entities.DataSource import DataSource
from LOGS.Entities.DataSourceRequestParameter import DataSourceRequestParameter
from LOGS.Entities.DataSources import DataSources
from LOGS.Entities.Entities import Entities
from LOGS.Entities.EntitiesRequestParameter import EntitiesRequestParameter
from LOGS.Entities.EntityOriginWriteModelWithId import EntityOriginWriteModelWithId
from LOGS.Entities.Equipment import Equipment
from LOGS.Entities.Experiment import Experiment
from LOGS.Entities.ExperimentRequestParameter import ExperimentRequestParameter
from LOGS.Entities.Experiments import Experiments
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.Format import Format
from LOGS.Entities.FormatFormat import FormatFormat
from LOGS.Entities.FormatFormatRequestParameter import FormatFormatRequestParameter
from LOGS.Entities.FormatFormats import FormatFormats
from LOGS.Entities.FormatInstrument import FormatInstrument
from LOGS.Entities.FormatInstrumentRequestParameter import (
    FormatInstrumentRequestParameter,
)
from LOGS.Entities.FormatInstruments import FormatInstruments
from LOGS.Entities.FormatMethod import FormatMethod
from LOGS.Entities.FormatMethodRequestParameter import FormatMethodRequestParameter
from LOGS.Entities.FormatMethods import FormatMethods
from LOGS.Entities.FormatRequestParameter import FormatRequestParameter
from LOGS.Entities.Formats import Formats
from LOGS.Entities.FormatVendor import FormatVendor
from LOGS.Entities.FormatVendorRequestParameter import FormatVendorRequestParameter
from LOGS.Entities.FormatVendors import FormatVendors
from LOGS.Entities.Instrument import Instrument
from LOGS.Entities.InstrumentRequestParameter import InstrumentRequestParameter
from LOGS.Entities.Instruments import Instruments
from LOGS.Entities.Inventories import Inventories
from LOGS.Entities.Inventory import Inventory
from LOGS.Entities.InventoryRequestParameter import InventoryRequestParameter
from LOGS.Entities.LabNotebook import LabNotebook
from LOGS.Entities.LabNotebookEntries import LabNotebookEntries
from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
from LOGS.Entities.LabNotebookEntryRequestParameter import (
    LabNotebookEntryRequestParameter,
)
from LOGS.Entities.LabNotebookExperiment import LabNotebookExperiment
from LOGS.Entities.LabNotebookExperimentRequestParameter import (
    LabNotebookExperimentRequestParameter,
)
from LOGS.Entities.LabNotebookExperiments import LabNotebookExperiments
from LOGS.Entities.LabNotebookRequestParameter import LabNotebookRequestParameter
from LOGS.Entities.LabNotebooks import LabNotebooks
from LOGS.Entities.Method import Method
from LOGS.Entities.MethodRequestParameter import MethodRequestParameter
from LOGS.Entities.Methods import Methods
from LOGS.Entities.Origin import Origin
from LOGS.Entities.OriginRequestParameter import OriginRequestParameter
from LOGS.Entities.Origins import Origins
from LOGS.Entities.Person import Person
from LOGS.Entities.PersonRequestParameter import PersonRequestParameter
from LOGS.Entities.Persons import Persons
from LOGS.Entities.Project import Project
from LOGS.Entities.ProjectRequestParameter import ProjectRequestParameter
from LOGS.Entities.Projects import Projects
from LOGS.Entities.Role import Role
from LOGS.Entities.RoleRequestParameter import RoleRequestParameter
from LOGS.Entities.Roles import Roles
from LOGS.Entities.Sample import Sample
from LOGS.Entities.SampleRequestParameter import SampleRequestParameter
from LOGS.Entities.Samples import Samples
from LOGS.Entity import Entity, EntityIterator, IEntityWithIntId
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection
from LOGS.LOGSOptions import LOGSOptions
from LOGS.ServerMetaData import ServerMetaData

_T = TypeVar(
    "_T",
    Bridge,
    CustomField,
    CustomType,
    Dataset,
    DataSource,
    Equipment,
    Experiment,
    Format,
    FormatFormat,
    FormatInstrument,
    FormatMethod,
    FormatVendor,
    IEntityWithIntId,
    Instrument,
    Inventory,
    LabNotebook,
    LabNotebookEntry,
    LabNotebookExperiment,
    Method,
    Origin,
    Person,
    Project,
    Role,
    Sample,
)


class LOGS:
    """Python class to access the LOGS web API"""

    _connection: LOGSConnection
    _entities: List[Type] = [
        Bridge,
        CustomField,
        CustomType,
        Dataset,
        DataSource,
        Equipment,
        Experiment,
        Instrument,
        Inventory,
        LabNotebook,
        LabNotebookEntry,
        LabNotebookExperiment,
        Method,
        Origin,
        Person,
        Project,
        Sample,
    ]
    _entityByName = {t.__name__: t for t in _entities}
    _defaultConfigFile: str = "logs.json"
    _currentUser: Person
    _cacheDir: Optional[str] = None

    def __init__(
        self,
        url: Optional[str] = None,
        apiKey: Optional[str] = None,
        configFile: Optional[str] = None,
        options: Optional[LOGSOptions] = None,
        verify: bool = True,
    ):
        """Checks the connection to the server on creation

        :param url: URL to specific LOGS group (e.g. https://mylogs/mygroup or https://mylogs:80/mygroup/api/0.1)
        :param api_key: The API key that grants access to LOGS (you need to generate on in LOGS and copy it)
        :param verbose: If set you see some information about the server connection. Defaults to False.

        :raises: Exception: URL does not defined or is invalid.
        :raises: Exception: The URL does not define a group.
        :raises: Exception: Server cannot be reached.
        """
        self._options = Tools.checkAndConvert(
            options, LOGSOptions, "options", initOnNone=True
        )

        _url = url
        _apiKey = apiKey

        if not configFile and os.path.isfile(self._defaultConfigFile):
            configFile = self._defaultConfigFile

        if configFile:
            config = self._readConfig(configFile)
            if "url" in config:
                _url = config["url"]
            if "apiKey" in config:
                _apiKey = config["apiKey"]
            if "proxyTargetUrl" in config:
                self._options.proxyTargetUrl = config["proxyTargetUrl"]

        if url:
            _url = url

        if apiKey:
            _apiKey = apiKey

        if not _url:
            raise LOGSException("The url to the LOGS server must be provided.")

        if not _apiKey:
            raise LOGSException(
                "The API key to access the server %a must be provided" % _url
            )

        self.promptPrefix = "LOGSAPI>"

        self._connection = LOGSConnection(
            url=_url, apiKey=_apiKey, options=self._options, verify=verify
        )
        self._currentUser = self._fetchCurrentUser()

    def _fetchCurrentUser(self) -> Person:
        data, responseError = self._connection.getEndpoint(["session"])
        if responseError:
            raise LOGSException(responseError=responseError)

        if not isinstance(data, dict):
            raise LOGSException(
                "Unexpected response from session endpoint. Could not get current user."
            )

        person = None
        if "person" in data:
            person = Person(data["person"])

        if not person or not person.id:
            raise LOGSException(
                "Unexpected response from session endpoint. Could not get current user."
            )

        return person

    def _readConfig(self, path: str) -> dict:
        if not os.path.isfile(path):
            raise LOGSException("Could not find config file %a" % path)

        with open(path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                raise LOGSException(
                    "Could not read config from file %a: %s" % (path, str(e))
                )
        return config

    @classmethod
    def getHumanReadableSize(cls, size: float, suffix="B"):
        for unit in Constants.byteUnits:
            if abs(size) < 1024.0:
                return "%3.1f%s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f%s%s" % (size, "Yi", suffix)

    def getDatasetDir(self, dataset: Dataset):
        if self.cacheDir:
            if not os.path.isdir(self.cacheDir):
                raise LOGSException(
                    f"Specified cache directory '{self.cacheDir}' cannot be opened or is not a directory."
                )

            dataDir = os.path.join(self.cacheDir, dataset.cacheId)
            if dataDir and not os.path.exists(dataDir):
                os.mkdir(dataDir)
            return dataDir
        return None

    def _fetchEntity(self, entityType: Type[_T], id: Union[int, str]) -> _T:
        e = entityType(id=cast(Any, id), connection=self._connection)
        if isinstance(e, Dataset):
            e.cacheDir = self.getDatasetDir(e)
        e.fetch()
        return e

    def _restoreEntitiesByTypeName(self, typeDict: Dict[str, Any]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._restoreEntities(cast(Any, t), entities)

    def _restoreEntities(
        self, entityType: Type[Entity], entities: List[Constants.ENTITIES]
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Restoring of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entities) < 1:
            return
        elif len(entities) == 1:
            if not entities[0].id:
                raise EntityNotFoundException(entities[0])

            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["restore", str(entities[0].id)],
                data=entities[0].toDict(),
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
                and len(data["results"]) > 0
            ):
                entities[0].override(data["results"][0])
        else:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_restore"],
                data=[e.id for e in entities],
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)

        if responseError:
            raise EntityUpdatingException(entity=entities, responseError=responseError)

    def _updateEntitiesByTypeName(self, typeDict: Dict[str, Any]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._updateEntities(cast(Any, t), entities)

    def _updateEntities(
        self, entityType: Type[Entity], entities: List[Constants.ENTITIES]
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Updating of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entities) < 1:
            return
        elif len(entities) == 1:
            if not entities[0].id:
                raise EntityNotFoundException(entities[0])

            data, responseError = self._connection.putEndpoint(
                entityType._endpoint + [str(entities[0].id)],
                data=entities[0]._toDictWithSlack(),
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
                and len(data["results"]) > 0
            ):
                entities[0].override(data["results"][0])
        else:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_edit"],
                data=[e._toDictWithSlack() for e in entities],
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)

        if responseError:
            raise EntityUpdatingException(entity=entities, responseError=responseError)

    def _createDataset(self, dataset: Dataset):
        data = DatasetCreator(connection=self._connection, dataset=dataset).create()
        # TODO: The following is not optimal. DatasetCreator should directly set the dataset properties (add dataset write model to multipart)
        if (
            "results" in data
            and isinstance(data["results"], list)
            and len(data["results"]) == 1
        ):
            dataset.override(data["results"][0])
            dataset.connection = self._connection

    def _createEntitiesByTypeName(self, typeDict: Dict[str, Entity]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)

            if not t:
                continue

            self._createEntities(cast(Any, t), cast(Any, entities))

    def _addOriginToEntity(
        self, endpoint: List[str], entity: Optional[EntityOriginWriteModelWithId]
    ):
        return self._addOriginToEntities(endpoint, [entity])

    def _addOriginToEntities(
        self,
        endpoint: List[str],
        entities: List[Optional[EntityOriginWriteModelWithId]],
    ):
        entities = [e for e in entities if e]
        if len(entities) == 1:
            data, responseError = self._connection.postEndpoint(
                endpoint + ["origin"], data=[e.toDict() for e in entities if e]
            )
            if responseError:
                indent = " " * 2
                message = ""
                if isinstance(data, list):
                    message = "%sCould not add origin to %s %a" % (
                        (
                            "\n" + indent
                            if responseError and len(responseError.errors) > 1
                            else ""
                        ),
                        Tools.plural("entity", entities),
                        Tools.eclipsesJoin(", ", [e.id for e in entities if e]),
                    )

                # indent *= 2
                if responseError:
                    message += ": " + formatErrorMessage(
                        errors=responseError.errors, indent=indent
                    )

                raise LOGSException(message=message, responseError=responseError)

        # for o in entities:
        #     print(">>>>>", o.toDict())
        # data, errors = self._connection.postEndpoint(
        #     entityType._endpoint + ["bulk_create"],
        #     data=[e.toDict() for e in entities],
        # )

    def _createEntityOriginWriteModel(
        self, entity: Union[Entity, IUniqueEntity]
    ) -> Optional[EntityOriginWriteModelWithId]:
        if isinstance(entity, IUniqueEntity) and (
            entity._foreignUid or entity._foreignOrigin
        ):
            if isinstance(entity, Entity):
                model = EntityOriginWriteModelWithId(
                    id=entity.id, uid=entity._foreignUid, origin=entity._foreignOrigin
                )
                if model.uid:
                    setattr(entity, "uid", model.uid)
                if model.uid:
                    setattr(entity, "origin", model.origin)
                return model

        return None

    def _createEntities(self, entityType: Type[Entity], entities: List[Entity]):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Creating of entity type %a is not implemented."
                % (
                    entityType.__name__
                    if entityType.__name__ != Entity.__name__
                    else "unknown"
                )
            )

        datasets = cast(List[Dataset], [e for e in entities if isinstance(e, Dataset)])
        entities = [e for e in entities if not isinstance(e, Dataset)]

        if len(datasets) > 0:
            for dataset in datasets:
                self._createDataset(dataset)
                self._addOriginToEntity(
                    entityType._endpoint, self._createEntityOriginWriteModel(dataset)
                )

        responseError = None
        if len(entities) == 1:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint, data=entities[0].toDict()
            )
            if responseError:
                raise EntityCreatingException(
                    entity=entities, responseError=responseError
                )

            entities[0].override(data)
            entities[0].connection = self._connection
            self._addOriginToEntity(
                entityType._endpoint, self._createEntityOriginWriteModel(entities[0])
            )

        elif len(entities) > 1:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_create"],
                data=[e.toDict() for e in entities],
            )
            if responseError:
                raise EntityCreatingException(
                    entity=entities, responseError=responseError
                )

            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)
                    entities[i].connection = self._connection
                self._addOriginToEntities(
                    entityType._endpoint,
                    [self._createEntityOriginWriteModel(e) for e in entities],
                )

    def _deleteEntitiesByTypeName(
        self,
        typeDict: Dict[str, List[Union[Constants.ID_TYPE, None]]],
        permanently: bool = False,
    ):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._deleteEntities(cast(Any, t), [e for e in entities if e], permanently)

    def _deleteEntities(
        self,
        entityType: Type[Entity],
        entityIds: List[Constants.ID_TYPE],
        permanently: bool = False,
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Deleting of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entityIds) < 1:
            return
        elif len(entityIds) == 1:
            _, responseError = self._connection.deleteEndpoint(
                entityType._endpoint + [str(entityIds[0])],
                parameters={"deletePermanently": permanently} if permanently else {},
            )
        else:
            _, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_delete"],
                data=[id for id in entityIds],
                parameters={"deletePermanently": permanently} if permanently else {},
            )

        if responseError:
            raise EntityDeletingException(
                entityIds=entityIds, responseError=responseError
            )

    @classmethod
    def _collectTypes(cls, entities: list) -> Dict[str, Any]:
        result: Dict[str, Any] = {k: [] for k in cls._entityByName.keys()}
        result["unknown"] = []

        for entity in entities:
            unknown = True

            for k, v in cls._entityByName.items():
                if isinstance(entity, v):
                    result[k].append(entity)
                    unknown = False
                    break

            if unknown:
                result["unknown"].append(entity)
        return result

    def printServerStatus(self):
        self._connection.printServerStatus()

    @overload
    def restore(self, entities: Constants.ENTITIES): ...

    @overload
    def restore(self, entities: List[Constants.ENTITIES]): ...

    # Implementation of overload
    def restore(self, entities: Any):
        def decorator(entities: Any):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityUpdatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action."
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._restoreEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def update(self, entities: Constants.ENTITIES): ...

    @overload
    def update(self, entities: List[Constants.ENTITIES]): ...

    # Implementation of overload
    def update(self, entities: Any):
        def decorator(entities: Any):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityUpdatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action."
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._updateEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def create(self, entities: _T): ...

    @overload
    def create(self, entities: List[_T]): ...

    # Implementation of overload
    def create(self, entities: Any):
        def decorator(entities: List[Entity]):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityCreatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action"
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._createEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        decorator(entities)

    @overload
    def delete(self, entities: Constants.ENTITIES, permanently=False): ...

    @overload
    def delete(self, entities: List[Constants.ENTITIES], permanently=False): ...

    # Implementation of overload
    def delete(self, entities: Any = None, permanently=False):
        def decorator(entities: Any):
            types: Dict[str, List[Union[Constants.ID_TYPE, None]]] = self._collectTypes(
                entities
            )
            typesIds = {
                typeName: cast(List, [cast(Entity, e).id for e in entities if e])
                for typeName, entities in types.items()
            }
            if len(types["unknown"]) > 0:
                raise EntityDeletingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action"
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._deleteEntitiesByTypeName(typesIds, permanently=permanently)

            for entityList in types.values():
                for entity in entityList:
                    if permanently and isinstance(entity, ConnectedEntity):
                        entity.connection = None
                    if isinstance(entity, ISoftDeletable):
                        entity.isDeleted = True

        if isinstance(entities, EntityIterator):
            raise LOGSException(
                "An %a cannot be used for delete. Please convert it to a list first."
                % EntityIterator.__name__
            )
        elif not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def deleteById(
        self, entityType: Type[Constants.ENTITIES], ids: int, permanently: bool = False
    ): ...

    @overload
    def deleteById(
        self, entityType: Type[Constants.ENTITIES], ids: str, permanently: bool = False
    ): ...

    @overload
    def deleteById(
        self,
        entityType: Type[Constants.ENTITIES],
        ids: List[int],
        permanently: bool = False,
    ): ...

    @overload
    def deleteById(
        self,
        entityType: Type[Constants.ENTITIES],
        ids: List[str],
        permanently: bool = False,
    ): ...

    # Implementation of overload
    def deleteById(self, entityType=None, ids: Any = None, permanently: bool = False):
        def decorator(entityType: Any):
            self._deleteEntities(entityType, ids, permanently=permanently)

        if ids and not isinstance(ids, list):
            ids = [ids]
        return decorator(entityType)

    def sample(self, id: int) -> Sample:
        return self._fetchEntity(Sample, id)

    def samples(self, parameter: Optional[SampleRequestParameter] = None) -> Samples:
        if parameter and not isinstance(parameter, SampleRequestParameter):
            raise LOGSException(
                "Parameter for %s.samples must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    SampleRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Samples(connection=self._connection, parameters=parameter)

    def project(self, id: int) -> Project:
        return self._fetchEntity(Project, id)

    def projects(self, parameter: Optional[ProjectRequestParameter] = None) -> Projects:
        if parameter and not isinstance(parameter, ProjectRequestParameter):
            raise LOGSException(
                "Parameter for %s.projects must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    ProjectRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Projects(connection=self._connection, parameters=parameter)

    def dataset(self, id: int) -> Dataset:
        return self._fetchEntity(Dataset, id)

    def datasets(self, parameter: Optional[DatasetRequestParameter] = None) -> Datasets:
        if parameter and not isinstance(parameter, DatasetRequestParameter):
            raise LOGSException(
                "Parameter for %s.datasets must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    DatasetRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Datasets(connection=self._connection, parameters=parameter)

    def person(self, id: int) -> Person:
        return self._fetchEntity(Person, id)

    def persons(self, parameter: Optional[PersonRequestParameter] = None) -> Persons:
        if parameter and not isinstance(parameter, PersonRequestParameter):
            raise LOGSException(
                "Parameter for %s.persons must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    PersonRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Persons(connection=self._connection, parameters=parameter)

    def method(self, id: int) -> Method:
        return self._fetchEntity(Method, id)

    def methods(self, parameter: Optional[MethodRequestParameter] = None) -> Methods:
        if parameter and not isinstance(parameter, MethodRequestParameter):
            raise LOGSException(
                "Parameter for %s.methods must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    MethodRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Methods(connection=self._connection, parameters=parameter)

    def instrument(self, id: int) -> Instrument:
        return self._fetchEntity(Instrument, id)

    def instruments(
        self, parameter: Optional[InstrumentRequestParameter] = None
    ) -> Instruments:
        if parameter and not isinstance(parameter, InstrumentRequestParameter):
            raise LOGSException(
                "Parameter for %s.instruments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    InstrumentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Instruments(connection=self._connection, parameters=parameter)

    def experiment(self, id: int) -> Experiment:
        return self._fetchEntity(Experiment, id)

    def experiments(
        self, parameter: Optional[ExperimentRequestParameter] = None
    ) -> Experiments:
        if parameter and not isinstance(parameter, ExperimentRequestParameter):
            raise LOGSException(
                "Parameter for %s.experiments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    ExperimentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Experiments(connection=self._connection, parameters=parameter)

    def origin(self, id: int) -> Origin:
        return self._fetchEntity(Origin, id)

    def origins(self, parameter: Optional[OriginRequestParameter] = None) -> Origins:
        if parameter and not isinstance(parameter, OriginRequestParameter):
            raise LOGSException(
                "Parameter for %s.origins must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    OriginRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Origins(connection=self._connection, parameters=parameter)

    def format(self, id: str) -> Format:
        return self._fetchEntity(Format, id)

    def formats(self, parameter: Optional[FormatRequestParameter] = None) -> Formats:
        if parameter and not isinstance(parameter, FormatRequestParameter):
            raise LOGSException(
                "Parameter for %s.formats must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Formats(connection=self._connection, parameters=parameter)

    def role(self, id: int) -> Role:
        return self._fetchEntity(Role, id)

    def roles(self, parameter: Optional[RoleRequestParameter] = None) -> Roles:
        if parameter and not isinstance(parameter, RoleRequestParameter):
            raise LOGSException(
                "Parameter for %s.Roles must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    RoleRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Roles(connection=self._connection, parameters=parameter)

    def bridge(self, id: int) -> Bridge:
        return self._fetchEntity(Bridge, id)

    def bridges(self, parameter: Optional[BridgeRequestParameter] = None) -> Bridges:
        if parameter and not isinstance(parameter, BridgeRequestParameter):
            raise LOGSException(
                "Parameter for %s.Bridges must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    BridgeRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Bridges(connection=self._connection, parameters=parameter)

    def dataSource(self, id: int) -> DataSource:
        return self._fetchEntity(DataSource, id)

    def dataSources(
        self, parameter: Optional[DataSourceRequestParameter] = None
    ) -> DataSources:
        if parameter and not isinstance(parameter, DataSourceRequestParameter):
            raise LOGSException(
                "Parameter for %s.DataSources must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    DataSourceRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return DataSources(connection=self._connection, parameters=parameter)

    def labNotebook(self, id: int) -> LabNotebook:
        return self._fetchEntity(LabNotebook, id)

    def labNotebooks(
        self, parameter: Optional[LabNotebookRequestParameter] = None
    ) -> LabNotebooks:
        if parameter and not isinstance(parameter, LabNotebookRequestParameter):
            raise LOGSException(
                "Parameter for %s.LabNotebooks must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    LabNotebookRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebooks(connection=self._connection, parameters=parameter)

    def labNotebookExperiment(self, id: int) -> LabNotebookExperiment:
        return self._fetchEntity(LabNotebookExperiment, id)

    def labNotebookExperiments(
        self, parameter: Optional[LabNotebookExperimentRequestParameter] = None
    ) -> LabNotebookExperiments:
        if parameter and not isinstance(
            parameter, LabNotebookExperimentRequestParameter
        ):
            raise LOGSException(
                "Parameter for %s.LabNotebookExperiments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    LabNotebookExperimentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebookExperiments(connection=self._connection, parameters=parameter)

    def labNotebookEntry(self, id: int) -> LabNotebookEntry:
        return self._fetchEntity(LabNotebookEntry, id)

    def labNotebookEntries(
        self, parameter: Optional[LabNotebookEntryRequestParameter] = None
    ) -> LabNotebookEntries:
        if parameter and not isinstance(parameter, LabNotebookEntryRequestParameter):
            raise LOGSException(
                "Parameter for %s.LabNotebookEntries must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    LabNotebookEntryRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebookEntries(connection=self._connection, parameters=parameter)

    def formatVendor(self, id: int) -> FormatVendor:
        return self._fetchEntity(FormatVendor, id)

    def formatVendors(
        self, parameter: Optional[FormatVendorRequestParameter] = None
    ) -> FormatVendors:
        if parameter and not isinstance(parameter, FormatVendorRequestParameter):
            raise LOGSException(
                "Parameter for %s.Vendors must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatVendorRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatVendors(connection=self._connection, parameters=parameter)

    def formatMethod(self, id: int) -> FormatMethod:
        return self._fetchEntity(FormatMethod, id)

    def formatMethods(
        self, parameter: Optional[FormatMethodRequestParameter] = None
    ) -> FormatMethods:
        if parameter and not isinstance(parameter, FormatMethodRequestParameter):
            raise LOGSException(
                "Parameter for %s.Methods must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatMethodRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatMethods(connection=self._connection, parameters=parameter)

    def formatInstrument(self, id: int) -> FormatInstrument:
        return self._fetchEntity(FormatInstrument, id)

    def formatInstruments(
        self, parameter: Optional[FormatInstrumentRequestParameter] = None
    ) -> FormatInstruments:
        if parameter and not isinstance(parameter, FormatInstrumentRequestParameter):
            raise LOGSException(
                "Parameter for %s.Instruments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatInstrumentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatInstruments(connection=self._connection, parameters=parameter)

    def formatFormat(self, id: int) -> FormatFormat:
        return self._fetchEntity(FormatFormat, id)

    def formatFormats(
        self, parameter: Optional[FormatFormatRequestParameter] = None
    ) -> FormatFormats:
        if parameter and not isinstance(parameter, FormatFormatRequestParameter):
            raise LOGSException(
                "Parameter for %s.Formats must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatFormatRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatFormats(connection=self._connection, parameters=parameter)

    def customField(self, id: int) -> CustomField:
        return self._fetchEntity(CustomField, id)

    def customFields(
        self, parameter: Optional[CustomFieldRequestParameter] = None
    ) -> CustomFields:
        if parameter and not isinstance(parameter, CustomFieldRequestParameter):
            raise LOGSException(
                "Parameter for %s.CustomFields must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    CustomFieldRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return CustomFields(connection=self._connection, parameters=parameter)

    def customType(self, id: int) -> CustomType:
        return self._fetchEntity(CustomType, id)

    def customTypes(
        self, parameter: Optional[CustomTypeRequestParameter] = None
    ) -> CustomTypes:
        if parameter and not isinstance(parameter, CustomTypeRequestParameter):
            raise LOGSException(
                "Parameter for %s.CustomTypes must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    CustomTypeRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return CustomTypes(connection=self._connection, parameters=parameter)

    def inventory(self, id: int) -> Inventory:
        return self._fetchEntity(Inventory, id)

    def inventories(
        self, parameter: Optional[InventoryRequestParameter] = None
    ) -> Inventories:
        if parameter and not isinstance(parameter, InventoryRequestParameter):
            raise LOGSException(
                "Parameter for %s.Inventories must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    InventoryRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Inventories(connection=self._connection, parameters=parameter)

    def entity(self, uid: str):
        return Entities(connection=self._connection).fetch(uid=uid)

    def entities(
        self, parameter: Optional[EntitiesRequestParameter] = None
    ) -> Entities:
        return Entities(connection=self._connection, parameters=parameter)

    def datasetMatching(
        self,
        files: Union[Constants.FILE_TYPE, Sequence[Constants.FILE_TYPE]],
        formatIds: Optional[List[str]] = None,
        ignoreReadErrors=False,
    ) -> DatasetMatching:
        return DatasetMatching(
            connection=self._connection,
            files=files,
            formatIds=formatIds,
            ignoreReadErrors=ignoreReadErrors,
        )

    def updatableDatasetFiles(
        self, files: Sequence[Constants.FILE_TYPE], formatIds: List[str]
    ):
        datasets = Datasets(
            connection=self._connection, parameters=cast(DatasetRequestParameter, {})
        ).findDatasetByFiles(files=files, formatIds=formatIds)
        for dataset in datasets:
            yield DatasetsUpdatableFiles(
                datasetId=dataset.logsId,
                files=[
                    FileEntry(fullPath=file.fullPath, state=file.state)
                    for file in dataset.files
                ],
            )

    @property
    def instanceOrigin(self) -> Origin:
        return Origin(name="LOGS (%s)" % self.group, url=self.url, uid=self.uid)

    @property
    def url(self) -> str:
        return self._connection.url

    @property
    def apiUrl(self) -> str:
        return self._connection.apiUrl

    @property
    def uid(self) -> Optional[UUID]:
        return self._connection.metadata.uid

    @property
    def group(self) -> Optional[str]:
        return self._connection._group

    @property
    def currentUser(self) -> Person:
        return self._currentUser

    @property
    def cacheDir(self) -> Optional[str]:
        return self._cacheDir

    @cacheDir.setter
    def cacheDir(self, value):
        self._cacheDir = Tools.checkAndConvert(value, str, "cacheDir")

    def version(self) -> Optional[str]:
        return self._connection.metadata.version

    @property
    def metadata(self) -> ServerMetaData:
        return self._connection.metadata


if __name__ == "__main__":
    api_key = input("Please specify api key: ")
    _url = input("Please specify LOGS url: ")

    # Example input:
    # api_key = "8V6oQ804t2nPgGPDJIk4CuneRI5q48ERUxgEpk+YqXzX9uLuMUySycHkeXP6DefN"
    # url = "http://localhost:900/sandbox"

    logs = LOGS(
        _url, api_key, options=LOGSOptions(showRequestUrl=True, showRequestBody=False)
    )
