import pygame
import sys

BG = pygame.image.load("Textures/menu/background.png")


class Button:
    """
    FIXME
    write some comments

    """

    def __init__(self, image, pos):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        # screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    # def changeColor(self, position):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
    #                                                                                       self.rect.bottom):
    #         self.text = self.font.render(self.text_input, True, self.hovering_color)
    #     else:
    #         self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Textures/menu/font.ttf", size)


class Parts:
    def __init__(self, x, y, window, text="Build rocket", size=50):
        self.render = get_font(size).render(text, True, "#b68f40")
        self.rect = self.render.get_rect(center=(x, y))
        self.window = window
        self.arr = []

    def blit(self):
        self.window.blit(self.render, self.rect)

    def update(self):
        for element in self.arr:
            element.update(self.window)


class Capsule(Parts):
    def __init__(self, window):
        Parts.__init__(self, 140, 90, window, "Capsule", size=30)
        self.arr = [Button("Textures/capsule/capsule_60x40.png", pos=(40, 200)),
                    Button("Textures/capsule/capsule_75x75.png", pos=(100, 200)),
                    Button("Textures/capsule/capsule_120x80.png", pos=(200, 200)), ]


class Tanks(Parts):
    def __init__(self, window):
        Parts.__init__(self, 190, 350, window, "Fuel tanks", size=30)


class Engines(Parts):
    def __init__(self, window):
        Parts.__init__(self, 140, 700, window, "Engines", size=30)


def sandbox(SCREEN, flag, width, height):
    SCREEN.blit(BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    # MENU_TEXT = get_font(60).render("Create Rocket", True, "#b68f40")
    # MENU_RECT = MENU_TEXT.get_rect(center=(width / 2, 40))
    #
    # capsule_text = get_font(30).render("Capsule", True, "#b68f40")
    # capsule_rect = capsule_text.get_rect(center=(140, 90))
    #
    # fuel_text = get_font(30).render("Fuel tank", True, "#b68f40")
    # fuel_rect = capsule_text.get_rect(center=(140, 350))
    #
    # engine_text = get_font(30).render("Engine", True, "#b68f40")
    # engine_rect = engine_text.get_rect(center=(140, 350))
    #
    # SCREEN.blit(MENU_TEXT, MENU_RECT)
    # SCREEN.blit(capsule_text, capsule_rect)
    # SCREEN.blit(fuel_text, fuel_rect)
    # SCREEN.blit(fuel_text, fuel_rect)

    create_rocket = Parts(width / 2, 40, SCREEN)
    capsule = Capsule(SCREEN)
    tanks = Tanks(SCREEN)
    engines = Engines(SCREEN)

    for part in [capsule, tanks, engines, create_rocket]:
        part.blit()
        part.update()

    # capsule1 = Button(image=pygame.image.load("Textures/capsule/capsule_60x40.png"), pos=(30, 200))
    # fuel1 = Button(image=pygame.image.load("Textures/tanks/tank_simple_100x75.png"), pos=(40, 500))

    PLAY_BUTTON = Button(image=pygame.image.load("Textures/menu/Play Rect.png"), pos=(960, 375))

    # capsule1.update(SCREEN)
    # fuel1.update(SCREEN)
    PLAY_BUTTON.update(SCREEN)
    # for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
    #     button.changeColor(MENU_MOUSE_POS)
    #     button.update(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                flag = "play menu"
                SCREEN.fill((0, 0, 0, 0))
            # if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            #     pygame.quit()
            #     sys.exit()
    return flag
