"""
fastGA-hpc - Framework for Genetic Algorithms

Expose les classes principales :
- GeneticAlgorithm : Algorithme séquentiel de base
- ParallelGeneticAlgorithm : Version parallèle
- Chromosome : Classe de base pour les solutions
"""

from .core.genetic_algorithm import GeneticAlgorithm
from .parallel.parallel_ga import MasterSlaveModel, CellularModel, IslandModel, ParallelGA
from .common.chromosome import Chromosome
from .common.population import Population
from .core.operators import Crossover, Mutator
from .utils import default_stopping_condition, basic_aspiration, diversification_aspiration, frequency_based_intensification, restart_based_diversification


__version__ = "0.2.12"
__all__ = [
    'GeneticAlgorithm',
    'MasterSlaveModel',
    'CellularModel',
    'IslandModel',
    'ParallelGA',
    'Chromosome',
    'Population',
    'Crossover',
    'Mutator',
    'default_stopping_condition',
    'basic_aspiration',
    'diversification_aspiration',
    'frequency_based_intensification',
    'restart_based_diversification',
]