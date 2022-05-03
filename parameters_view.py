# parameters
import pygame
# import trajectory_calculation as tr
import rocket_view as r_v
import sandbox as s_b

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]

parameters_view = pygame.Surface((r_v.w / 2, r_v.h / 2))
parameters_view.fill(GREY)


def parameters(arr, it):
    parameters_view.fill(GREY)
    font = pygame.font.Font(None, 40)
    x = arr[0]
    y = arr[1]
    t = font.render(f"Time = " + str(it) + "c", True, [0, 0, 0])
    speed = font.render(f"Speed = {((arr[2]**2 + arr[3]**2)**0.5):.2f} м/c", True, [0, 0, 0])
    height = font.render(f"Height = {((x ** 2 + y ** 2) ** 0.5 - s_b.constants.rad_Earth)/1000:.2f} км", True, [0, 0, 0])
    parameters_view.blit(speed, (r_v.w / 4 - 100, 100))
    parameters_view.blit(height, (r_v.w / 4 - 100, 60))
    parameters_view.blit(t, (r_v.w / 4 - 100, 20))

