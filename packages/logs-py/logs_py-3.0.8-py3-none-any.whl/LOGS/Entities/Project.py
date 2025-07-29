from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.ProjectPersonPermission import ProjectPersonPermission
from LOGS.Entities.ProjectRelations import ProjectRelations
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Entity.SerializableContent import SerializableClass
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import GenericPermissionEntity
from LOGS.Interfaces.IRelatedEntity import IRelatedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


class ProjectTag(SerializableClass):
    id: Optional[int] = None
    name: Optional[str] = None

    def __str__(self):
        s = (" name:'%s'" % getattr(self, "name")) if hasattr(self, "name") else ""
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)


@Endpoint("projects")
class Project(
    IEntityWithIntId,
    INamedEntity,
    IRelatedEntity[ProjectRelations],
    IUniqueEntity,
    ICreationRecord,
    IModificationRecord,
    IOwnedEntity,
    GenericPermissionEntity,
):
    _relationType = ProjectRelations

    _notes: Optional[str]
    _projectTags: Optional[List[ProjectTag]]
    _relations: Optional[ProjectRelations]
    _projectPersonPermissions: Optional[List[ProjectPersonPermission]]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: Optional[str] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._name = name
        self._notes = None
        self._projectTags = None
        self._relations = None
        self._projectPersonPermissions = None
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def projectTags(self) -> Optional[List[ProjectTag]]:
        return self._projectTags

    @projectTags.setter
    def projectTags(self, value):
        self._projectTags = self.checkListAndConvertNullable(
            value, ProjectTag, "projectTags"
        )

    @property
    def relations(self) -> Optional[ProjectRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        self._relations = self.checkAndConvertNullable(
            value, ProjectRelations, "relations"
        )

    @property
    def projectPersonPermissions(self) -> Optional[List[ProjectPersonPermission]]:
        return self._projectPersonPermissions

    @projectPersonPermissions.setter
    def projectPersonPermissions(self, value):
        self._projectPersonPermissions = self.checkListAndConvertNullable(
            value, ProjectPersonPermission, "projectPersonPermissions"
        )
