import sandbox_menu
import sandbox
import main_menu
import draw_screen
import pygame
import trajectory_calculation

pygame.init()
FPS = 20
clock = pygame.time.Clock()
finished = False
start_ticks = pygame.time.get_ticks()
flag_start = 0
flag_menu = "main menu"

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.update()
window_width, window_height = pygame.display.get_surface().get_size()

rocket = sandbox.Rocket()

Rocket_surface = draw_screen.RocketView(window_width, window_height, rocket)
Space_surface = draw_screen.SpaceView(window_width, window_height, rocket)
Parameters_surface = draw_screen.ParametersView(window_width, window_height, rocket)
Views = [Rocket_surface, Space_surface, Parameters_surface]

rocket_engine = None

flag_turn = "None"
flag_power = "None"
part_size = ["engine", 0]


def draw_everything(engine):
    """
    Drawing play menu, which include 3 views
    :param engine: object of class PhysicsEngine from trajectory_calculation
    """
    for view in Views:
        view.set_engine(engine)
        view.draw()
        window.blit(view.surface, (view.x, view.y))


def menu_type(flag, obj, part_type):
    """
    Function, that determines which menu to show. If flag = main menu or sandbox menu, required menu is shown
    :param flag: type of menu: main menu, sandbox menu, play menu
    :param obj: rocket
    :param part_type: array of a part of a rocket, which is being selected in this particular moment, and its width
    :return: flag, part_type
    """
    if flag == "main menu":
        flag = main_menu.main_menu(window, flag)
    elif flag == "sandbox menu":
        flag, obj, part_type = sandbox_menu.sandbox(window, flag, window_width, window_height, obj, events, part_type)

    return flag, part_type


def play_menu(obj, engine, start):
    """
    Function, which initializes, processes rocket parameters and calculate new step
    :param obj: object of class Rocket from sandbox
    :param engine: object of class PhysicsEngine from trajectory_calculation
    :param start: flag, that shows whether rocket was launched
    :return: obj, engine
    """
    if engine is None:
        param = [6.37e6, 0, 0, 0]
        initial_parameters = obj.get_active_parameters()
        engine = trajectory_calculation.PhysicsEngine(*initial_parameters, param)
        engine.switch_engine(True, 0)
        engine.set_rocket_direction(0)

    if start == 1:
        engine.process_step()

    draw_everything(engine)

    return obj, engine


def rocket_direction(eve, turn, engine):
    """
        Analyzing keyboard inputs and controlling rocket direction
        :param eve: events
        :param turn: flag that shows whether right or left arrow was pressed
        :param engine: object of class PhysicsEngine from trajectory_calculation
        :return: turn, engine
        """
    if turn == "right":
        rocket.angle -= 1
    if turn == "left":
        rocket.angle += 1

    for inc in eve:
        if (turn == "right") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_RIGHT):
            turn = "None"
        if (turn == "left") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_LEFT):
            turn = "None"

        if inc.type == pygame.KEYDOWN:
            if inc.key == pygame.K_RIGHT:
                turn = "right"
                rocket.angle -= 1
            if inc.key == pygame.K_LEFT:
                turn = "left"
                rocket.angle += 1

    engine.set_rocket_direction(trajectory_calculation.np.deg2rad(rocket.angle + 90))
    return turn, engine


def rocket_power(eve, power):
    """
    Analyzing keyboard inputs and controlling rocket power
    :param eve: events
    :param power: flag that shows whether Shift(increase speed) or CTRL(reduce speed) was pressed
    """
    if (power == "increase") and (rocket_engine.rocket_parameters.engine_power < 100):
        rocket_engine.rocket_parameters.engine_power += 2
    if (power == "reduce") and (rocket_engine.rocket_parameters.engine_power > 0):
        rocket_engine.rocket_parameters.engine_power -= 2

    for inc in eve:
        if (power == "increase") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_LSHIFT):
            power = "None"
        if (power == "reduce") and (inc.type == pygame.KEYUP) and (inc.key == pygame.K_LCTRL):
            power = "None"

        if inc.type == pygame.KEYDOWN:
            if inc.key == pygame.K_LSHIFT:
                if rocket_engine.rocket_parameters.engine_power < 100:
                    power = "increase"
                    rocket_engine.rocket_parameters.engine_power += 2
            if inc.key == pygame.K_LCTRL:
                if rocket_engine.rocket_parameters.engine_power > 0:
                    power = "reduce"
                    rocket_engine.rocket_parameters.engine_power -= 2

    return power


def displaying_menu(menu, part_type, obj, engine, start, turn, power, eve, finish):
    """
    Function, which is responsible for everything related to menus
    :param menu: type of menu: main menu, sandbox menu, play menu
    :param part_type: array of a part of a rocket, which is being selected in this particular moment, and its width
    :param obj:  object of class Rocket from sandbox
    :param engine: object of class PhysicsEngine from trajectory_calculation
    :param start: flag that shows whether rocket was launched
    :param turn: flag that shows whether right or left arrow was pressed
    :param power: flag that shows whether Shift(increase speed) or CTRL(reduce speed) was pressed
    :param eve: events
    :param finish: finished flag
    :return: menu, part_type, obj, engine, start, turn, power, finish
    """
    menu, part_type = menu_type(menu, obj, part_type)

    if menu == "play menu":
        obj, engine = play_menu(obj, engine, start)
        if engine.rocket_parameters.collision_flag:
            finish = True
        else:
            turn, engine = rocket_direction(eve, turn, engine)
            power = rocket_power(eve, power)

    return menu, part_type, obj, engine, start, turn, power, finish


while not finished:
    clock.tick(FPS)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    events = pygame.event.get()

    flag_menu, part_size, rocket, rocket_engine, flag_start, flag_turn, flag_power, finished = displaying_menu(
        flag_menu,
        part_size, rocket,
        rocket_engine,
        flag_start,
        flag_turn,
        flag_power, events, finished)

    for event in events:
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True
            if event.key == pygame.K_SPACE and flag_menu == "play menu":
                flag_start = 1
    pygame.display.update()

pygame.quit()
