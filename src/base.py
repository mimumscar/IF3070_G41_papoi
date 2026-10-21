import copy
import random

# ref: https://github.com/hellerbarde/BinPack/blob/master/binpack/item.py

class Vehicle:
    def __init__(self, id, width, length, shippingFee, weight, eta):
        self.id = id
        self.width = width
        self.length = length
        self.orientation = 'Horizontal' 
        self.shippingFee = shippingFee
        self.weight = weight
        self.eta = eta
        
        self.x = None
        self.y = None

    def rotate(self):
        if self.orientation == 'Horizontal':
            self.orientation = 'Vertical'
        else:
            self.orientation = 'Horizontal'

    def getCurrentDimensions(self):
        if self.orientation == 'Horizontal':
            return self.width, self.length
        return self.length, self.width


class Ship:
    def __init__(self, width, length, maxCapacity):
        self.width = width
        self.length = length
        self.maxCapacity = maxCapacity


class State:
    def __init__(self, ship, vehicles):
        self.ship = ship
        self.vehicles = copy.deepcopy(vehicles) if vehicles else []

    def clone(self):
        return State(self.ship, self.vehicles)

    def swapVehiclePositions(self, a, b):
        va = self.vehicles[a]
        vb = self.vehicles[b]
        va.x, vb.x = vb.x, va.x
        va.y, vb.y = vb.y, va.y

    def moveVehicle(self, i, x, y):
        self.vehicles[i].x = x
        self.vehicles[i].y = y

    def removeVehicle(self, i):
        self.vehicles[i].x = None
        self.vehicles[i].y = None

    def rotateVehicle(self, i):
        self.vehicles[i].rotate()

    def getMoves(self):
        moves = []
        for i, v in enumerate(self.vehicles):
            for x in range(self.ship.width):
                for y in range(self.ship.length):
                    if (v.x, v.y) != (x, y):
                        moves.append(("move", i, x, y))
            if v.x is not None:
                moves.append(("remove", i))
                moves.append(("rotate", i))
            for j in range(i + 1, len(self.vehicles)):
                if v.x is not None or self.vehicles[j].x is not None:
                    moves.append(("swap", i, j))
        return moves

    def applyMove(self, move):
        s = self.clone()
        if move[0] == "move":
            s.moveVehicle(move[1], move[2], move[3])
        elif move[0] == "remove":
            s.removeVehicle(move[1])
        elif move[0] == "rotate":
            s.rotateVehicle(move[1])
        else:
            s.swapVehiclePositions(move[1], move[2])
        return s

    def isValid(self):
        grid = [[False] * self.ship.length for _ in range(self.ship.width)]
        berat = 0
        for v in self.vehicles:
            if v.x is None or v.y is None:
                continue
            berat += v.weight
            w, l = v.getCurrentDimensions()
            if berat > self.ship.maxCapacity:
                return False
            if v.x < 0 or v.y < 0 or v.x + w > self.ship.width or v.y + l > self.ship.length:
                return False
            for i in range(v.x, v.x + w):
                for j in range(v.y, v.y + l):
                    if grid[i][j]:
                        return False
                    grid[i][j] = True
        return True

    @staticmethod
    def generateRandomState(ship, vehicles):
        state = State(ship, vehicles)
        urutan = list(range(len(state.vehicles)))
        random.shuffle(urutan)
        for i in urutan:
            v = state.vehicles[i]
            for _ in range(20):
                v.orientation = random.choice(['Horizontal', 'Vertical'])
                w, l = v.getCurrentDimensions()
                if ship.width >= w and ship.length >= l:
                    v.x = random.randint(0, ship.width - w)
                    v.y = random.randint(0, ship.length - l)
                    if state.isValid():
                        break
                v.x = None
                v.y = None
        return state

    def getShippingFee(self):
        return sum(v.shippingFee for v in self.vehicles if v.x is not None)

    def getEtaPenalty(self):
        placed = [v for v in self.vehicles if v.x is not None]
        penalty = 0
        for i in range(len(placed)):
            for j in range(i + 1, len(placed)):
                a, b = placed[i], placed[j]
                if (a.eta < b.eta and a.y > b.y) or (b.eta < a.eta and b.y > a.y):
                    penalty += 1
        return penalty

    def getFitness(self):
        return self.getShippingFee() - 3 * self.getEtaPenalty()