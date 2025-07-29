from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Optional, Type, TypeVar

from LOGS.Auxiliary import Tools
from LOGS.Interfaces.IEntityInterface import IEntityInterface
from LOGS.Interfaces.IRelationModel import IRelationModel

if TYPE_CHECKING:
    pass


_Relations = TypeVar("_Relations", bound=IRelationModel)


@dataclass
class IRelatedEntity(Generic[_Relations], IEntityInterface):
    # The expression here should be _relationType: Optional[Type[_Relations]] = None, but it is not working
    _relationType: Optional[Type] = None
    _relations: Optional[_Relations] = None

    @property
    def relations(self) -> Optional[_Relations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        if not self._relationType:
            raise NotImplementedError(
                "Relation class definition (_relationType) for of entity type %a is missing."
                % (type(self).__name__)
            )

        self._relations = Tools.checkAndConvert(
            value, self._relationType, "relations", allowNone=True
        )
