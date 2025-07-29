from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Method import Method
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Method)
class MethodMinimal(EntityMinimalWithIntId[Method]):
    pass
