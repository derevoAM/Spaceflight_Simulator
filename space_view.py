# from space point of view
import pygame
import trajectory_calculation as tr
import rocket_view as r_v

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]
EARTH = [31, 67, 242]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

space_view = pygame.Surface((r_v.w / 2, r_v.h / 2))

space_view.fill(BLACK)

radius = r_v.h / 16

scale = radius / tr.const.rad_Earth


def draw_everything(arr):
    space_view.fill((0, 0, 0, 0))
    pygame.draw.circle(space_view, WHITE, (
        scale * arr[0] + r_v.w / 4, scale * arr[1] + r_v.h / 4),
                       10)
    pygame.draw.circle(space_view, EARTH, (r_v.w / 4, r_v.h / 4), radius)
    for i in range(tr.counter):
        pygame.draw.rect(space_view, WHITE,
                         (scale * tr.position_and_velocity_log[i][0] + r_v.w / 4,
                          scale * tr.position_and_velocity_log[i][1] + r_v.h / 4, 1, 1))
