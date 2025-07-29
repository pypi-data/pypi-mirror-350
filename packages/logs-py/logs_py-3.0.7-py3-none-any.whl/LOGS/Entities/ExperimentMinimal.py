from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Experiment import Experiment
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Experiment)
class ExperimentMinimal(EntityMinimalWithIntId[Experiment]):
    pass
