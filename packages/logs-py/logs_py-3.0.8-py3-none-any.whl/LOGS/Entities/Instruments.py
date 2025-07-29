from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Instrument import Instrument
from LOGS.Entities.InstrumentRequestParameter import InstrumentRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("instruments")
class Instruments(EntityIterator[Instrument, InstrumentRequestParameter]):
    """LOGS connected Person iterator"""

    _generatorType = Instrument
    _parameterType = InstrumentRequestParameter
