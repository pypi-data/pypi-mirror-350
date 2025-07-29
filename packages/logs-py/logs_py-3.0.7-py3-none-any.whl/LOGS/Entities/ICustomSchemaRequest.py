from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ICustomSchemaRequest:
    typeIds: Optional[List[str]] = None
