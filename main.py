import sandbox as sand
import trajectory_calculation as tr
#import draw as dr
import rocket_view as r_v
import pygame

pygame.init()
FPS = 30

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

w, h = pygame.display.get_surface().get_size()

print(w, h)

clock = pygame.time.Clock()
finished = False

pygame.display.update()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
    window.blit(r_v.rocket_view, (1536 / 2, 0))
    pygame.display.update()

pygame.quit()
