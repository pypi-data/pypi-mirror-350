from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.FormatFormat import FormatFormat
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(FormatFormat)
class FormatFormatMinimal(EntityMinimalWithStrId[FormatFormat]):
    pass
