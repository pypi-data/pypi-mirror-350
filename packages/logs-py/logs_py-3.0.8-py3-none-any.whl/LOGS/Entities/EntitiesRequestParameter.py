from dataclasses import dataclass
from typing import List, Optional, Sequence, Union
from uuid import UUID

from LOGS.Entity.SerializableContent import SerializableClass


@dataclass
class EntitiesRequestParameter(SerializableClass):
    _noSerialize = ["asString"]
    uids: Optional[Sequence[Union[str, UUID]]] = None
    names: Optional[List[str]] = None
