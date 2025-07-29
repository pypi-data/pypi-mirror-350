from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entities.OriginMinimal import OriginMinimal
from LOGS.Entity.SerializableContent import SerializableClass


@dataclass
class EntityOriginWriteModelWithId(SerializableClass):
    _noSerialize = ["asString"]
    id: Optional[Constants.ID_TYPE] = None
    uid: Optional[UUID] = None
    origin: Optional[OriginMinimal] = None
