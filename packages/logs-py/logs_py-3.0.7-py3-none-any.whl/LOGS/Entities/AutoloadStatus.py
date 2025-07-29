from datetime import datetime
from typing import List, Optional
from uuid import UUID

from LOGS.Entities.AutoloadStatusError import AutoloadStatusError
from LOGS.Entities.BridgeType import BridgeType
from LOGS.Entities.RunState import RunState
from LOGS.Entity.SerializableContent import SerializableClass


class AutoloadStatus(SerializableClass):
    type: Optional[BridgeType]
    uuid: Optional[UUID]
    lastUpdated: Optional[datetime]
    counter: Optional[int]
    dataSourceId: Optional[int]
    runState: Optional[RunState]
    startedOn: Optional[datetime]
    duration: Optional[str]
    errors: Optional[List[AutoloadStatusError]]
    info: Optional[dict]
