import pygame

BLUE = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]

rocket_view = pygame.Surface((1536 / 2, 864))
rocket_view.fill(BLUE)

pygame.draw.rect(rocket_view, GREEN, (0, 864 - 50, 1536 / 2, 50))
pygame.draw.rect(rocket_view, GREY, (100, 864 - 100, 1536 / 2 - 200, 50))




