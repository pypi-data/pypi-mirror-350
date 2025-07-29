from typing import List, Optional

from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Format import Format
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(Format)
class FormatMinimal(EntityMinimalWithStrId[Format]):
    _version: Optional[List[str]] = None

    @property
    def version(self) -> Optional[List[str]]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkListAndConvertNullable(value, str, "version")
