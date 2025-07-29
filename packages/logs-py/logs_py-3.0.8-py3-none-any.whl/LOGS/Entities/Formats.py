from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities import Format
from LOGS.Entities.FormatRequestParameter import FormatRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("parsers")
class Formats(EntityIterator[Format, FormatRequestParameter]):
    """LOGS connected Formats iterator"""

    _generatorType = Format
    _parameterType = FormatRequestParameter
