import pygame
import sys
import cv2

BG = pygame.image.load("textures/menu/background.png")
"""Uploads background picture"""
pygame.mixer.music.load("textures/music/Star_finder.mp3")
"""Uploads background music"""
pygame.mixer.music.play(loops=0)
"""Plays the music"""


class Button:
    """
    Class of Buttons

    """

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
        Initializing buttons
        :param image: image
        :param pos: position on the screen
        :param text_input: text
        :param font: font
        :param base_color: basic color of a text
        :param hovering_color: color of a text when mouse is pointing on it
        """
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
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Checking whether the button was clicked on
        :param position:
        """
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom)

    def change_color(self, position):
        """
        Changes the color of button text when the mouse is on a button
        :param position: position of a mouse on the screen
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
    :return: pygame.font.Font("textures/menu/font.ttf", size)
    """
    return pygame.font.Font("textures/menu/font.ttf", size)


def play_video():
    """
    When CREDITS is clicked plays video.
    """
    file_name = "textures/credits/sw-3000.mp4"
    window_name = "window"
    inter_frame_wait_ms = 5

    video = cv2.VideoCapture(file_name)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = video.read()
        if not ret:
            print("Reached end of video, exiting.")
            break

        cv2.imshow(window_name, frame)
        if cv2.waitKey(inter_frame_wait_ms) & 0x7F == ord('q'):
            print("Exit requested.")
            break

    video.release()
    cv2.destroyAllWindows()


def buttons_define(screen, coef_w, coef_h):
    """
    Defining all the buttons anf texts
    :param screen: screen
    :param coef_w: used for width scale depending on users screen parameters
    :param coef_h: used for height scale depending on users screen parameters
    """
    text = get_font(100).render("MAIN MENU", True, "#b68f40")
    rect = text.get_rect(center=(960 * coef_w, 150 * coef_h))
    screen.blit(text, rect)

    play_button = Button(image=pygame.image.load("textures/menu/Play Rect.png"),
                         pos=(960 * coef_w, 375 * coef_h),
                         text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    credits_button = Button(image=pygame.image.load("textures/menu/Options Rect.png"),
                            pos=(960 * coef_w, 600 * coef_h),
                            text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=pygame.image.load("textures/menu/Quit Rect.png"),
                         pos=(960 * coef_w, 825 * coef_h),
                         text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    return play_button, credits_button, quit_button


def main_menu(screen, menu):
    """
    Main function of main_menu.py.
    :param screen: screen
    :param menu: type of menu: main menu, sandbox menu, play menu
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
                pygame.mixer.music.load("textures/music/credits.mp3")
                pygame.mixer.music.play(loops=0)
                play_video()
                pygame.mixer.music.stop()
            if quit_button.check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()
    return menu
