import pygame
import sys
import parts
import random

BG = pygame.image.load("Textures/sandbox_menu/sandbox_back.png")

pygame.mixer.init()
playlist = [
    "Textures/music/Trava_u_doma.mp3",
    "Textures/music/Star_finder.mp3",
    "Textures/music/Fly_Me_To_The_Moon.mp3",
    "Textures/music/Counting_Stars.mp3",
    "Textures/music/Boyfriend.mp3",
    "Textures/music/My_Way.mp3",
    "Textures/music/Stop.mp3",
]


class Button:
    """
    Class of buttons(texts and images)
    """

    def __init__(self, image, pos):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Drawing object on scren
        :param screen: screen itself
        :return:
        """
        pass

    def check_for_input(self, position):
        """
        Checking whether an image(text or part of a rocket) was clicked on
        :param position: position of a mouse click
        :return:
        """
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom)


class ButtonText(Button):
    """
    Class of text buttons

    """

    def __init__(self, image, pos, text_input="", base_color="#d7fcd4", hovering_color="White"):
        Button.__init__(self, image, pos)
        self.text_input = text_input
        self.font = get_font(25)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class PartsButton(Button):
    """
    Class of parts of a rocket, which are placed in sandbox menu to choose, as buttons
    """

    def __init__(self, entity, pos, image):
        Button.__init__(self, image, pos)
        self.entity = entity

    def update(self, screen):
        """
        Function, which adds part(button) to the screen
        :param screen: main window
        :return: none
        """
        self.rect = self.entity.texture.get_rect(center=(self.x_pos, self.y_pos))
        screen.blit(self.entity.texture, self.rect)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Textures/menu/font.ttf", size)


class Parts:
    """
    Class of parts of a rocket, which are drawn on the sandbox_menu
    """

    def __init__(self, x, y, window, rocket=None, text="Build rocket", size=50):
        self.render = get_font(size).render(text, True, "#b68f40")
        self.rect = self.render.get_rect(center=(x, y))
        self.window = window
        self.rocket = rocket
        self.arr = []

    def blit(self):
        """
        Function, which adds text on screen
        :return:
        """
        self.window.blit(self.render, self.rect)

    def update(self):
        """
        Function, which adds all database of a particular part of a rocket to the screen
        :return:
        """
        for element in self.arr:
            element.update(self.window)

    def resize(self):
        """
        Function, which changes the size of an image of a part of a rocket
        :return:
        """
        pass


class Cabin(Parts):
    """
    Cabin class, inherited from class Parts
    """

    def __init__(self, window, width, height, rocket):
        Parts.__init__(self, int(width * 0.11), int(height / 12), window, rocket=rocket, text="Capsules", size=30)
        self.arr = [PartsButton(parts.Cabin(rocket.surface, mass=3000), pos=(int(width * 0.07), height / 4),
                                image=pygame.image.load("Textures/capsule/final/capsule_270x180.png")),
                    PartsButton(parts.Cabin(rocket.surface, mass=3000), pos=(int(width * 0.15), height / 4),
                                image=pygame.image.load("Textures/capsule/final/capsule_270x180.png"))]

    def resize(self):
        self.arr[0].entity.texture = pygame.transform.scale(self.arr[0].image, (90, 60))
        self.arr[1].entity.texture = pygame.transform.scale(self.arr[1].image, (60, 40))


class Tanks(Parts):
    """
    Fuel tanks class, inherited from class Parts
    """

    def __init__(self, window, width, height, rocket):
        Parts.__init__(self, int(width * 0.11), int(height * 0.32), window, rocket=rocket, text="Fuel tanks", size=30)

        self.arr = [
            PartsButton(parts.FuelTank(rocket.surface, capacity=20000, mass=2000), pos=(int(width * 0.04), height / 2),
                        image=pygame.image.load("Textures/tanks/final/fuel_tank_180x180.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=30000, mass=3000), pos=(int(width * 0.09), height / 2),
                        image=pygame.image.load("Textures/tanks/final/fuel_tank_180x240.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=35000, mass=3500), pos=(int(width * 0.15), height / 2),
                        image=pygame.image.load("Textures/tanks/final/fuel_tank_270x180.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=45000, mass=4500), pos=(int(width * 0.20), height / 2),
                        image=pygame.image.load("Textures/tanks/final/fuel_tank_360x180.png"))
        ]

    def resize(self):
        self.arr[0].entity.texture = pygame.transform.scale(self.arr[0].image, (60, 60))
        self.arr[1].entity.texture = pygame.transform.scale(self.arr[1].image, (80, 40))
        self.arr[2].entity.texture = pygame.transform.scale(self.arr[2].image, (60, 90))
        self.arr[3].entity.texture = pygame.transform.scale(self.arr[3].image, (60, 120))


class Engines(Parts):
    """
    Engines class, inherited from class Parts
    """

    def __init__(self, window, width, height, rocket):
        Parts.__init__(self, int(width * 0.11), int(height * 0.64), window, rocket=rocket, text="Engines", size=30)

        self.arr = [PartsButton(parts.Engine(rocket.surface, power=1000, consumption=100, mass=3000),
                                pos=(int(width * 0.04), 3 * height / 4),
                                image=pygame.image.load("Textures/engines/final/engine_180x120.png")),
                    PartsButton(parts.Engine(rocket.surface, power=2000, consumption=300, mass=5000),
                                pos=(int(width * 0.10), 3 * height / 4),
                                image=pygame.image.load("Textures/engines/final/engine_270x180.png")),
                    PartsButton(parts.Engine(rocket.surface, power=4000, consumption=700, mass=9000),
                                pos=(int(width * 0.16), 3 * height / 4),
                                image=pygame.image.load("Textures/engines/final/engine_360x240.png"))
                    ]

    def resize(self):
        self.arr[0].entity.texture = pygame.transform.scale(self.arr[0].image, (40, 60))
        self.arr[1].entity.texture = pygame.transform.scale(self.arr[1].image, (60, 90))
        self.arr[2].entity.texture = pygame.transform.scale(self.arr[2].image, (80, 120))


def upload_parts(arr):
    """
    Changing and placing all images on to the screen
    :param arr: array of parts of a rocket
    :return: none
    """
    for part in arr:
        part.resize()
        part.blit()
        part.update()


def upload_text(arr, mouse_pos, screen):
    """
    Placing all texts buttons on to the screene
    :param arr: array of text buttons
    :param mouse_pos: mouse position
    :param screen: screen
    :return: none
    """
    for part in arr:
        part.change_color(mouse_pos)
        part.update(screen)


def sandbox(SCREEN, flag, width, height, rocket):
    SCREEN.blit(BG, (0, 0))

    menu_mouse_pos = pygame.mouse.get_pos()

    create_rocket = Parts(width / 2, 40, SCREEN)
    capsule = Cabin(SCREEN, width, height, rocket=rocket)
    tanks = Tanks(SCREEN, width, height, rocket=rocket)
    engines = Engines(SCREEN, width, height, rocket=rocket)

    parts_array = [capsule, tanks, engines, create_rocket]
    upload_parts(parts_array)

    play_button = ButtonText(image=pygame.transform.scale(pygame.image.load("Textures/menu/Play Rect.png"), (100, 20)),
                             pos=(width - 100, height - 100), text_input="PLAY")
    restart_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("Textures/menu/Play Rect.png"), (100, 20)),
        pos=(width - 100, height - 150), text_input="RESTART")
    back_button = ButtonText(image=pygame.transform.scale(pygame.image.load("Textures/menu/Play Rect.png"), (100, 20)),
                             pos=(width - 100, height - 50), text_input="BACK")
    play_music_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("Textures/menu/Play Rect.png"), (40, 40)),
        pos=(width - 100, 50), text_input="|>")
    pause_music_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("Textures/menu/Play Rect.png"), (40, 40)),
        pos=(width - 100, 100), text_input="||")
    unpause_music_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("Textures/menu/Play Rect.png"), (40, 40)),
        pos=(width - 100, 150), text_input="||>")

    text_array = [play_button, restart_button, back_button, play_music_button, pause_music_button, unpause_music_button]

    upload_text(text_array, menu_mouse_pos, SCREEN)

    # capsule1.update(SCREEN)
    # fuel1.update(SCREEN)

    # for button in [play_button, OPTIONS_BUTTON, QUIT_BUTTON]:
    #     button.changeColor(menu_mouse_pos)
    #     button.update(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.check_for_input(menu_mouse_pos):
                flag = "play menu"
                SCREEN.fill((0, 0, 0, 0))
            if restart_button.check_for_input(menu_mouse_pos):
                rocket.parts.clear()
                rocket.surface = pygame.Surface([rocket.width, rocket.height], pygame.SRCALPHA)
            if back_button.check_for_input(menu_mouse_pos):
                flag = "main menu"
            for segments in parts_array:
                for part in segments.arr:
                    if part.check_for_input(menu_mouse_pos):
                        rocket.add_part(part.entity)
            if play_music_button.check_for_input(menu_mouse_pos):
                pygame.mixer.music.stop()
                if pygame.mixer.music.get_busy() is False:
                    pygame.mixer.music.load(playlist[random.randint(0, 6)])
                    pygame.mixer.music.play(loops=0)
            if pause_music_button.check_for_input(menu_mouse_pos):
                pygame.mixer.music.pause()
            if unpause_music_button.check_for_input(menu_mouse_pos):
                pygame.mixer.music.unpause()

            # if QUIT_BUTTON.checkForInput(menu_mouse_pos):
            #     pygame.quit()
            #     sys.exit()
    rocket.recount()
    rocket.draw()
    SCREEN.blit(rocket.surface, (width / 2, 200))
    return flag, rocket
