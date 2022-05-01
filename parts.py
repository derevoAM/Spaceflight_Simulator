import pygame


class Entity:
    """
    Просто класс, объект которого будет статично отрисован на ракете
    """

    def __init__(self, surface, x=0, y=0, size=1):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.texture = 0

    def draw(self):
        self.surface.blit(self.texture, dest=[self.x, self.y])


class Engine(Entity):
    def __init__(self, surface, power = 0, consumption = 0, x=0, y=0):
        Entity.__init__(self, surface, x=x, y=y)
        self.power = power
        self.consumption = consumption
        self.output = 100
        self.power_on = 0
        self.texture = pygame.image.load('textures/engines/big_engine_120x80.png')


class FuelTank(Entity):
    def __init__(self, surface, capacity, x=0, y=0):
        Entity.__init__(self, surface, x=x, y=y)
        self.capacity = capacity
        self.fullness = 100
        self.texture = pygame.image.load('textures/tanks/new/tank_simple_90x60.png')


class Cabin(Entity):
    def __init__(self, surface, x=0, y=0):
        Entity.__init__(self, surface, x=x, y=y)
        self.texture = pygame.image.load('textures/capsule/capsule_90x60.png')


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