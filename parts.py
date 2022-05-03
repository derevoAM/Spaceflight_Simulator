import pygame


class Entity:
    """
    Просто класс, объект которого будет статично отрисован на ракете
    """

    def __init__(self, surface, x=0, y=0, size=1, mass=0):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.texture = 0
        self.active = 0

    def draw(self):
        self.surface.blit(self.texture, dest=[self.x, self.y])


class Engine(Entity):
    def __init__(self, surface, power=0, consumption=0, x=0, y=0, mass=0):
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.power = power
        self.consumption = consumption
        self.output = 100
        self.power_on = 0
        self.type = "engine"
        self.texture = pygame.image.load('Textures/engines/big_engine_120x80.png')


class FuelTank(Entity):
    def __init__(self, surface, capacity = 0, x=0, y=0, mass=0):
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.capacity = capacity
        self.fullness = 100
        self.type = "fueltank"
        self.texture = pygame.image.load('Textures/tanks/tank_simple_100x50.png')


class Cabin(Entity):
    def __init__(self, surface, x=0, y=0, mass=0):
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.type = "cabin"
        self.texture = pygame.image.load('Textures/capsule/capsule_90x60.png')


class Conector(Entity):
    def __init__(self, surface):
        Entity.__init__(self, surface)
        self.double = 1
        self.left = 0


'''screen = pygame.display.set_mode((900, 900))
engine = Engine(screen, 100 , 100, x=200, y=100)
engine.draw()
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()'''
