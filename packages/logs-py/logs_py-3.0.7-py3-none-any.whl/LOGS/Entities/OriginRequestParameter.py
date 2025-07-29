from dataclasses import dataclass
from typing import List, Optional, Sequence, Union
from uuid import UUID

from LOGS.Entity.EntityRequestParameter import DefaultOrder, EntityRequestParameter
from LOGS.Interfaces.INamedEntity import INamedEntityRequest


@dataclass
class OriginRequestParameter(EntityRequestParameter[DefaultOrder], INamedEntityRequest):
    urls: Optional[List[str]] = None
    uids: Optional[Sequence[Union[UUID, str]]] = None
