import numpy as np
from typing import List
from ..common.population import Population

# Fonction utilitaire pour diviser la population
def split_population(pop: Population, n: int) -> List[Population]:
    indices = np.array_split(np.arange(len(pop.individuals)), n)
    return [Population([pop.individuals[i] for i in idx]) for idx in indices]