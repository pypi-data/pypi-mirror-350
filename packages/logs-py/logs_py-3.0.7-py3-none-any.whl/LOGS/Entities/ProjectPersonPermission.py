from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromSingle
from LOGS.Entity.SerializableContent import SerializableContent

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.ProjectMinimal import ProjectMinimal


class ProjectPersonPermission(SerializableContent):
    _person: Optional["PersonMinimal"] = None
    _project: Optional["ProjectMinimal"] = None
    _administer: Optional[bool] = None
    _edit: Optional[bool] = None
    _add: Optional[bool] = None
    _read: Optional[bool] = None

    @property
    def person(self) -> Optional["PersonMinimal"]:
        return self._person

    @person.setter
    def person(self, value):
        self._person = MinimalFromSingle(value, "PersonMinimal", "person")

    @property
    def project(self) -> Optional["ProjectMinimal"]:
        return self._project

    @project.setter
    def project(self, value):
        self._project = MinimalFromSingle(value, "ProjectMinimal", "project")

    @property
    def administer(self) -> Optional[bool]:
        return self._administer

    @administer.setter
    def administer(self, value):
        self._administer = self.checkAndConvertNullable(value, bool, "administer")

    @property
    def edit(self) -> Optional[bool]:
        return self._edit

    @edit.setter
    def edit(self, value):
        self._edit = self.checkAndConvertNullable(value, bool, "edit")

    @property
    def add(self) -> Optional[bool]:
        return self._add

    @add.setter
    def add(self, value):
        self._add = self.checkAndConvertNullable(value, bool, "add")

    @property
    def read(self) -> Optional[bool]:
        return self._read

    @read.setter
    def read(self, value):
        self._read = self.checkAndConvertNullable(value, bool, "read")
