from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.FormatInstrument import FormatInstrument
from LOGS.Entities.FormatInstrumentRequestParameter import (
    FormatInstrumentRequestParameter,
)
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("parser_instruments")
class FormatInstruments(
    EntityIterator[FormatInstrument, FormatInstrumentRequestParameter]
):
    """LOGS connected class FormatInstrument iterator"""

    _generatorType = FormatInstrument
    _parameterType = FormatInstrumentRequestParameter
