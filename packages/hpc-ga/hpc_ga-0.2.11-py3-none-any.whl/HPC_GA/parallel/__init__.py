"""
Implémentations parallèles :
- ParallelGeneticAlgorithm : Modèle d'îlots parallèles
- Utilitaires pour MPI/multiprocessing
"""

from .parallel_ga import MasterSlaveModel, CellularModel, IslandModel, ParallelGA
from .utils import split_population

__all__ = [
    'ParallelGA',
    'IslandModel',
    'MasterSlaveModel',
    'CellularModel',
    'split_population'
]