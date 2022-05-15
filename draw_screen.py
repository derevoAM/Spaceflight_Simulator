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

    def draw(self, engine):
        """
        Drawing parameters view
        :param engine: object of class PhysicsEngine from trajectory_calculation
        :return:
        """
        pass


class RocketView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height, width / 2, 0, rocket)
        self.color = SKY

    def draw(self, engine):
        self.surface.fill(SKY)
        self.rocket.recount()
        self.rocket.draw()
        self.surface.blit(self.rocket.get_surface(), (0, 0))


class ParametersView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height / 2, 0, 0, rocket)
        self.font = pygame.font.Font(None, 40)

    def draw(self, engine):

        self.surface.fill(GREY)
        x = engine.rocket_parameters.parameters[0]
        y = engine.rocket_parameters.parameters[1]
        vx = engine.rocket_parameters.parameters[2]
        vy = engine.rocket_parameters.parameters[3]
        speed = self.font.render(f"Speed = {((vx ** 2 + vy ** 2) ** 0.5):.2f} м/c", True, [0, 0, 0])
        height = self.font.render(f"Height = {((x ** 2 + y ** 2) ** 0.5 - engine.constants.rad_Earth) / 1000:.2f} км", True,
                             [0, 0, 0])
        self.surface.blit(speed, (self.width / 2 - 100, 100))
        self.surface.blit(height, (self.width / 2 - 100, 60))


class SpaceView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height / 2, 0, height / 2, rocket)

    def draw(self, engine):
        self.surface.fill(BLACK)
        scale = self.height / (4 * engine.constants.rad_Earth)
        x = engine.rocket_parameters.parameters[0]
        y = engine.rocket_parameters.parameters[1]
        pygame.draw.circle(self.surface, EARTH, (self.width / 2, self.height / 2), self.height / 4)
        pygame.draw.circle(self.surface, WHITE, (scale * x + self.width / 2, -scale * y + self.height / 2), 10)
