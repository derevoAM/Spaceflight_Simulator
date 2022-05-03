import trajectory_calculation as tr
# import draw as dr
import rocket_view as r_v
import space_view as s_v
import parameters_view as p_v
import sandbox as s_b
import main_menu as m_m

import pygame

pygame.init()
FPS = 20

window = r_v.window

print(r_v.w, r_v.h)

clock = pygame.time.Clock()
finished = False

pygame.display.update()

start_ticks = pygame.time.get_ticks()

counter = 0
flag_seconds = 0
flag_start = 0
flag_menu = 0


def draw_screen(sec):
    r_v.rocket_position(s_b.rocket.parameters)
    s_v.draw_everything(s_b.rocket.parameters)
    p_v.parameters(s_b.rocket.parameters, sec)

    window.blit(r_v.rocket_view, (r_v.w / 2, 0))
    window.blit(s_v.space_view, (0, r_v.h / 2))
    window.blit(p_v.parameters_view, (0, 0))






while not finished:

    clock.tick(FPS)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    #events = pygame.event.get()

    if flag_menu == 0:
        flag_menu = m_m.main_menu(window, flag_menu)
        if flag_menu == 1:
            draw_screen(0)
    else:

        if (flag_start == 1) and (seconds - flag_seconds >= 0.1):
            flag_seconds = seconds
            counter += 1
            draw_screen(counter * 5)
            tr.process_step(s_b.rocket, 5, True, seconds, s_b.constants)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True
                if event.key == pygame.K_SPACE:
                    flag_start = 1
    pygame.display.update()

pygame.quit()
