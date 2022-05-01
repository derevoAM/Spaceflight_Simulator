import pygame.draw as dr
import pygame
import math
import time

FPS = 60

RED = 0xFF0000
LIGHT_BLUE = 0x55e2e3
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = 0x5d8900
INTERFACE_COLOR = 0x999696
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1100
HEIGHT = 600

def draw_mukhomor(x, y, lx, ly, angle, screen):
    shape_surf = pygame.Surface([max(lx, ly), max(lx, ly)], pygame.SRCALPHA)
    dr.ellipse(shape_surf, (160, 160, 160), [lx / 2 - ly / 2, 0, ly, lx])
    dr.ellipse(shape_surf, (104, 102, 103), [lx / 2 - ly / 2, 0, ly, lx], width=1)
    dr.ellipse(shape_surf, (212, 50, 19), [0, 0, lx, ly])
    dr.ellipse(shape_surf, (104, 102, 103), [0, 0, lx, ly], width=1)
    dr.ellipse(shape_surf, (255, 255, 255), [lx / 4, ly / 4, lx / 8, ly / 6])
    dr.ellipse(shape_surf, (255, 255, 255), [lx / 2, ly / 3, lx / 6, ly / 7])
    dr.ellipse(shape_surf, (255, 255, 255), [3 * lx / 4, ly / 4, lx / 6, ly / 7])
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    screen.blit(rotated_surf, dest=[x, y])

image = pygame.Surface([100, 100], pygame.SRCALPHA)
#draw_mukhomor(15, 25, 70, 50, 0, image)
dr.circle(image, (255, 255, 255), (50, 50), 40)

def blitRotate(surf, image, pos, originPos, angle):
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

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)


pygame.init()
drawing_screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False
ir = 0

while not finished:
    clock.tick(FPS)
    drawing_screen.fill(BLACK)
    drawing_screen.blit(image, (100, 100))
    blitRotate(drawing_screen, image, (300, 300), (50, 50), ir)
    pygame.display.update()
    ir += 3
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
