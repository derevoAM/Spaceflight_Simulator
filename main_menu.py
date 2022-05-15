import pygame
import sys

pygame.init()

coefficient_w = pygame.display.Info().current_w / 1920
"""The horizontal linear coefficient for scaling"""
coefficient_h = pygame.display.Info().current_h / 1080
"""The vertical linear coefficient for scaling"""

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Menu")

BG = pygame.image.load("Textures/menu/background.png")
"""Uploads background picture"""
pygame.mixer.music.load("Textures/music/Star_finder.mp3")
"""Uploads background music"""
pygame.mixer.music.play(loops=0)
"""Plays the music"""


class Button:
    """
    Class for Buttons

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
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                              self.rect.bottom)

    def change_color(self, position):
        """
        Changes the color of button text when the mouse is on a button.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Textures/menu/font.ttf", size)


def main_menu(SCREEN, flag):
    """
    Main function of main_menu.py.
    """
    SCREEN.blit(BG, (0, 0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(960 * coefficient_w, 150 * coefficient_h))

    PLAY_BUTTON = Button(image=pygame.image.load("Textures/menu/Play Rect.png"),
                         pos=(960 * coefficient_w, 375 * coefficient_h),
                         text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("Textures/menu/Options Rect.png"),
                            pos=(960 * coefficient_w, 600 * coefficient_h),
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("Textures/menu/Quit Rect.png"),
                         pos=(960 * coefficient_w, 825 * coefficient_h),
                         text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

    SCREEN.blit(MENU_TEXT, MENU_RECT)

    for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        button.change_color(MENU_MOUSE_POS)
        button.update(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                pygame.mixer.music.stop()
                flag = "sandbox menu"
                SCREEN.fill((0, 0, 0, 0))
            if OPTIONS_BUTTON.check_for_input(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
            if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()
    return flag
