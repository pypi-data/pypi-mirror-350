from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Optional, TypeVar, Union

from LOGS.Entity.SerializableContent import SerializableClass
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest


class DefaultOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"


_Sorting = TypeVar("_Sorting", bound=Enum)


@dataclass
class EntityRequestParameter(Generic[_Sorting], SerializableClass, IPaginationRequest):
    _noSerialize = ["asString"]
    excludeIds: Optional[Union[List[int], List[str]]] = None
    searchTerm: Optional[str] = None
    ids: Optional[Union[List[int], List[str]]] = None
    includeCount: Optional[bool] = None
    includeRelations: Optional[bool] = True
    orderby: Optional[_Sorting] = None
