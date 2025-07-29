from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.FormatVendor import FormatVendor
from LOGS.Entities.FormatVendorRequestParameter import FormatVendorRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("vendors")
class FormatVendors(EntityIterator[FormatVendor, FormatVendorRequestParameter]):
    """LOGS connected class FormatVendors iterator"""

    _generatorType = FormatVendor
    _parameterType = FormatVendorRequestParameter
