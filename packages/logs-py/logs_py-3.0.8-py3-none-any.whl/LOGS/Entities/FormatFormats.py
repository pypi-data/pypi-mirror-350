from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.FormatFormat import FormatFormat
from LOGS.Entities.FormatFormatRequestParameter import FormatFormatRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("parser_formats")
class FormatFormats(EntityIterator[FormatFormat, FormatFormatRequestParameter]):
    """LOGS connected class FormatFormat iterator"""

    _generatorType = FormatFormat
    _parameterType = FormatFormatRequestParameter
