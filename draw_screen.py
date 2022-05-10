import trajectory_calculation as tr

import pygame

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]
EARTH = [31, 67, 242]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]


class View:
    """
    Class of different views
    """
    def __init__(self, width, height, x, y, rocket):
        self.width = int(width)
        self.height = int(height)
        self.x = x
        self.y = y
        self.surface = pygame.Surface((self.width, self.height))
        self.color = WHITE
        self.rocket = rocket

    def draw(self):
        pass


class RocketView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height, width / 2, 0, rocket)
        self.color = SKY

    def draw(self):
        self.surface.fill(SKY)
        self.rocket.recount()
        self.rocket.draw()
        self.surface.blit(self.rocket.get_surface(), (0, 0))


class ParametersView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height / 2, 0, 0, rocket)

    def draw(self):
        self.surface.fill(GREY)


class SpaceView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height, 0, height / 2, rocket)

    def draw(self):
        self.surface.fill(GREEN)
