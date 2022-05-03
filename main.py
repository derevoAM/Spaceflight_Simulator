import sandbox as sand
import trajectory_calculation as tr
# import draw as dr
import rocket_view as r_v
import space_view as s_v
import parameters_view as p_v
import pygame

pygame.init()
FPS = 30

window = r_v.window

print(r_v.w, r_v.h)

clock = pygame.time.Clock()
finished = False

pygame.display.update()

start_ticks = pygame.time.get_ticks()

counter = 0
flag_seconds = 0
while not finished:
    clock.tick(FPS)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds - flag_seconds >= 0.1:
        flag_seconds = seconds
        counter += 1
        r_v.rocket_position(tr.position_and_velocity_log[counter])
        s_v.draw_everything(tr.position_and_velocity_log[counter])
        p_v.parameters(tr.position_and_velocity_log[counter])

        window.blit(r_v.rocket_view, (r_v.w / 2, 0))
        window.blit(s_v.space_view, (0, r_v.h / 2))
        window.blit(p_v.parameters_view, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
    pygame.display.update()

pygame.quit()
