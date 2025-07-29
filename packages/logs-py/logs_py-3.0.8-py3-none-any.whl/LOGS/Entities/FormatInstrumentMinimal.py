from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.FormatInstrument import FormatInstrument
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(FormatInstrument)
class FormatInstrumentMinimal(EntityMinimalWithStrId[FormatInstrument]):
    pass
