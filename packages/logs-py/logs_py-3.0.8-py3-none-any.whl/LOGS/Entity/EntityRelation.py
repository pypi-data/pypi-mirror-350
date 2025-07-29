from typing import Generator, Generic, Optional, TypeVar

from LOGS.Entity.Entity import Entity
from LOGS.Entity.EntityIterator import EntityIterator
from LOGS.Entity.SerializableContent import SerializableContent

_T = TypeVar("_T", bound=Entity)


class EntityRelation(Generic[_T], SerializableContent):
    _noSerialize = ["link", "entities"]
    _count: Optional[int] = None
    _link: Optional[str] = None
    _entities: Optional[EntityIterator] = None

    def __init__(self, ref=None, entities: Optional[EntityIterator] = None):
        self._entities = entities

        super().__init__(ref=ref)

    def __iter__(self) -> Generator[_T, None, None]:
        if self._entities:
            for item in self._entities:
                yield item

    def __str__(self):
        return "<%s to %a>" % (
            type(self).__name__,
            type(self._entities).__name__.lower() if self._entities else "",
        )

    @property
    def count(self) -> Optional[int]:
        return self._count

    @count.setter
    def count(self, value):
        self._count = self.checkAndConvert(value, int, "count")

    @property
    def link(self) -> Optional[str]:
        return self._link

    @link.setter
    def link(self, value):
        self._link = self.checkAndConvert(value, str, "link")
        if self._entities:
            self._entities._firstUrl = self._link

    @property
    def entities(self) -> Optional[EntityIterator]:
        return self._entities
