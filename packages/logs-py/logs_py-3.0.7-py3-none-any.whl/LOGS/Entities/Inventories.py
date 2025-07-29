from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Inventory import Inventory
from LOGS.Entities.InventoryRequestParameter import InventoryRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("inventories")
class Inventories(EntityIterator[Inventory, InventoryRequestParameter]):
    """LOGS connected Inventories iterator"""

    _generatorType = Inventory
    _parameterType = InventoryRequestParameter
