from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.DataSource import DataSource
from LOGS.Entities.DataSourceRequestParameter import DataSourceRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("autoload_configurations")
class DataSources(EntityIterator[DataSource, DataSourceRequestParameter]):
    """LOGS connected class AutouploadSource iterator"""

    _generatorType = DataSource
    _parameterType = DataSourceRequestParameter
