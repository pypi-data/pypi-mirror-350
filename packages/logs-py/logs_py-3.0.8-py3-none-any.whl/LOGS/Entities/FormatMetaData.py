from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.FormatFormatMinimal import FormatFormatMinimal
    from LOGS.Entities.FormatInstrumentMinimal import FormatInstrumentMinimal
    from LOGS.Entities.FormatMethodMinimal import FormatMethodMinimal
    from LOGS.Entities.FormatVendorMinimal import FormatVendorMinimal


class FormatMetaData(ConnectedEntity):
    _vendor: List["FormatVendorMinimal"]
    _method: List["FormatMethodMinimal"]
    _format: List["FormatFormatMinimal"]
    _instrument: List["FormatInstrumentMinimal"]

    def __init__(self, ref=None, connection: Optional[LOGSConnection] = None):
        self._vendor = []
        self._method = []
        self._format = []
        self._instrument = []
        super().__init__(ref=ref, connection=connection)

    @property
    def vendor(self) -> List["FormatVendorMinimal"]:
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = MinimalFromList(
            value, "FormatVendorMinimal", "vendor", connection=self.connection
        )

    @property
    def method(self) -> List["FormatMethodMinimal"]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MinimalFromList(
            value, "FormatMethodMinimal", "method", connection=self.connection
        )

    @property
    def format(self) -> List["FormatFormatMinimal"]:
        return self._format

    @format.setter
    def format(self, value):
        self._format = MinimalFromList(
            value, "FormatFormatMinimal", "format", connection=self.connection
        )

    @property
    def instrument(self) -> List["FormatInstrumentMinimal"]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = MinimalFromList(
            value, "FormatInstrumentMinimal", "instrument", connection=self.connection
        )
