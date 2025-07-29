from dataclasses import dataclass
from typing import Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class FormatMethodRequestParameter(EntityRequestParameter):
    name: Optional[str] = None
