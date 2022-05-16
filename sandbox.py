import matplotlib.pyplot as plt
import numpy as np
import pygame
import parts as p
import trajectory_calculation


# Этот файл просто возвращает холст с нарисованной ракетой

class Rocket:
    """
    Rocket class. Has an aray of parts, physical engine and a canvas, which as a drawn rocket on it
    """

    def __init__(self):
        """
        constructor
        initializes characteristics
        """
        self.width = 100
        self.height = 800
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.angle = -90
        self.parts = []

        self.physics_engine = None

    def activate_stage(self):
        """
        recounts rocket parameters
        """
        self.physics_engine = trajectory_calculation.PhysicsEngine(5, *self.get_active_parameters())

    def activate_all(self):
        """
        activates all rocket parts
        """
        for part in self.parts:
            part.active = True

    def get_active_parameters(self):
        """
        returns characteristics of the rocket as a sum of the part's characteristics
        """
        initial_mass = 0
        exhaust_speed = 0
        fuel_consumption = 0
        capacity = 0
        fuel = 0

        for part in self.parts:
            initial_mass += part.mass
            if part.type == "fueltank" and part.active:
                capacity += part.capacity
                fuel += part.capacity * part.fullness

            elif part.type == "engine" and part.active:
                exhaust_speed = part.output * part.power
                fuel_consumption = part.output * part.consumption

        return [initial_mass, exhaust_speed, fuel_consumption, capacity, fuel]

    ###################
    def add_part(self, part_entity):
        """
        adding part to the rocket
        part_entity - Entity class object
        """
        part_entity.surface = self.surface
        self.parts.append(part_entity)
        part_entity.draw()

    def recount(self):
        """
        This function builds rocket from it's parts array.
        It makes rocket parts to follow the order from up to down:
        capsule, fueltanks, engine
        """
        fuel_tanks_y = [0]
        cabin_height = 0
        part_counter = 0
        for part_entity in self.parts:
            if part_entity.type == "fueltank":
                fuel_tanks_y.append(fuel_tanks_y[-1] + part_entity.texture.get_height())
            elif part_entity.type == "cabin":
                cabin_height = part_entity.texture.get_height()
        for part_entity in self.parts:
            if part_entity.type == "fueltank":
                part_entity.y = cabin_height + fuel_tanks_y[part_counter]
                part_counter += 1
            elif part_entity.type == "engine":
                part_entity.y = cabin_height + fuel_tanks_y[-1]
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        for part_entity in self.parts:
            part_entity.surface = self.surface
            part_entity.draw()

    def get_surface(self):
        """
        returns canvas with the drawn rocket on it
        """
        return self.surface

    def draw(self):
        """
        draws rocket on it's canvas
        """
        for part_entity in self.parts:
            part_entity.draw()


def load_rocket(sourcefile):
    """
    loads rocket from the file
    sourcefile - path to the file with rocket
    """
    rocket_entity = Rocket()
    with open(sourcefile, "r") as f:
        part_lines = f.readlines()
    for part_line in part_lines:
        part_line_array = part_line.split()
        part_type = part_line_array[0]
        print(part_type, part_line_array[1], part_line_array[2])
        part_entity = None
        if part_type == "engine":
            # А другие параметры не волнуют, ракету мы загружаем только при старте
            part_entity = p.Engine(0, x=int(part_line_array[1]), y=int(part_line_array[2]))
        elif part_type == "fueltank":
            part_entity = p.FuelTank(0, x=int(part_line_array[1]), y=int(part_line_array[2]))
        elif part_type == "cabin":
            part_entity = p.Cabin(0, x=int(part_line_array[1]), y=int(part_line_array[2]))
        rocket_entity.add_part(part_entity)
    return rocket_entity


def save_rocket(rocket_entity, outfile):
    """
    saves the rocket to the file
    rocket_entity - Rocket class object
    outfile - path to the file
    """
    with open(outfile, "w") as file:
        for part_entity in rocket_entity.parts:
            file.write(str(part_entity.type) + " " + str(part_entity.x) + " " + str(part_entity.y) + "\n")


## Тестирую на совместимость!

if __name__ == "__main__":
    screen = pygame.display.set_mode((900, 900))
    r = Rocket()
    engine1 = p.Engine(0)
    engine1.texture = pygame.image.load("textures/engines/big_engine_100x75.png")
    fueltank1 = p.FuelTank(0)
    fueltank1.texture = pygame.image.load("textures/tanks/tank_simple_50x75.png")
    fueltank2 = p.FuelTank(0)
    fueltank2.texture = pygame.image.load("textures/tanks/tank_simple_50x75.png")
    fueltank3 = p.FuelTank(0)
    fueltank3.texture = pygame.image.load("textures/tanks/tank_simple_50x75.png")
    r.add_part(fueltank1)
    r.add_part(fueltank2)
    r.add_part(fueltank3)
    r.add_part(engine1)
    capsule = p.Cabin(0)
    capsule.texture = pygame.image.load("textures/capsule/capsule_60x40.png")
    r.add_part(capsule)
    screen.blit(r.surface, dest=[400, 0])
    r.recount()
    screen.blit(r.surface, dest=[0, 0])

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

    pygame.quit()

    '''
    constants = trajectory_calculation.Constants()

    rocket = load_rocket("rockets/test.txt")

    rocket.parameters = np.array([constants.rad_Earth, 0, 0, 0])

    rocket.activate_all()

    rocket.activate_stage()

    rocket.active_stage = trajectory_calculation.MechanicalParameters([80000, 4000, 300, 50000, 50000])

    size = 500000
    const = trajectory_calculation.Constants()

    position_and_velocity_log = np.ndarray(shape=(size, 4), dtype=float)

    predicative_orbit_log = np.ndarray(shape=(500, 4), dtype=float)
    position_and_velocity_log[0] = np.array([const.rad_Earth, 0, 0, 0])  # основной массив (x, y, Vx, Vy)
    time_log = np.ndarray(shape=(size,), dtype=float)  # текущее время расчета
    step_time = 5  # шаг расчета
    counter = 0  # счетчик

    engine_is_on = True
    heading = np.array([8, 2])
    heading = heading / np.linalg.norm(heading)
    rocket.direction = heading

    while position_and_velocity_log[counter][2] >= 0:
        counter += 1
        """position_and_velocity_log[counter], time_log[counter] = trajectory_calculation.calc_step(
            position_and_velocity_log[counter - 1], step_time,
            rocket.active_stage,
            heading, engine_is_on, time_log[counter - 1],
            const)"""
        position_and_velocity_log[counter] = rocket.parameters
        trajectory_calculation.process_step(rocket, step_time, engine_is_on, time_log[counter], constants)
        predicative_orbit_log = rocket.predicative_orbit

    heading = np.array([0, 1])
    heading = heading / np.linalg.norm(heading)
    rocket.direction = heading

    rocket.active_stage = trajectory_calculation.MechanicalParameters([30000, 3000, 200, 28000, 28000])

    while counter < 1000:
        counter += 1
        position_and_velocity_log[counter] = rocket.parameters
        trajectory_calculation.process_step(rocket, step_time, engine_is_on, time_log[counter], constants)
        predicative_orbit_log = rocket.predicative_orbit

    fig, ax = plt.subplots()
    plt.axis('equal')
    ax.add_patch(plt.Circle((0, 0), const.rad_Earth))
    ax.plot(position_and_velocity_log[:counter, 0], position_and_velocity_log[:counter, 1], color="black", linewidth=4)
    ax.plot(predicative_orbit_log[::, 0], predicative_orbit_log[::, 1])

    plt.show()
    '''
