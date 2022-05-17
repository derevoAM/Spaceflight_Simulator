import pygame
import sys

# import cv2

BG = pygame.image.load("Textures/menu/background.png")
"""Uploads background picture"""
pygame.mixer.music.load("Textures/music/Star_finder.mp3")
"""Uploads background music"""
pygame.mixer.music.play(loops=0)
"""Plays the music"""


class Button:
    """
    Class of Buttons
    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Drawing buttons on the screen
        :param screen: screen
        :return: None
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Checking whether the button was clicked on
        :param position: position of the pointer on the screen
        :return: None
        """
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom)

    def change_color(self, position):
        """
        Changes the color of button text when the mouse is on a button.
        :param: position of the pointer on the screen
        :return: None
        """

        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):
    """
    Returns font with exact size
    :param size: size of font
    :return: pygame.font.Font("Textures/menu/font.ttf", size)
    """
    return pygame.font.Font("Textures/menu/font.ttf", size)


# def play_video():
#     """
#     When CREDITS is clicked plays video.
#     :return none:
#     """
#     file_name = "Textures/credits/sw-3000.mp4"
#     window_name = "window"
#     inter_frame_wait_ms = 5
#
#     video = cv2.VideoCapture(file_name)
#     cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
#     cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#
#     while True:
#         ret, frame = video.read()
#         if not ret:
#             print("Reached end of video, exiting.")
#             break
#
#         cv2.imshow(window_name, frame)
#         if cv2.waitKey(inter_frame_wait_ms) & 0x7F == ord('q'):
#             print("Exit requested.")
#             break
#
#     video.release()
#     cv2.destroyAllWindows()


def buttons_define(screen, coeff_w, coeff_h):
    """
    Defining all the buttons anf texts
    :param screen: screen
    :param coeff_w: used for width scale depending on users screen parameters
    :param coeff_h: used for height scale depending on users screen parameters
    :return:
    """
    text = get_font(100).render("MAIN MENU", True, "#b68f40")
    rect = text.get_rect(center=(960 * coeff_w, 150 * coeff_h))
    screen.blit(text, rect)

    play_button = Button(image=pygame.image.load("Textures/menu/Play Rect.png"),
                         pos=(960 * coeff_w, 375 * coeff_h),
                         text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    credits_button = Button(image=pygame.image.load("Textures/menu/Options Rect.png"),
                            pos=(960 * coeff_w, 600 * coeff_h),
                            text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=pygame.image.load("Textures/menu/Quit Rect.png"),
                         pos=(960 * coeff_w, 825 * coeff_h),
                         text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    return play_button, credits_button, quit_button


def credits_menu(screen):
    """
    Draws the screen of Credits (press b to quit)
    :param screen: the surface where function draws
    :return: menu - shows the type of next menu
    """
    FPS = 30
    clock = pygame.time.Clock()
    while True:
        credits_back = pygame.image.load("Textures/credits/credits_back.png")
        screen.blit(credits_back, (0, 0))

        clock.tick(FPS)
        # pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    menu = "main menu"
                    screen.fill((0, 0, 0, 0))
                    return menu


def main_menu(screen, menu):
    """
    Main function of main_menu.py
    :param screen: screen
    :param menu: type of menu: main menu, sandbox menu, play menu
    :return: menu - shows the type of next menu
    """
    screen.blit(BG, (0, 0))
    coefficient_w = screen.get_size()[0] / 1920
    coefficient_h = screen.get_size()[1] / 1080
    menu_mouse_pos = pygame.mouse.get_pos()

    play_button, credits_button, quit_button = buttons_define(screen, coefficient_w, coefficient_h)

    for button in [play_button, credits_button, quit_button]:
        button.change_color(menu_mouse_pos)
        button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.check_for_input(menu_mouse_pos):
                pygame.mixer.music.stop()
                menu = "sandbox menu"
                screen.fill((0, 0, 0, 0))
            if credits_button.check_for_input(menu_mouse_pos):
                pygame.mixer.music.stop()
                menu = credits_menu(screen)
                # pygame.mixer.music.load("Textures/music/credits.mp3")
                # pygame.mixer.music.play(loops=0)
                # play_video()
            if quit_button.check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()
    return menu
