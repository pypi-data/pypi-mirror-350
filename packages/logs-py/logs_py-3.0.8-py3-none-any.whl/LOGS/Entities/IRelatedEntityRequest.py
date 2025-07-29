from dataclasses import dataclass
from typing import Optional


@dataclass
class IRelatedEntityRequest:
    includeRelations: Optional[bool] = None
    includeRelationLink: Optional[bool] = None
    includeRelationCount: Optional[bool] = None
