from datetime import datetime
from typing import List, Optional

from regex import Regex

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.CustomSchemaSection import CustomSchemaSection
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("custom_fields")
class CustomSchema(EntityWithStrId, IOwnedEntity, INamedEntity):
    _createdAt: Optional[datetime]
    _enabled: Optional[bool]
    _sections: Optional[List[CustomSchemaSection]]

    _alphanumeric = Regex(r"[^a-zA-Z0-9_]")

    def __init__(
        self,
        ref=None,
        id: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
        name: str = "",
    ):
        self._name = name
        if id is None or id == "":
            id = self._idFromName(name)
        self._createdAt = None
        self._enabled = None
        self._sections = None

        super().__init__(connection=connection, id=id, ref=ref)

    @classmethod
    def _idFromName(cls, name):
        return cls._alphanumeric.sub("_", name).lower()

    @property
    def createdAt(self) -> Optional[datetime]:
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.checkAndConvertNullable(value, datetime, "createdAt")

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvert(value, str, "name", allowNone=True)
        if self.id is None or self.id == "":
            self.id = self._idFromName(self._name)

    @property
    def enabled(self) -> Optional[bool]:
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = self.checkAndConvertNullable(value, bool, "enabled")

    @property
    def sections(self) -> Optional[List[CustomSchemaSection]]:
        return self._sections

    @sections.setter
    def sections(self, value):
        self._sections = self.checkListAndConvertNullable(
            value, CustomSchemaSection, "sections"
        )
