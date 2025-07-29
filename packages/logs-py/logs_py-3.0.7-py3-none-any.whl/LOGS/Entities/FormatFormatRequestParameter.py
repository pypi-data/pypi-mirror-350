from dataclasses import dataclass

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest


@dataclass
class FormatFormatRequestParameter(EntityRequestParameter, IPermissionedEntityRequest):
    pass
