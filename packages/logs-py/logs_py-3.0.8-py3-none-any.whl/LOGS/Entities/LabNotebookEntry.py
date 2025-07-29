from datetime import datetime
from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import EntityFetchingException, EntityIncompleteException
from LOGS.Entities.LabNotebookEntryContent.EntryContentConverter import (
    EntryContentConverter,
)
from LOGS.Entities.LabNotebookEntryContent.EntryContentDocument import (
    EntryContentDocument,
)
from LOGS.Entities.LabNotebookEntryRelations import LabNotebookEntryRelations
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable


@Endpoint("lab_notebook_entries")
class LabNotebookEntry(
    IEntityWithIntId,
    IRelatedEntity[LabNotebookEntryRelations],
    INamedEntity,
    ICreationRecord,
    IModificationRecord,
    ISoftDeletable,
    GenericPermissionEntity,
):
    _relationType = LabNotebookEntryRelations
    _noContent: bool = True

    _version: Optional[int] = None
    _labNotebook: Optional[EntityMinimalWithIntId] = None
    _labNotebookExperiment: Optional[EntityMinimalWithIntId] = None
    _entryDate: Optional[datetime] = None
    _content: Optional[EntryContentDocument] = None

    def fromDict(self, ref) -> None:
        if isinstance(ref, dict):
            if "name" in ref and ref["name"]:
                ref["name"] = ref["name"].replace(" > ", "_")

        super().fromDict(ref)

    def fetchContent(self):
        connection, endpoint, id = self._getConnectionData()

        content, responseError = connection.getEndpoint(endpoint + [id, "content"])
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        self.content = content
        self._noContent = False

    @property
    def version(self) -> Optional[int]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvertNullable(value, int, "version")

    @property
    def labNotebook(self) -> Optional[EntityMinimalWithIntId]:
        return self._labNotebook

    @labNotebook.setter
    def labNotebook(self, value):
        self._labNotebook = self.checkAndConvertNullable(
            value, EntityMinimalWithIntId, "labNotebook"
        )

    @property
    def labNotebookExperiment(self) -> Optional[EntityMinimalWithIntId]:
        return self._labNotebookExperiment

    @labNotebookExperiment.setter
    def labNotebookExperiment(self, value):
        self._labNotebookExperiment = self.checkAndConvertNullable(
            value, EntityMinimalWithIntId, "labNotebookExperiment"
        )

    @property
    def entryDate(self) -> Optional[datetime]:
        return self._entryDate

    @entryDate.setter
    def entryDate(self, value):
        self._entryDate = self.checkAndConvertNullable(value, datetime, "entryDate")

    @property
    def content(self) -> Optional[EntryContentDocument]:
        if self._noContent:
            raise EntityIncompleteException(
                self,
                parameterName="content",
                functionName=f"{self.fetchContent.__name__}()",
                hasFetchFull=False,
            )
        return self._content

    @content.setter
    def content(self, value):
        if value:
            self._noContent = False
        self._content = EntryContentConverter[EntryContentDocument].convert(
            value, fieldName="content"
        )
