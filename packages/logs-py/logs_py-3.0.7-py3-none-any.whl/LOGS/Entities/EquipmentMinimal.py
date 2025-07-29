from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Equipment import Equipment
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Equipment)
class EquipmentMinimal(EntityMinimalWithIntId[Equipment]):
    pass
