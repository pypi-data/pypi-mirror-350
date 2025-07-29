from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import DefaultOrder, EntityRequestParameter


@dataclass
class FormatRequestParameter(EntityRequestParameter[DefaultOrder]):
    name: Optional[str] = None
    vendors: Optional[List[str]] = None
    vendors: Optional[List[str]] = None
    methods: Optional[List[str]] = None
    formats: Optional[List[str]] = None
    instruments: Optional[List[str]] = None
