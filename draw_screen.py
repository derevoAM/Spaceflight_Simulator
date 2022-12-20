import pygame

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]
EARTH = [31, 67, 242]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]


def blit_rotate(surf, image, pos, origin_pos, angle):
    """
    In the following example program, the function blitRotate(surf, image, pos, originPos, angle) does all
    the above steps and "blit" a rotated image to a surface.
    :param surf is the target Surface
    :param image is the Surface which has to be rotated and blit
    :param pos is the position of the pivot on the target Surface surf (relative to the top left of surf)
    :param origin_pos is position of the pivot on the image Surface (relative to the top left of image)
    :param angle is the angle of rotation in degrees
    The 2nd argument (pos) of blitRotate is the position of the pivot point in the window and the
    3rd argument (originPos) is the position of the pivot point on the rotating Surface:
    """
    image_rect = image.get_rect(topleft=(pos[0] - origin_pos[0], pos[1] - origin_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


class View:
    """
    Class of different views
    """

    def __init__(self, width, height, x, y, rocket):
        """
        Initializing the view
        :param width: width of a surface
        :param height: height of a surface
        :param x: x coordinate of top left corner of surface on main screen
        :param y: y coordinate of top left corner of surface on main screen
        :param rocket: object of class Rocket from sandbox
        """
        self.width = int(width)
        self.height = int(height)
        self.x = x
        self.y = y
        self.surface = pygame.Surface((self.width, self.height))
        self.rocket = rocket
        self.engine = None

    def draw(self):
        """
        Drawing the view(all the images and texts on surface)
        """
        pass

    def set_engine(self, engine):
        """
        Setting the engine to get its parameters
        :param engine: object of class PhysicsEngine from trajectory_calculation
        """
        self.engine = engine


class RocketView(View):
    """
    Class of a view with a rocket
    """

    def __init__(self, width, height, rocket):
        """
        Initializing RocketView
        :param width: width of a surface
        :param height: height of a surface
        :param rocket: object of class Rocket from sandbox
        """
        View.__init__(self, width / 2, 2 * height / 3, 0, height / 3, rocket)

    def draw(self):
        """
        Drawing rocket on a RocketView surface according to its direction
        """
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(pygame.image.load("textures/View_background/stars.jpg"), (0, 0))
        if self.engine.rocket_parameters.fuel_remained <= 0:
            self.rocket.draw(0)
        else:
            self.rocket.draw(self.engine.rocket_parameters.engine_power)
        h = 0
        for part in self.rocket.parts:
            h += (part.texture.get_size()[1] / 1.5)
        self.rocket.surface = pygame.transform.scale(self.rocket.surface, (100 / 1.2, 800 / 1.5))
        blit_rotate(self.surface, self.rocket.surface,
                    (self.width / 2, self.height / 2),
                    (self.rocket.parts[0].texture.get_size()[0] / (2 * 1.2), h / 2), self.rocket.angle)


class ParametersView(View):
    """
    Class of a view with rocket parameters
    """

    def __init__(self, width, height, rocket):
        """
        Initializing ParametersView
        :param width: width of a surface
        :param height: height of a surface
        :param rocket: object of class Rocket from sandbox
        """
        View.__init__(self, width / 2, height / 3, 0, 0, rocket)
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)
        self.rocket_param = None
        self.time = None
        self.speed = None
        self.height = None
        self.fuel = None
        self.power = None

    def define_text(self):
        """
        Defining rocket parameters at a particular moment
        """
        x = self.engine.rocket_parameters.parameters[0]
        y = self.engine.rocket_parameters.parameters[1]
        vx = self.engine.rocket_parameters.parameters[2]
        vy = self.engine.rocket_parameters.parameters[3]
        self.rocket_param = self.font_big.render("Rocket parameters", True, [0., 0, 0])
        self.time = self.font.render(f"Time = {self.engine.rocket_parameters.current_time:.1f} c", True, [0, 0, 0])
        self.speed = self.font.render(f"Speed = {((vx ** 2 + vy ** 2) ** 0.5):.2f} м/c", True, [0, 0, 0])
        self.height = self.font.render(
            f"Height = {((x ** 2 + y ** 2) ** 0.5 - self.engine.constants.rad_Earth) / 1000:.2f} км",
            True,
            [0, 0, 0])
        self.fuel = self.font.render("Fuel", True, [0, 0, 0])
        self.power = self.font.render("Power", True, [0, 0, 0])

    def blit_text(self):
        """
        Adding texts to the surface
        """
        self.surface.blit(self.rocket_param, (self.width / 2 - 150, 10))
        self.surface.blit(self.time, (self.width / 2 - 100, 80))
        self.surface.blit(self.height, (self.width / 2 - 100, 120))
        self.surface.blit(self.speed, (self.width / 2 - 100, 160))
        self.surface.blit(self.fuel, (self.width / 2 - 100, 200))
        self.surface.blit(self.power, (self.width / 2 - 100, 240))

    def draw_rect(self):
        """
        Drawing rectangles, which show how much fuel is left and current power of a rocket
        """
        pygame.draw.rect(self.surface, BLACK, [self.width / 2 - 20, 190, 300, 40], width=1)
        pygame.draw.rect(self.surface, GREEN, [
            self.width / 2 - 19, 191,
            298 * self.engine.rocket_parameters.fuel_remained / self.rocket.get_active_parameters()[4],
            38])

        pygame.draw.rect(self.surface, BLACK, [self.width / 2 - 10, 240, 300, 40], width=1)
        pygame.draw.rect(self.surface, RED, [
            self.width / 2 - 9, 241,
            298 * self.engine.rocket_parameters.engine_power / 100,
            38])

    def draw(self):
        """
        Drawing rocket on a RocketView surface according to its direction
        """
        self.surface.fill(GREY)
        self.define_text()
        self.blit_text()
        self.draw_rect()


class SpaceView(View):
    """
    Class of a view with a planet and rocket position on the map
    """

    def __init__(self, width, height, rocket):
        """
        Initializing SpaceView
        :param width: width of a surface
        :param height: height of a surface
        :param rocket: object of class Rocket from sandbox
        """
        View.__init__(self, width / 2, height, width / 2, 0, rocket)
        self.scale = 0

    def draw_planet(self):
        """
        Drawing a planet
        """
        pygame.draw.circle(self.surface, EARTH, (self.width / 2, self.height / 2), self.height / 6)

    def draw_trajectory(self):
        """
        Drawing predicative orbit
        """
        for current in self.engine.rocket_parameters.predictive_orbit:
            pygame.draw.circle(self.surface, WHITE,
                               (self.scale * current[0] + self.width / 2, -self.scale * current[1] + self.height / 2),
                               1)

    def draw(self):
        """
        Drawing planet and predicative orbit
        """
        self.surface.fill(BLACK)
        self.scale = self.height / (6 * self.engine.constants.rad_Earth)
        x = self.engine.rocket_parameters.parameters[0]
        y = self.engine.rocket_parameters.parameters[1]
        self.draw_planet()
        pygame.draw.circle(self.surface, GREEN, (self.scale * x + self.width / 2, -self.scale * y + self.height / 2), 4)
        self.draw_trajectory()
