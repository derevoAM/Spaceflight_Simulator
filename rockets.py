class Entity:
    def __init__(self, surface, x, y, vx=0, vy=0, size=1):
        self.screen = surface
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.ax = 0
        self.ay = 0
        self.dt = 0
        # А вот дт можно взять из показателя фпс, он то не меняется

    def draw(self):
        pass

    def move(self):
        self.vx += self.ax * self.dt
        self.vy += self.ay * self.dt
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt


class Engine(Entity):
    def __init__(self, surface, x, y, power, consumption, vx=0, vy=0, size=1):
        Entity.__init__(self, surface, x, y)
        self.power = power
        self.consumption = consumption
        self.output = 100
        self.power_on = 0



class FuelTank(Entity):
    def __init__(self, surface, x, y, capacity, vx=0, vy=0, size=1):
        Entity.__init__(self, surface, x, y)
        self.capacity = capacity
        self.fullness = 100


class Cabin(Entity):
    def __init__(self, surface, x, y, vx=0, vy=0, size=1):
        Entity.__init__(self, surface, x, y)



class Conector(Entity):
    def __init__(self, surface, x, y, vx=0, vy=0, size=1):
        Entity.__init__(self, surface, x, y)
        self.double = 1
        self.left = 0

        
