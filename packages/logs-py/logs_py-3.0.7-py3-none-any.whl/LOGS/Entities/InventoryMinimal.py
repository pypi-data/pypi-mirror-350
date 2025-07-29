from typing import Optional

from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Inventory import Inventory
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Inventory)
class InventoryMinimal(EntityMinimalWithIntId[Inventory]):
    _inventoryName: Optional[str] = None

    @property
    def inventoryName(self) -> Optional[str]:
        return self._inventoryName

    @inventoryName.setter
    def inventoryName(self, value):
        self._inventoryName = self.checkAndConvert(
            value, str, "inventoryName", allowNone=True
        )
