'''
ref:
- PPT Beyond Classical Search IF3070 (Genetic Algorithm)
- https://github.com/aimacode/aima-python/blob/master/aima/search.py
'''

import random
import time

from base import Ship, State

GA_CONFIGS = [
    {'populationSize': 20, 'generations': 100},
    {'populationSize': 50, 'generations': 100},
    {'populationSize': 100, 'generations': 100},
    {'populationSize': 100, 'generations': 10},
    {'populationSize': 100, 'generations': 30},
    {'populationSize': 100, 'generations': 80},
]

class GeneticAlgorithm:
    def __init__(self, ship, vehicles, populationSize = 50, generations = 100, mutationRate = 0.1):
        self.ship = ship
        self.vehicles = vehicles
        self.populationSize = populationSize
        self.generations = generations
        self.mutationRate = mutationRate
        
        self.initialState = None
        self.maxHistory = []
        self.meanHistory = []
        self.iterations = 0
        self.duration = 0

    def repair(self, state):
        positions = [(v.x, v.y) for v in state.vehicles]
        for v in state.vehicles:
            v.x = None
            v.y = None
        for v, (x, y) in zip(state.vehicles, positions):
            if x is not None:
                v.x = x
                v.y = y
                if not state.isValid():
                    v.x = None
                    v.y = None
        return state

    def select(self, population, fitnesses):
        low = min(fitnesses)
        weights = [f - low + 1 for f in fitnesses]
        return random.choices(population, weights=weights, k=2)

    def recombine(self, x, y):
        n = len(x.vehicles)
        point = random.randint(1, n-1)
        child = State(self.ship, x.vehicles[:point] + y.vehicles[point:])
        return self.repair(child)

    def mutate(self, state):
        if random.random() > self.mutationRate:
            return state

        n = len(state.vehicles)
        action = random.choice(["swap", "move", "rotate"])
        if action == "swap":
            a, b = random.sample(range(n), 2)
            state.swapVehiclePositions(a, b)
        else:
            i = random.randrange(n)
            if action == "rotate":
                state.rotateVehicle(i)
            else:
                w, l = state.vehicles[i].getCurrentDimensions()
                if w > self.ship.width or l > self.ship.length:
                    state.removeVehicle(i)
                else:
                    state.moveVehicle(i, random.randint(0, self.ship.width - w), random.randint(0, self.ship.length - l))
        return self.repair(state)

    def runGeneticAlgorithm(self):
        startTime = time.perf_counter()
        population = [State.generateRandomState(self.ship, self.vehicles) for _ in range(self.populationSize)]
        fitnesses = [s.getFitness() for s in population]
        best = population[fitnesses.index(max(fitnesses))]
        
        self.initialState = best.clone()
        self.maxHistory = [max(fitnesses)]
        self.meanHistory = [sum(fitnesses) / len(fitnesses)]

        for _ in range(self.generations):
            best = population[fitnesses.index(max(fitnesses))]
            nextPopulation = [best.clone()]
            while len(nextPopulation) < self.populationSize:
                x, y = self.select(population, fitnesses)
                child = self.recombine(x, y)
                nextPopulation.append(self.mutate(child))

            population = nextPopulation
            fitnesses = [s.getFitness() for s in population]
            self.maxHistory.append(max(fitnesses))
            self.meanHistory.append(sum(fitnesses) / len(fitnesses))

        self.iterations = self.generations
        self.duration = time.perf_counter() - startTime
        return population[fitnesses.index(max(fitnesses))]