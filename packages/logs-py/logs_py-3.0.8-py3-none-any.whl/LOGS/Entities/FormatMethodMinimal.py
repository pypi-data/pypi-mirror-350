from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.FormatMethod import FormatMethod
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(FormatMethod)
class FormatMethodMinimal(EntityMinimalWithStrId[FormatMethod]):
    pass
