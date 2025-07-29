from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.FormatMethod import FormatMethod
from LOGS.Entities.FormatMethodRequestParameter import FormatMethodRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("parser_methods")
class FormatMethods(EntityIterator[FormatMethod, FormatMethodRequestParameter]):
    """LOGS connected class FromatMethod iterator"""

    _generatorType = FormatMethod
    _parameterType = FormatMethodRequestParameter
