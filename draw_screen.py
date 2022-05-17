import pygame

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]
EARTH = [31, 67, 242]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]

def blit_rotate(surf, image, pos, originPos, angle):
    """
    In the following example program, the function blitRotate(surf, image, pos, originPos, angle) does all
    the above steps and "blit" a rotated image to a surface.
    :param surf is the target Surface
    :param image is the Surface which has to be rotated and blit
    :param pos is the position of the pivot on the target Surface surf (relative to the top left of surf)
    :param originPos is position of the pivot on the image Surface (relative to the top left of image)
    :param angle is the angle of rotation in degrees
This means, the 2nd argument (pos) of blitRotate is the position of the pivot point in the window and the
 3rd argument (originPos) is the position of the pivot point on the rotating Surface:
    """
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # rotated image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)


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
        View.__init__(self, width / 2, 2 * height / 3, 0, height / 3, rocket)
        self.color = SKY

    def draw(self, engine):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(pygame.image.load("Textures/View_background/stars.jpg"), (0, 0))
        self.rocket.recount()
        pygame.draw.line(self.surface, BLACK, (self.width / 2, 0), (self.width / 2, self.height))
        h = 0
        for part in self.rocket.parts:
            h += part.texture.get_size()[1]
        h /= 1.5
        self.rocket.surface = pygame.transform.scale(self.rocket.surface, (100 / 1.2, 800 / 1.5))
        blit_rotate(self.surface, self.rocket.surface,
                    (self.width / 2, self.height / 2),
                    (self.rocket.parts[0].texture.get_size()[0] / (2 * 1.2), h / 2), self.rocket.angle)


class ParametersView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height / 3, 0, 0, rocket)
        self.font = pygame.font.Font(None, 40)
        self.font_big = pygame.font.Font(None, 60)

    def draw(self, engine):
        self.surface.fill(GREY)
        x = engine.rocket_parameters.parameters[0]
        y = engine.rocket_parameters.parameters[1]
        vx = engine.rocket_parameters.parameters[2]
        vy = engine.rocket_parameters.parameters[3]
        rocket_param = self.font_big.render("Rocket parameters", True, [0., 0, 0])
        time = self.font.render(f"Time = {engine.rocket_parameters.current_time:.1f} c", True, [0, 0, 0])
        speed = self.font.render(f"Speed = {((vx ** 2 + vy ** 2) ** 0.5):.2f} м/c", True, [0, 0, 0])
        height = self.font.render(f"Height = {((x ** 2 + y ** 2) ** 0.5 - engine.constants.rad_Earth) / 1000:.2f} км",
                                  True,
                                  [0, 0, 0])
        fuel = self.font.render("Fuel", True, [0, 0, 0])
        power = self.font.render("Power", True, [0, 0, 0])
        self.surface.blit(rocket_param, (self.width / 2 - 150, 10))
        self.surface.blit(time, (self.width / 2 - 100, 80))
        self.surface.blit(height, (self.width / 2 - 100, 120))
        self.surface.blit(speed, (self.width / 2 - 100, 160))
        self.surface.blit(fuel, (self.width / 2 - 100, 200))
        self.surface.blit(power, (self.width / 2 - 100, 240))

        pygame.draw.rect(self.surface, BLACK, (self.width / 2 - 20, 190, 300, 40), width=1)
        pygame.draw.rect(self.surface, GREEN, (
        self.width / 2 - 19, 191, 298 * engine.rocket_parameters.fuel_remained / self.rocket.get_active_parameters()[4],
        38))

        pygame.draw.rect(self.surface, BLACK, (self.width / 2 - 10, 240, 300, 40), width=1)
        pygame.draw.rect(self.surface, RED, (
            self.width / 2 - 9, 241,
            298 * engine.rocket_parameters.engine_power / 100,
            38))


class SpaceView(View):
    def __init__(self, width, height, rocket):
        View.__init__(self, width / 2, height, width / 2, 0, rocket)

    def draw(self, engine):
        self.surface.fill(BLACK)
        scale = self.height / (6 * engine.constants.rad_Earth)
        x = engine.rocket_parameters.parameters[0]
        y = engine.rocket_parameters.parameters[1]
        pygame.draw.circle(self.surface, EARTH, (self.width / 2, self.height / 2), self.height / 6)
        pygame.draw.circle(self.surface, GREEN, (scale * x + self.width / 2, -scale * y + self.height / 2), 4)
        for current in engine.rocket_parameters.predicative_orbit:
            pygame.draw.circle(self.surface, WHITE,
                               (scale * current[0] + self.width / 2, -scale * current[1] + self.height / 2), 1)
