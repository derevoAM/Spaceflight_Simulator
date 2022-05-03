# rocket point of view
import pygame
import trajectory_calculation as tr
import sandbox as sb

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

w, h = pygame.display.get_surface().get_size()
rocket_view = pygame.Surface((w / 2, h))
rocket_view.fill(SKY)

pygame.draw.rect(rocket_view, GREEN, (0, h - 50, w / 2, 50))
pygame.draw.rect(rocket_view, GREY, (100, h - 100, w / 2 - 200, 50))
pygame.draw.line(rocket_view, [0, 0, 0], (w / 4, 0), (w / 4, h))
rocket_view.blit(sb.r.surface, (w / 4 - sb.r.width / 2, 0))


def rocket_position(arr):
    x = arr[0]
    y = arr[1]
    height = (x ** 2 + y ** 2) ** 0.5 - tr.const.rad_Earth
    if int(255 * (1 - height / (3 * 10 ** 5))) > 0:
        SKY[2] = int(255 * (1 - height / (3 * 10 ** 5)))
    else:
        SKY[2] = 0
    if int(42 * (1 - height / (3 * 10 ** 5))) > 0:
        SKY[1] = int(42 * (1 - height / (3 * 10 ** 5)))
    else:
        SKY[1] = 0

    #print(SKY, height)
    rocket_view.fill(SKY)
    rocket_view.blit(sb.r.surface, (w / 4 - sb.r.width / 2, 0))
    pygame.draw.rect(rocket_view, GREEN, (0, h - 50, w / 2, 50))
    pygame.draw.rect(rocket_view, GREY, (100, h - 100, w / 2 - 200, 50))
