"""
fastTabou - Framework for Tabu Search algorithms with sequential and parallel implementations
"""

from .sequential.tabu_search import TabuSearch
from .sequential.utils import default_aspiration, frequency_aspiration, diversification_stop
from .parallel.parallel_tabu import ParallelTabuSearch
from .parallel.utils import default_stopping_condition, basic_aspiration, diversification_aspiration, frequency_based_intensification, restart_based_diversification
from .common.neighborhood import NeighborhoodGenerator, CompositeNeighborhood
from .common.solution import Solution


__version__ = "0.2.28"
__all__ = ['TabuSearch',
           'ParallelTabuSearch',
           'default_aspiration',
           'frequency_aspiration',
           'diversification_stop',
           'NeighborhoodGenerator',
           'CompositeNeighborhood',
           'Solution',
           'default_stopping_condition',
           'basic_aspiration',
           'diversification_aspiration',
           'frequency_based_intensification',
           'restart_based_diversification',
           'parallel_tabu_utils'
           ]