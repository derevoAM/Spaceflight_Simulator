import random
import sys

import pygame

import parts

BG = pygame.image.load("textures/sandbox_menu/sandbox_back.png")

pygame.mixer.init()
playlist = [
    "textures/music/Trava_u_doma.mp3",
    "textures/music/Star_finder.mp3",
    "textures/music/Fly_Me_To_The_Moon.mp3",
    "textures/music/Counting_Stars.mp3",
    "textures/music/Boyfriend.mp3",
    "textures/music/My_Way.mp3",
    "textures/music/Stop.mp3",
]


def get_font(size):  # Returns Press-Start-2P in the desired size
    """
    Returns
    :param size: font size
    :return:
    """
    return pygame.font.Font("textures/menu/font.ttf", size)


class Button:
    """
    Class of buttons(texts and images)
    """

    def __init__(self, image, pos):
        """
        Initializing a button
        :param image: image
        :param pos: position on the screen
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Drawing object on screen
        :param screen: screen itself
        """
        pass

    def check_for_input(self, position):
        """
        Checking whether an image(text or part of a rocket) was clicked on
        :param position: position of a mouse click
        :return: True, if clicked, false, if not clicked
        """
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom)


class ButtonText(Button):
    """
    Class of text buttons

    """

    def __init__(self, image, pos, text_input="", base_color="#d7fcd4", hovering_color="White"):
        """
        Initializing text button
        :param image: image
        :param pos: position on the screen
        :param text_input: text itself
        :param base_color: color
        :param hovering_color: color, when the mouse is on the button(not necessary clicked_
        """
        Button.__init__(self, image, pos)
        self.text_input = text_input
        self.font = get_font(25)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Updating text button on the screen
        :param screen: screen
        """
        screen.blit(self.text, self.text_rect)


class PartsButton(Button):
    """
    Class of parts of a rocket, which are placed in sandbox menu to choose, as buttons
    """

    def __init__(self, entity, pos, image):
        """
        Initializing part button
        :param entity: object of class Entity(Engine, FuelTank, Cabin) from parts
        :param pos: position on the screen
        :param image: texture of the particular part
        """
        Button.__init__(self, image, pos)
        self.entity = entity

    def update(self, screen):
        """
        Function, which adds part(button) to the screen
        :param screen: screen
        """
        self.rect = self.entity.texture.get_rect(center=(self.x_pos, self.y_pos))
        screen.blit(self.entity.texture, self.rect)


class Parts:
    """
    Class of parts of a rocket, which are drawn on the sandbox_menu
    """

    def __init__(self, x, y, screen, rocket=None, text="Build rocket", size=50):
        """
        Initializing a particular part of a rocket
        :param x: x coordinate of image on the screen
        :param y: y coordinate of image on the screen
        :param screen: screen
        :param rocket: object of class Rocket from sandbox
        :param text: the name of a part
        :param size: size of text, representing the part
        """
        self.render = get_font(size).render(text, True, "#b68f40")
        self.rect = self.render.get_rect(center=(x, y))
        self.screen = screen
        self.rocket = rocket
        self.arr = []

    def blit(self):
        """
        Function, which adds text on screen
        """
        self.screen.blit(self.render, self.rect)

    def update(self, size):
        """
        Function, which adds all database of a particular part of a particular size of a rocket to the screen
        :param size: width of a rocket
        """
        for element in self.arr:
            if (size == 0) or element.entity.texture.get_size()[0] == size:
                element.update(self.screen)

    def resize(self):
        """
        Function, which changes the size of an image of a part of a rocket
        """
        pass


class Cabin(Parts):
    """
    Cabin class, inherited from class Parts
    """

    def __init__(self, screen, width, height, rocket):
        """
        Initializing cabin class
        :param screen: screen
        :param width: screen width
        :param height: screen height
        :param rocket: object of class Rocket from sandbox
        """
        Parts.__init__(self, int(width * 0.16), int(height / 12), screen, rocket=rocket, text="Choose capsule", size=30)
        self.arr = [PartsButton(parts.Cabin(rocket.surface, mass=5000), pos=(int(width * 0.15), height / 4 - 50),
                                image=pygame.image.load("textures/capsule/final/capsule_270x180.png")),
                    PartsButton(parts.Cabin(rocket.surface, mass=3000), pos=(int(width * 0.15), height / 4 - 50),
                                image=pygame.image.load("textures/capsule/final/capsule_270x180.png")),
                    PartsButton(parts.Cabin(rocket.surface, mass=1500), pos=(int(width * 0.15), height / 4 - 50),
                                image=pygame.image.load("textures/capsule/final/capsule_270x180.png"))
                    ]

    def resize(self):
        """
        Resizes the size of Cabin parts.
        """
        self.arr[0].entity.texture = pygame.transform.scale(self.arr[0].image, (80, 120))
        self.arr[1].entity.texture = pygame.transform.scale(self.arr[1].image, (60, 90))
        self.arr[2].entity.texture = pygame.transform.scale(self.arr[2].image, (40, 60))


class Tanks(Parts):
    """
    Fuel tanks class, inherited from class Parts
    """

    def __init__(self, screen, width, height, rocket):
        """
        Initializing fuel tanks class
        :param screen: screen
        :param width: screen width
        :param height: screen height
        :param rocket: object of class Rocket from sandbox
        """
        Parts.__init__(self, int(width * 0.20), int(height * 0.32), screen, rocket=rocket,
                       text="Choose fuel tanks(max 4)", size=25)

        self.arr = [
            PartsButton(parts.FuelTank(rocket.surface, capacity=20000, mass=22000), pos=(int(width * 0.04), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_180x180.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=35000, mass=38500), pos=(int(width * 0.12), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_270x180.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=45000, mass=49500), pos=(int(width * 0.20), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_360x180.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=30000, mass=33000), pos=(int(width * 0.04), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_180x240.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=40000, mass=44000), pos=(int(width * 0.12), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_270x240.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=550000, mass=60000),
                        pos=(int(width * 0.20), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_360x240.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=27000, mass=30000), pos=(int(width * 0.04), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_270x120.png")),
            PartsButton(parts.FuelTank(rocket.surface, capacity=35000, mass=39000), pos=(int(width * 0.12), height / 2),
                        image=pygame.image.load("textures/tanks/final/fuel_tank_360x120.png"))

        ]

    def resize(self):
        """
        Resizes the size of Fuel Tank parts.
        """
        self.arr[0].entity.texture = pygame.transform.scale(self.arr[0].image, (60, 60))
        self.arr[1].entity.texture = pygame.transform.scale(self.arr[1].image, (60, 90))
        self.arr[2].entity.texture = pygame.transform.scale(self.arr[2].image, (60, 120))
        self.arr[3].entity.texture = pygame.transform.scale(self.arr[3].image, (80, 60))
        self.arr[4].entity.texture = pygame.transform.scale(self.arr[4].image, (80, 90))
        self.arr[5].entity.texture = pygame.transform.scale(self.arr[5].image, (80, 120))
        self.arr[6].entity.texture = pygame.transform.scale(self.arr[6].image, (40, 90))
        self.arr[7].entity.texture = pygame.transform.scale(self.arr[7].image, (40, 120))


class Engines(Parts):
    """
    Engines class, inherited from class Parts
    """

    def __init__(self, screen, width, height, rocket):
        """
        Initializing engines class
        :param screen: screen
        :param width: screen width
        :param height: screen height
        :param rocket: object of class Rocket from sandbox
        """
        Parts.__init__(self, int(width * 0.16), int(height * 0.64), screen, rocket=rocket, text="Choose engine",
                       size=30)

        self.arr = [PartsButton(parts.Engine(rocket.surface, power=10000, consumption=1, mass=3000),
                                pos=(int(width * 0.04), 3 * height / 4),
                                image=pygame.image.load("textures/engines/final/engine_180x120.png")),
                    PartsButton(parts.Engine(rocket.surface, power=20000, consumption=3, mass=5000),
                                pos=(int(width * 0.10), 3 * height / 4),
                                image=pygame.image.load("textures/engines/final/engine_270x180.png")),
                    PartsButton(parts.Engine(rocket.surface, power=40000, consumption=7, mass=9000),
                                pos=(int(width * 0.16), 3 * height / 4),
                                image=pygame.image.load("textures/engines/final/engine_360x240.png"))
                    ]

    def resize(self):
        """
        Resizes the size of Engine parts.
        """
        self.arr[0].entity.texture = pygame.transform.scale(self.arr[0].image, (40, 60))
        self.arr[1].entity.texture = pygame.transform.scale(self.arr[1].image, (60, 90))
        self.arr[2].entity.texture = pygame.transform.scale(self.arr[2].image, (80, 120))


def upload_parts(arr, size):
    """
    Changing and placing all images on to the screen
    :param arr: array of parts of a rocket
    :param size: texture width, used to choose right parts in terms of rocket width
    """
    for part in arr:
        part.resize()
        part.blit()
        part.update(size)


def upload_text(arr, screen):
    """
    Placing all texts buttons on to the screen
    :param arr: array of text buttons
    :param screen: screen
    """
    for part in arr:
        part.update(screen)


def music_buttons_control(events, text_array):
    """
    The function plays, pauses, or continues to play music if corresponding button is clicked
    :param events: events
    :param text_array: text buttons
    """
    menu_mouse_pos = pygame.mouse.get_pos()

    play_music_button, pause_music_button = text_array[3], text_array[4]

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_music_button.check_for_input(menu_mouse_pos):
                pygame.mixer.music.stop()
                if pygame.mixer.music.get_busy() is False:
                    pygame.mixer.music.load(playlist[random.randint(0, 6)])
                    pygame.mixer.music.play(loops=0)
            if pause_music_button.check_for_input(menu_mouse_pos):
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()


def gameplay_check_events(screen, events, mouse_pos, text, rocket, parts_arr, part_choose, menu):
    """
    Analyzing whether part button was clicked on and change the state
    :param screen: screen
    :param events: events
    :param mouse_pos: mouse position
    :param text: type of part
    :param rocket: object of class Rocket from sandbox
    :param parts_arr: array of displayed parts
    :param part_choose: array of a part of a rocket, which is being selected in this particular moment, and its width
    :param menu: type of menu: main menu, sandbox menu, play menu
    :return: menu, part_choose, rocket
    """
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if text[0].check_for_input(mouse_pos):
                menu = "play menu"
                screen.fill((0, 0, 0, 0))
            if text[1].check_for_input(mouse_pos):
                part_choose = ["engine", 0]
                rocket.parts.clear()
                rocket.surface = pygame.Surface([rocket.width, rocket.height], pygame.SRCALPHA)
            if text[2].check_for_input(mouse_pos):
                menu = "main menu"
            for segments in parts_arr:
                for part in segments.arr:
                    if part.check_for_input(mouse_pos) and (
                            (part_choose[1] == 0) or (part.entity.texture.get_size()[0] == part_choose[1])):
                        match part_choose[0]:
                            case "engine":
                                part_choose[1] = part.entity.texture.get_size()[0]
                                part_choose[0] = "capsule"
                            case "capsule":
                                part_choose[0] = "fuel tank"
                        rocket.add_part(part.entity)

    return menu, part_choose, rocket


def gameplay_buttons_control(screen, menu, width, height, rocket, events, text_array, part_choose):
    """
     The function performs the exact game actions when corresponding button is clicked
    :param screen: screen
    :param menu: type of menu: main menu, sandbox menu, play menu
    :param width: screen width
    :param height: screen height
    :param rocket: object of class Rocket from sandbox
    :param events: events
    :param text_array: array of text buttons
    :param part_choose: array of a part of a rocket, which is being selected in this particular moment, and its width
    :return: menu, part_choose
    """

    menu_mouse_pos = pygame.mouse.get_pos()

    create_rocket = Parts(width / 2, 40, screen)
    capsule = Cabin(screen, width, height, rocket=rocket)
    tanks = Tanks(screen, width, height, rocket=rocket)
    engines = Engines(screen, width, height, rocket=rocket)
    parts_array = [create_rocket]
    match part_choose[0]:
        case "engine":
            parts_array.append(engines)
        case "fuel tank":
            parts_array.append(tanks)
        case "capsule":
            parts_array.append(capsule)

    upload_parts(parts_array, part_choose[1])

    menu, part_choose, rocket = gameplay_check_events(screen, events, menu_mouse_pos, text_array, rocket, parts_array,
                                                      part_choose, menu)

    return menu, part_choose


def text_buttons_define(width, height):
    """
    Defines and creates 5 buttons: 3 for gameplay, 2 for playing music
    :param width: screen width
    :param height: screen height
    """
    play_button = ButtonText(image=pygame.transform.scale(pygame.image.load("textures/menu/Play Rect.png"), (100, 20)),
                             pos=(width - 100, height - 100), text_input="PLAY")
    restart_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("textures/menu/Play Rect.png"), (190, 20)),
        pos=(width - 100, height - 150), text_input="RESTART")
    back_button = ButtonText(image=pygame.transform.scale(pygame.image.load("textures/menu/Play Rect.png"), (100, 20)),
                             pos=(width - 100, height - 50), text_input="BACK")
    play_music_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("textures/menu/Play Rect.png"), (350, 40)),
        pos=(width - 225, 50), text_input="Play Random Song")
    pause_music_button = ButtonText(
        image=pygame.transform.scale(pygame.image.load("textures/menu/Play Rect.png"), (350, 40)),
        pos=(width - 225, 100), text_input="Pause/Continue")

    return [play_button, restart_button, back_button, play_music_button, pause_music_button]


def sandbox(screen, menu, width, height, rocket, events, part_choose):
    """
    The main function of sandbox_menu.py
    :param screen: screen
    :param menu: type of menu: main menu, sandbox menu, play menu
    :param width: screen width
    :param height: screen height
    :param rocket: object of class Rocket from sandbox
    :param events: events
    :param part_choose:  part of a rocket, which is being selected in this particular moment, with the size of a texture
    :return: menu, rocket, part_choose
    """
    screen.blit(BG, (0, 0))

    text_array = text_buttons_define(width, height)
    upload_text(text_array, screen)

    menu, part_choose = gameplay_buttons_control(screen, menu, width, height, rocket, events, text_array, part_choose)
    music_buttons_control(events, text_array)

    rocket.recount()
    screen.blit(rocket.surface, (width / 2, 100))
    return menu, rocket, part_choose
