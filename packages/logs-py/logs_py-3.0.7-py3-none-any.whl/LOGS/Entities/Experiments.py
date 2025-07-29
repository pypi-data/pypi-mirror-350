from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Experiment import Experiment
from LOGS.Entities.ExperimentRequestParameter import ExperimentRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("experiments")
class Experiments(EntityIterator[Experiment, ExperimentRequestParameter]):
    """LOGS connected Person iterator"""

    _generatorType = Experiment
    _parameterType = ExperimentRequestParameter
