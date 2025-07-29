from typing import Callable, List, Dict, Optional, Tuple
from ..common.solution import Solution
from ..common.neighborhood import NeighborhoodGenerator
import numpy as np
import random
from collections import defaultdict


class TabuSearch:
    def __init__(
        self,
        initial_solution: Solution,
        neighborhood_generator: NeighborhoodGenerator,
        get_move_hash: Callable[[Solution], int],
        tabu_tenure: int = 10,
        aspiration_criteria: Optional[List[Callable[[Solution], bool]]] = None,
        update_history: Optional[Callable[[Solution, Dict], Dict]] = None,
        apply_intensification: Optional[Callable[[Solution, List], Solution]] = None,
        update_intensification_memory: Optional[Callable[[Solution, List], List]] = None,
        apply_diversification: Optional[Callable[[Solution, List], Solution]] = None,
        update_diversification_memory: Optional[Callable[[Solution, List], List]] = None,
        max_iterations: int = 100,
        diversification_necessity: int = 5,
        diversification_frequency: int = 20,
        intensification_threshold: int = 20,
        patience: int = 15
    ):
        self.current_solution = initial_solution
        self.best_solution = initial_solution.copy()
        self.neighborhood = neighborhood_generator
        self.tabu_list = []
        self.tabu_tenure = tabu_tenure
        self.aspiration_criteria = aspiration_criteria or []
        self._apply_diversification = apply_diversification
        self._apply_intensification = apply_intensification
        self._update_diversification_memory = update_diversification_memory
        self.diversification_memory = update_diversification_memory(initial_solution, []) if update_diversification_memory else []
        self._update_intensification_memory = update_intensification_memory
        self.intensification_memory = update_intensification_memory(initial_solution, []) if update_intensification_memory else []
        self._get_move_hash = get_move_hash
        self.max_iterations = max_iterations
        self.iterations = 0
        self.best_iteration = 0
        self._frequency: Dict[int, int] = defaultdict(int)  # Suivi des solutions visitées
        self._update_history = update_history
        self.history = {}
        self.diversification_necessity = diversification_necessity
        self.diversification_frequency = diversification_frequency
        self.intensification_threshold = intensification_threshold
        self.patience = patience
        self.no_improvement_count = 0
        
    def run(self) -> Solution:
        while not self._should_stop():
            neighbors = self._generate_neighbors()
            best_candidate = self._select_best_candidate(neighbors)
            
            if best_candidate:
                self._update_current_solution(best_candidate)
                self._update_best_solution(best_candidate)
                self._update_tabu_list(best_candidate)
                if self._update_history is not None:
                    self.history = self._update_history(best_candidate, self.history)

            self.iterations += 1
            if self.no_improvement_count == self.diversification_necessity or self.iterations % self.diversification_frequency == 0:
                if self._apply_diversification:
                    self._update_current_solution(self._apply_diversification(self.current_solution, self.diversification_memory))
                    self.diversification_memory = self._update_diversification_memory(self.current_solution, self.diversification_memory)
            elif self.no_improvement_count == self.intensification_threshold:
                if self._apply_intensification:
                    self._update_current_solution(self._apply_intensification(self.current_solution, self.intensification_memory))
                    self.intensification_memory = self._update_intensification_memory(self.current_solution, self.intensification_memory)
        return self.best_solution

    def _generate_neighbors(self) -> List[Solution]:
        """Génère les voisins avec stratégie d'intensification si activée."""
        neighbors = self.neighborhood.generate(self.current_solution)
            
        if not neighbors:  # Si intensification a filtré tous les voisins
            neighbors = self.neighborhood.generate(self.current_solution)
            
        return neighbors

    def _should_stop(self) -> bool:
        """Détermine si la recherche doit s'arrêter."""
        # Critère d'arrêt principal
        if self.iterations >= self.max_iterations:
            return True
            
        # Critère de stagnation
        if self.iterations - self.best_iteration > self.patience:
            return True
            
        return False
    
    def _update_tabu_list(self, best_candidate: Solution):
        """Met à jour la liste tabou avec une solution ou un attribut."""
        candidate_hash = self._get_move_hash(best_candidate)
        
        if len(self.tabu_list) >= self.tabu_tenure:
            self.tabu_list.pop(0)
            
        self.tabu_list.append(candidate_hash)
    
    def _select_best_candidate(self, neighbors: List[Solution]) -> Optional[Solution]:
        """Sélectionne le meilleur candidat selon les critères tabou."""
        if not neighbors:
            return None
            
        # Évalue tous les voisins
        evaluated_neighbors = [(n, n.evaluate()) for n in neighbors]
        
        # Trie du meilleur (score le plus élevé) au pire
        sorted_neighbors = sorted(evaluated_neighbors, key=lambda x: x[1], reverse=True)
        
        # Cherche le premier candidat non tabou ou qui satisfait les critères d'aspiration
        for candidate, score in sorted_neighbors:
            move_hash = self._get_move_hash(candidate)
            is_tabu = move_hash in self.tabu_list
            is_aspired = any(crit(candidate) for crit in self.aspiration_criteria)
            
            # Critère d'aspiration: permet de surpasser tabou si solution est meilleure que la meilleure globale
            is_best_aspired = score > self.best_solution.evaluate()
            
            if (not is_tabu) or is_aspired or is_best_aspired:
                if score > self.current_solution.evaluate():
                    return candidate
                    
        # Si tous sont tabous et aucun ne satisfait les critères, retourne None
        return None
            
    def _update_frequency(self, best_candidate: Solution):
        """Met à jour la fréquence des solutions visitées."""
        self._frequency[hash(best_candidate)] += 1
        
    def _update_best_solution(self, candidate: Solution):
        """Met à jour la meilleure solution globale."""
        if candidate.evaluate() > self.best_solution.evaluate():
            self.best_solution = candidate.copy()
            self.best_iteration = self.iterations
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1
            
    def _update_current_solution(self, candidate: Solution):
        """Met à jour la solution courante."""
        if self._update_intensification_memory:
            self.intensification_memory = self._update_intensification_memory(candidate, self.intensification_memory)
        if self._update_diversification_memory:
            self.diversification_memory = self._update_diversification_memory(candidate, self.diversification_memory)
        self.current_solution = candidate.copy()