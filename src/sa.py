import math
import random
import time
from base import State

#referensi
# - https://github.com/aimacode/aima-python/blob/master/aima/search.py

class SimulatedAnnealing:
    def __init__(self, ship, vehicles, iterations=500, temperature=100.0, cooling=0.99):
        self.initialState = State.generateRandomState(ship, vehicles)
        self.iterations = iterations
        self.temperature = temperature
        self.cooling = cooling
        self.history = []           
        self.current_history = []   
        self.acceptance_history = []  
        self.stuck_count = 0           
        self.duration = 0

    def randomNeighbor(self, state):
        groups = {}
        for move in state.getMoves():
            groups.setdefault(move[0], []).append(move)
        if len(groups) == 0:
            return state.clone()
        for _ in range(500):
            kind = random.choice(list(groups))
            s = state.applyMove(random.choice(groups[kind]))
            if s.isValid():
                return s
        return state.clone()

    def run(self):
        mulai = time.perf_counter()
        current = self.initialState.clone()
        best = current.clone()
        T = self.temperature
        self.history = [best.getFitness()]
        self.current_history = [current.getFitness()]
        self.acceptance_history = []
        self.stuck_count = 0
        same_score = 0

        for i in range(self.iterations):
            candidate = self.randomNeighbor(current)
            delta = candidate.getFitness() - current.getFitness()
            prob = 1.0 if delta >= 0 else math.exp(delta / T)

            if random.random() < prob:
                current = candidate

            if current.getFitness() > best.getFitness():
                best = current.clone()
                same_score = 0
            else:
                same_score += 1
                if same_score == 10:
                    self.stuck_count += 1

            self.history.append(best.getFitness())
            self.current_history.append(current.getFitness())
            self.acceptance_history.append(prob)
            T = T * self.cooling

        self.duration = time.perf_counter() - mulai
        return best