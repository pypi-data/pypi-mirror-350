from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.FormatVendor import FormatVendor
from LOGS.Entity.EntityMinimalWithStrId import EntityMinimalWithStrId


@FullModel(FormatVendor)
class FormatVendorMinimal(EntityMinimalWithStrId[FormatVendor]):
    pass
