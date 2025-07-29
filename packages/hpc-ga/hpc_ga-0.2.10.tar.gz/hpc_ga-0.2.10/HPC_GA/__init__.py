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

__version__ = "0.2.10"
__all__ = [
    'GeneticAlgorithm',
    'MasterSlaveModel',
    'CellularModel',
    'IslandModel',
    'ParallelGA',
    'Chromosome',
    'Population',
    'Crossover',
    'Mutator'
]