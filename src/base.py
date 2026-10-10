import copy

# ref: https://github.com/hellerbarde/BinPack/blob/master/binpack/item.py
class Vehicle:
    def __init__(self, vId: str, width: int, length: int, shippingFee: int, weight: int, eta: int) -> None:
        self.id = vId
        self.width = width
        self.length = length
        self.orientation = 'Horizontal' 
        self.shippingFee = shippingFee
        self.weight = weight
        self.eta = eta
        
        self.x = None
        self.y = None

    def __repr__(self) -> str:
        return 'Vehicle(id=%r, orient=%r, x=%r, y=%r)' % (self.id, self.orientation, self.x, self.y)

    def rotate(self) -> None:
        self.orientation = 'Vertical' if self.orientation == 'Horizontal' else 'Horizontal'

    def getCurrentDimensions(self) -> tuple:
        if self.orientation == 'Horizontal':
            return self.width, self.length
        return self.length, self.width

    def __lt__(self, other: 'Vehicle') -> bool:
        return self.shippingFee < other.shippingFee


class Ship:
    def __init__(self, width: int, length: int, maxCapacity: int) -> None:
        self.width = width
        self.length = length
        self.maxCapacity = maxCapacity


class State:
    def __init__(self, ship: Ship, vehicles: list) -> None:
        self.ship = ship
        self.vehicles = copy.deepcopy(vehicles) if vehicles else []

    def __repr__(self) -> str:
        inShip = [v for v in self.vehicles if v.x is not None]
        return "State(Total_In_Ship=%s, Objective_Score=%s)" % (len(inShip), self.getObjectiveScore())

    def isValid(self) -> bool:
        totalWeight = 0
        grid = [[False for _ in range(self.ship.length)] for _ in range(self.ship.width)]

        for v in self.vehicles:
            if v.x is None or v.y is None:
                continue

            totalWeight += v.weight
            if totalWeight > self.ship.maxCapacity:
                return False

            w, l = v.getCurrentDimensions()

            if v.x < 0 or v.y < 0 or v.x + w > self.ship.width or v.y + l > self.ship.length:
                return False

            for i in range(v.x, v.x + w):
                for j in range(v.y, v.y + l):
                    if grid[i][j]:
                        return False
                    grid[i][j] = True

        return True

    def getObjectiveScore(self) -> int:
        return sum([v.shippingFee for v in self.vehicles if v.x is not None and v.y is not None])

    def getUrgencyScore(self) -> int:
        maxEta = 67
        return sum([(maxEta - v.eta) for v in self.vehicles if v.x is not None and v.y is not None])