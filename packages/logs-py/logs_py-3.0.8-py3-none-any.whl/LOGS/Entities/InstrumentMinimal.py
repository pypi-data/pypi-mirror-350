from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Instrument import Instrument
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Instrument)
class InstrumentMinimal(EntityMinimalWithIntId[Instrument]):
    pass
