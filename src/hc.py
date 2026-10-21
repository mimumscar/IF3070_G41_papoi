'''
ref:
- PPT Beyond Classical Search IF3070
- https://github.com/aimacode/aima-python/blob/master/search.py, dari line 941-956
'''

import time
from base import State

class HillClimbing:
    def __init__(self, ship, vehicles):
        self.ship = ship
        self.vehicles = vehicles
        self.initialState = None
        self.history = []
        self.iterations = 0
        self.duration = 0

    def getNeighbors(self, current):
        neighbors = []
        for move in current.getMoves():
            s = current.applyMove(move)
            if s.isValid():
                neighbors.append(s)
        return neighbors

    def runSteepestAscent(self):
        mulai = time.perf_counter()
        current = State.generateRandomState(self.ship, self.vehicles)
        self.initialState = current.clone()
        self.history = [current.getFitness()]

        while True:
            tetangga = self.getNeighbors(current)
            if len(tetangga) == 0:
                break
            best = max(tetangga, key=lambda s: s.getFitness())
            if best.getFitness() <= current.getFitness():
                break
            current = best
            self.history.append(current.getFitness())

        self.iterations = len(self.history) - 1
        self.duration = time.perf_counter() - mulai
        return current