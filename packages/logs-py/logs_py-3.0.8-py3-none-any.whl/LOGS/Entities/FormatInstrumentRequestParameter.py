from dataclasses import dataclass
from typing import Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class FormatInstrumentRequestParameter(EntityRequestParameter):
    name: Optional[str] = None
