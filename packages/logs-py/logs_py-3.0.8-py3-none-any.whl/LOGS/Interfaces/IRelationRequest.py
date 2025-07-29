from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    pass


@dataclass
class IRelationRequest:
    includePermissions: Optional[bool] = None
    includeRelationLink: Optional[bool] = None
    includeRelationCount: Optional[bool] = None
