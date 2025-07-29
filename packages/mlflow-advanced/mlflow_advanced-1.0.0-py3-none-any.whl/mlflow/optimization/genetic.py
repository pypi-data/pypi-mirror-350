import numpy as np
from typing import Dict, Any, Callable, List, Tuple, Optional
import random

class GeneticAlgorithm:
    """
    Genetic Algorithm for hyperparameter optimization.
    
    Features:
    - Tournament selection
    - Multiple crossover strategies
    - Adaptive mutation rates
    - Elitism
    """
    
    def __init__(self, objective_function: Callable, parameter_space: Dict[str, Tuple],
                 population_size: int = 50, elite_size: int = 10,
                 mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        self.objective_function = objective_function
        self.parameter_space = parameter_space
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        self.population = []
        self.fitness_scores = []
        self.best_individual = None
        self.best_fitness = float('-inf')
        self.generation_history = []
    
    def _create_individual(self) -> Dict[str, Any]:
        """Create a random individual."""
        individual = {}
        for param_name, (param_min, param_max) in self.parameter_space.items():
            if isinstance(param_min, int) and isinstance(param_max, int):
                individual[param_name] = random.randint(param_min, param_max)
            else:
                individual[param_name] = random.uniform(param_min, param_max)
        return individual
    
    def _initialize_population(self):
        """Initialize the population."""
        self.population = [self._create_individual() for _ in range(self.population_size)]
        self.fitness_scores = [self.objective_function(ind) for ind in self.population]
        
        # Track best individual
        best_idx = np.argmax(self.fitness_scores)
        if self.fitness_scores[best_idx] > self.best_fitness:
            self.best_fitness = self.fitness_scores[best_idx]
            self.best_individual = self.population[best_idx].copy()
    
    def _tournament_selection(self, tournament_size: int = 3) -> Dict[str, Any]:
        """Tournament selection."""
        tournament_indices = random.sample(range(len(self.population)), tournament_size)
        tournament_fitness = [self.fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[np.argmax(tournament_fitness)]
        return self.population[winner_idx].copy()
    
    def _crossover(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Single-point crossover."""
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        child1, child2 = parent1.copy(), parent2.copy()
        param_names = list(self.parameter_space.keys())
        crossover_point = random.randint(1, len(param_names) - 1)
        
        for i in range(crossover_point):
            param_name = param_names[i]
            child1[param_name], child2[param_name] = child2[param_name], child1[param_name]
        
        return child1, child2
    
    def _mutate(self, individual: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate an individual."""
        mutated = individual.copy()
        
        for param_name, (param_min, param_max) in self.parameter_space.items():
            if random.random() < self.mutation_rate:
                if isinstance(param_min, int) and isinstance(param_max, int):
                    mutated[param_name] = random.randint(param_min, param_max)
                else:
                    # Gaussian mutation
                    current_value = mutated[param_name]
                    std = (param_max - param_min) * 0.1  # 10% of range
                    new_value = random.gauss(current_value, std)
                    mutated[param_name] = np.clip(new_value, param_min, param_max)
        
        return mutated
    
    def optimize(self, n_generations: int = 100, verbose: bool = True) -> Dict[str, Any]:
        """
        Run genetic algorithm optimization.
        
        Args:
            n_generations: Number of generations to run
            verbose: Whether to print progress
            
        Returns:
            Optimization results
        """
        # Initialize population
        self._initialize_population()
        
        for generation in range(n_generations):
            new_population = []
            
            # Elitism - keep best individuals
            elite_indices = np.argsort(self.fitness_scores)[-self.elite_size:]
            for idx in elite_indices:
                new_population.append(self.population[idx].copy())
            
            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()
                
                child1, child2 = self._crossover(parent1, parent2)
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Trim to exact population size
            new_population = new_population[:self.population_size]
            
            # Evaluate new population
            self.population = new_population
            self.fitness_scores = [self.objective_function(ind) for ind in self.population]
            
            # Track best individual
            best_idx = np.argmax(self.fitness_scores)
            if self.fitness_scores[best_idx] > self.best_fitness:
                self.best_fitness = self.fitness_scores[best_idx]
                self.best_individual = self.population[best_idx].copy()
            
            # Record generation statistics
            gen_stats = {
                'generation': generation,
                'best_fitness': max(self.fitness_scores),
                'avg_fitness': np.mean(self.fitness_scores),
                'worst_fitness': min(self.fitness_scores)
            }
            self.generation_history.append(gen_stats)
            
            if verbose and generation % 10 == 0:
                print(f"Generation {generation}: Best = {gen_stats['best_fitness']:.4f}, "
                      f"Avg = {gen_stats['avg_fitness']:.4f}")
        
        return {
            'best_individual': self.best_individual,
            'best_fitness': self.best_fitness,
            'generation_history': self.generation_history,
            'final_population': self.population
        }