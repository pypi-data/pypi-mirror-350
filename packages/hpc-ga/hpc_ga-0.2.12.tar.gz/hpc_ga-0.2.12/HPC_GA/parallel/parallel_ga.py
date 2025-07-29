import ray
import numpy as np
import random
from typing import List, Callable, Dict, Any, Optional
from abc import ABC, abstractmethod
from ..common.population import Population
from ..common.chromosome import Chromosome
from ..core.genetic_algorithm import GeneticAlgorithm
from ..parallel.utils import split_population

# Initialisation de Ray (à faire une seule fois dans l'application)
ray.init(ignore_reinit_error=True)

@ray.remote
class IslandActor:
    """Acteur Ray pour exécuter un algorithme génétique sur une île"""
    def __init__(self, ga_class, ga_config: Dict[str, Any]):
        self.ga = ga_class(**ga_config)
        
    def run_generation(self) -> Population:
        self.ga._evolve()
        return self.ga.population
    
    def get_best(self) -> Chromosome:
        return self.ga.population.best()
    
    def receive_migrants(self, migrants: List[Chromosome]):
        # Stratégie de remplacement configurable
        replace_strategy = self.ga_config.get('migration_strategy', 'worst')
        
        if replace_strategy == 'worst':
            self.ga.population.individuals.sort()
            for i, migrant in enumerate(migrants):
                if i < len(self.ga.population.individuals):
                    self.ga.population.individuals[i] = migrant
        elif replace_strategy == 'random':
            indices = np.random.choice(len(self.ga.population.individuals), size=len(migrants), replace=False)
            for i, idx in enumerate(indices):
                self.ga.population.individuals[idx] = migrants[i]

class ParallelGA(ABC):
    """Classe abstraite pour les algorithmes génétiques parallèles"""
    def __init__(
        self,
        ga_class: Callable,
        initial_population: Population,
        ga_config: Dict[str, Any],
        parallel_config: Dict[str, Any]
    ):
        self.ga_class = ga_class
        self.initial_population = initial_population
        self.ga_config = ga_config
        self.parallel_config = parallel_config
        
    @abstractmethod
    def run(self, generations: int) -> Chromosome:
        pass

class IslandModel(ParallelGA):
    """Modèle d'îles avec migration périodique"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.islands = []
        self._setup_islands()
        
    def _setup_islands(self):
        n_islands = self.parallel_config.get('n_islands', 4)
        migration_interval = self.parallel_config.get('migration_interval', 5)
        migration_size = self.parallel_config.get('migration_size', 2)
        
        # Division de la population initiale
        sub_pops = split_population(self.initial_population, n_islands)
        
        # Création des îles
        self.islands = [
            IslandActor.remote(
                self.ga_class,
                {**self.ga_config, 'population': sub_pop}
            )
            for sub_pop in sub_pops
        ]
    
    def run(self, generations: int) -> Chromosome:
        migration_interval = self.parallel_config.get('migration_interval', 5)
        
        for gen in range(generations):
            # Exécution parallèle des îles
            self.islands = [island.run_generation.remote() for island in self.islands]
            
            # Migration périodique
            if gen > 0 and gen % migration_interval == 0:
                self._migrate()
                
        return self._get_global_best()
    
    def _migrate(self):
        migration_topology = self.parallel_config.get('migration_topology', 'ring')
        migration_size = self.parallel_config.get('migration_size', 2)
        
        # Récupération des migrants
        all_migrants = ray.get([island.get_best.remote() for island in self.islands])
        
        # Distribution selon la topologie
        if migration_topology == 'ring':
            for i in range(len(self.islands)):
                next_island = (i + 1) % len(self.islands)
                migrants = all_migrants[i:i+migration_size]
                self.islands[next_island].receive_migrants.remote(migrants)
        elif migration_topology == 'complete':
            for i, island in enumerate(self.islands):
                migrants = [m for j, m in enumerate(all_migrants) if j != i]
                island.receive_migrants.remote(migrants[:migration_size])
    
    def _get_global_best(self) -> Chromosome:
        bests = ray.get([island.get_best.remote() for island in self.islands])
        return max(bests, key=lambda x: x.fitness)

class MasterSlaveModel(ParallelGA):
    """Modèle maître-esclave avec évaluation parallèle"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = GeneticAlgorithm(
            population=self.initial_population,
            **self.ga_config
        )
        
    def run(self, generations: int) -> Chromosome:
        for _ in range(generations):
            # Évaluation parallèle
            self._parallel_evaluation()
            
            # Opérations génétiques séquentielles
            self.master._evolve()
            
        return self.master.population.best()
    
    def _parallel_evaluation(self):
        # Évalue les chromosomes en parallèle
        population = self.master.population.individuals
        fitnesses = ray.get([_evaluate_chromosome.remote(chrom) for chrom in population])
        
        for chrom, fit in zip(population, fitnesses):
            chrom._fitness = fit

@ray.remote
def _evaluate_chromosome(chrom: Chromosome) -> float:
    return chrom.evaluate()

class CellularModel(ParallelGA):
    """Modèle cellulaire avec voisinage spatial"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = self._create_grid()
        
    def _create_grid(self):
        grid_size = self.parallel_config.get('grid_size', (10, 10))
        neighborhood_radius = self.parallel_config.get('neighborhood_radius', 1)
        
        # Création de la grille avec des acteurs
        grid = [
            [IslandActor.remote(self.ga_class, {
                **self.ga_config,
                'population': Population([random.choice(self.initial_population.individuals)])
            }) for _ in range(grid_size[1])]
            for _ in range(grid_size[0])
        ]
        return grid
    
    def run(self, generations: int) -> Chromosome:
        for _ in range(generations):
            # Mise à jour synchrone de toutes les cellules
            new_grid = []
            for i in range(len(self.grid)):
                new_row = []
                for j in range(len(self.grid[0])):
                    neighbors = self._get_neighbors(i, j)
                    migrant = ray.get(neighbors[0].get_best.remote())
                    self.grid[i][j].receive_migrants.remote([migrant])
                    new_pop = ray.get(self.grid[i][j].run_generation.remote())
                    new_row.append(self.grid[i][j])
                new_grid.append(new_row)
            self.grid = new_grid
            
        return self._get_global_best()
    
    def _get_neighbors(self, i: int, j: int) -> List[Any]:
        radius = self.parallel_config.get('neighborhood_radius', 1)
        neighbors = []
        rows, cols = len(self.grid), len(self.grid[0])
        
        for di in range(-radius, radius + 1):
            for dj in range(-radius, radius + 1):
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    neighbors.append(self.grid[ni][nj])
        return neighbors
    
    def _get_global_best(self) -> Chromosome:
        bests = []
        for row in self.grid:
            for cell in row:
                bests.append(ray.get(cell.get_best.remote()))
        return max(bests, key=lambda x: x.fitness)
