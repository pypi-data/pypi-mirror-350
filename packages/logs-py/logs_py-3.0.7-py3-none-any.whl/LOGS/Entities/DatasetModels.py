from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from LOGS.Entity.SerializableContent import SerializableClass, SerializableContent


class DatasetSourceType(Enum):
    ManualUpload = 0
    SFTPAutoload = 1
    ClientAutoload = 2
    APIUpload = 3


class ParsedMetadata(SerializableContent):
    Parameters: bool = False
    Tracks: bool = False
    TrackCount: int = False
    TrackViewerTypes: List[str] = []


@dataclass
class DatasetSource(SerializableClass):
    id: Optional[int] = None
    type: Optional[DatasetSourceType] = None
    name: Optional[str] = None


class ViewableEntityTypes(Enum):
    ELN = "ELN"
    CustomField = "CustomField"
