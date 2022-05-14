# import trajectory_calculation as tr
# import rocket_view
# import space_view
# import parameters_view
import sandbox_menu
import sandbox
import parts
import main_menu
import draw_screen

import pygame

import trajectory_calculation

pygame.init()
FPS = 20

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

window_width, window_height = pygame.display.get_surface().get_size()

rocket = sandbox.Rocket()
# engine = parts.Engine(rocket.surface, x=200, y=300)
# fuel_tank = parts.FuelTank(rocket.surface, x=100, y=100)
# rocket.add_part(engine)
# rocket.add_part(fuel_tank)

initial_position = [7e6, 0, 0, 8000]
rocket_parameters = trajectory_calculation.PhysicsEngine(80000, 4000, 300, 50000, 50000, initial_position)
constants = rocket_parameters.constants
rocket_parameters.rocket_parameters.parameters = [constants.rad_Earth, 0, 0, 0]

#rocket_parameters.rocket_parameters.predicative_orbit

Rocket_surface = draw_screen.RocketView(window_width, window_height, rocket)
Space_surface = draw_screen.SpaceView(window_width, window_height, rocket)
Parameters_surface = draw_screen.ParametersView(window_width, window_height, rocket)

Views = [Rocket_surface, Space_surface, Parameters_surface]

print(Rocket_surface.width, Rocket_surface.height)

clock = pygame.time.Clock()
finished = False

pygame.display.update()

start_ticks = pygame.time.get_ticks()

counter = 0
flag_seconds = 0
flag_start = 0


def draw_everything():
    for view in Views:
        view.draw()
        window.blit(view.surface, (view.x, view.y))


flag_menu = "main menu"

rocket_parts = []
while not finished:

    clock.tick(FPS)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    # events = pygame.event.get()

    if flag_menu == "main menu":
        flag_menu = main_menu.main_menu(window, flag_menu)
    elif flag_menu == "sandbox menu":
        flag_menu, rocket = sandbox_menu.sandbox(window, flag_menu, window_width, window_height, rocket)
        if flag_menu == "play_menu":
            for i in rocket_parts:
                print()
    else:
        if (flag_start == "play_menu") and (seconds - flag_seconds >= 0.1):
            flag_seconds = seconds
            counter += 1
            rocket_parameters.process_step()
            draw_everything()

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
