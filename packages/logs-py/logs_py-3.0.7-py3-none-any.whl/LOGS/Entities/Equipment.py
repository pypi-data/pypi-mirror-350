from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.Entity import Entity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity


@Endpoint("equipments")
class Equipment(Entity, IOwnedEntity):
    pass
