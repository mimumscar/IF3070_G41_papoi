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

ETA_WEIGHT = 3

class State:
    def __init__(self, ship: Ship, vehicles: list) -> None:
        self.ship = ship
        self.vehicles = copy.deepcopy(vehicles) if vehicles else []

    def __repr__(self) -> str:
        inShip = [v for v in self.vehicles if v.x is not None]
        return "State(Total_In_Ship=%s, ShippingFee=%s, EtaPenalty=%s)" % (
            len(inShip), self.getShippingFee(), self.getEtaPenalty())

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

    @staticmethod
    def generateRandomState(ship, vehicles) -> 'State':
        import random
        state = State(ship, vehicles)
        
        vehicleIndices = list(range(len(state.vehicles)))
        random.shuffle(vehicleIndices)
        
        for idx in vehicleIndices:
            v = state.vehicles[idx]
            
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

    def getShippingFee(self) -> int:
        return sum([v.shippingFee for v in self.vehicles if v.x is not None and v.y is not None])

    def getEtaPenalty(self) -> int:
        placed = [v for v in self.vehicles if v.x is not None]
        penalty = 0
        for i in range(len(placed)):
            for j in range(i + 1, len(placed)):
                a, b = placed[i], placed[j]
                if (a.eta < b.eta and a.y > b.y) or (b.eta < a.eta and b.y > a.y):
                    penalty += 1
        return penalty

    def getFitness(self) -> int:
        return self.getShippingFee() - ETA_WEIGHT * self.getEtaPenalty()