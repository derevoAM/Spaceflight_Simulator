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

# Initialize a rocket
rocket = sandbox.Rocket()

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


def draw_everything(engine):
    """
    Drawing play menu, which include 3 views
    :return:
    """
    for view in Views:
        view.draw(engine)
        window.blit(view.surface, (view.x, view.y))


flag_menu = "main menu"


def menu_type(flag, obj):
    """
    Function, that determines which menu to show
    :param flag: type of menu: main, sandbox, play
    :param obj: rocket
    :return: flag
    """
    if flag == "main menu":
        flag = main_menu.main_menu(window, flag)
    elif flag == "sandbox menu":
        flag, obj = sandbox_menu.sandbox(window, flag, window_width, window_height, obj, events)

    return flag


def play_menu(obj, engine, const, flag):
    """
    Function, which processes rocket parameters and calculate new step
    :param obj: object of class Rocket from sandbox file
    :param engine: object of class PhysicsEngine from trajetcory_calculation file
    :param const: object of class Constants from trajetcory_calculation file
    :param flag: shows whether right or left arrow was pressed
    :return: obj, engine, const
    """
    if engine is None:
        param = [6.37e6, 0, 0, 0]
        initial_parameters = obj.get_active_parameters()
        print(initial_parameters)
        engine = trajectory_calculation.PhysicsEngine(*initial_parameters, param)
        const = engine.constants
        engine.switch_engine(True, 100)
        engine.set_rocket_direction(0)

    engine.process_step()
    draw_everything(engine)

    # print(engine.rocket_parameters.parameters, engine.rocket_parameters.current_stage_mass)
    print(engine.rocket_parameters.engine_power)
    return obj, engine, const, flag


def rocket_controls(eve, turn, power):
    """
    Analyzing keyboard inputs and controlling the rocket
    :param eve: events
    :param turn: flag that shows whether right or left arrow was pressed
    :param power: flag that shows whether Shift(increase speed) or CTRL(reduce speed) was pressed
    :return:
    """
    if turn == "right":
        rocket.angle -= 0.5
    if turn == "left":
        rocket.angle += 0.5

    if (power == "increase") and (rocket_engine.rocket_parameters.engine_power < 100):
        rocket_engine.rocket_parameters.engine_power += 1
    if (power == "reduce") and (rocket_engine.rocket_parameters.engine_power > 0):
        rocket_engine.rocket_parameters.engine_power -= 1

    for inc in eve:
        if (turn == "right") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_RIGHT):
            turn = "None"
        if (turn == "left") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_LEFT):
            turn = "None"

        if (power == "increase") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_LSHIFT):
            power = "None"
        if (power == "reduce") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_LCTRL):
            power = "None"

        if inc.type == pygame.KEYDOWN:
            if inc.key == pygame.K_RIGHT:
                turn = "right"
                rocket.angle -= 0.5
            if inc.key == pygame.K_LEFT:
                turn = "left"
                rocket.angle += 0.5
            if inc.key == pygame.K_LSHIFT:
                if rocket_engine.rocket_parameters.engine_power < 100:
                    power = "increase"
                    rocket_engine.rocket_parameters.engine_power += 1
            if inc.key == pygame.K_LCTRL:
                if rocket_engine.rocket_parameters.engine_power > 0:
                    power = "reduce"
                    rocket_engine.rocket_parameters.engine_power -= 1

    rocket_engine.set_rocket_direction(trajectory_calculation.np.deg2rad(rocket.angle + 90))
    return turn, power


rocket_engine = None
constants = None

flag_turn = "None"
flag_power = "None"
while not finished:

    clock.tick(FPS)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    events = pygame.event.get()

    flag_menu = menu_type(flag_menu, rocket)

    if flag_menu == "play menu":
        #if seconds - flag_seconds >= 1/20:
        flag_seconds = seconds
        rocket, rocket_engine, constants, flag_turn = play_menu(rocket, rocket_engine, constants, flag_turn)

        flag_turn, flag_power = rocket_controls(events, flag_turn, flag_power)

    for event in events:
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
            if event.key == pygame.K_SPACE:
                flag_start = 1
    pygame.display.update()

pygame.quit()
