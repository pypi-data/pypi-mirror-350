from dataclasses import dataclass
from typing import Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class FormatVendorRequestParameter(EntityRequestParameter):
    name: Optional[str] = None
    includeIcon: Optional[bool] = None
