import matplotlib.pyplot as plt
import numpy as np
import pygame
import pygame.draw as dr

# import textures as t
import parts as p
# объявили экран, на котором будем рисовать
# rocket_image = pygame.Surface([ROCKETWINDOWWIDTH, ROCKETWINDOWHEIGHT], pygame.SRCALPHA)
import trajectory_calculation


# Этот файл просто возвращает холст с нарисованной ракетой


class Rocket:
    """
    Класс ракеты. Идея состоит в том, что ракета представляет собой виртуальный холст
    с нарисованными деталями в нужном порядке, который подаётся в основную программу
    и уже там с ним производятся манипуляции в виде сжатия, поворота и т п
    """

    def __init__(self):
        """
        Конструктор ракеты
        инициализирует поля, являющиеся характеристиками холста ракеты и для подсчёта траектории
        """
        self.grid_x = 30
        self.grid_y = 20
        self.block_x = 100
        self.block_y = 100
        self.width = self.grid_x * self.block_x
        self.height = self.grid_y * self.block_y
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.parts = []
        ##########
        self.active_stage = trajectory_calculation.Stage(self.get_active_parameters())
        self.parameters = np.array([0.0, 0, 0, 0])
        self.direction = np.array([1.0, 0])
        self.predicative_orbit = np.ndarray(shape=(100, 4), dtype=float)

    def activate_stage(self):
        """
        перерассчитывает текущие параметры ракеты (ступени)
        """
        self.active_stage = trajectory_calculation.Stage(self.get_active_parameters())

    def activate_all(self):
        """
        Активирует все составляющие ракеты
        """
        for part in self.parts:
            part.active = True

    def get_active_parameters(self):
        """
        Функция возвращает параметры ракеты в текущий момент как сумму соответствующих параметров деталей
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

        return initial_mass, exhaust_speed, fuel_consumption, capacity, fuel

    ###################
    def add_part(self, part_entity):
        """
        Добавление детали в ракету
        part_entity - объкт классаа Entity
        """
        part_entity.surface = self.surface
        self.parts.append(part_entity)
        part_entity.draw()

    def recount(self):
        """
        Эта функция двигает составляющие ракеты так, чтобы ракета касалась верха окна и левой его стенки
        Вот это надо делать всегда после изменения составляющих ракеты
        После этого слетит сетка, но зато избавимся от копий деталей
        Операция жрёт время (потенциально)
        """
        x_min = self.width
        y_min = self.width
        for part_entity in self.parts:
            if part_entity.x < x_min:
                x_min = part_entity.x
            if part_entity.y < y_min:
                y_min = part_entity.y
        for part_entity in self.parts:
            part_entity.x -= x_min
            part_entity.y -= y_min
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        for part_entity in self.parts:
            part_entity.surface = self.surface
            part_entity.draw()

    def get_surface(self):
        """
        Просто возвращает холст с ракетой
        """
        return self.surface

    def draw_grid(self):
        """
        рисует сетку с шагом grid_x по оси х и grid_y по оси y
        """
        grey = (125, 125, 125)
        for i in range(self.block_x + 1):
            dr.line(self.surface, grey, (i * self.grid_x, 0), (i * self.grid_x, self.height))
        for j in range(self.block_y + 1):
            dr.line(self.surface, grey, (0, j * self.grid_y), (self.width, j * self.grid_y))

    def draw(self, gridded=0):
        """
        Просто отрисовывает все составляющие ракеты на её экране
        gridded отвечает за сетку на экране (ри True - рисует, при false - иначе)
        """
        if gridded:
            self.draw_grid()
        for part_entity in self.parts:
            part_entity.draw()


def load_rocket(sourcefile):
    """
    Читает составляющие ракеты из файла, строит ракету и возвращает готовый объект
    sourcefile - Путь к файлу, где записана ракета
    """
    rocket_entity = Rocket()
    with open(sourcefile, "r") as f:
        part_lines = f.readlines()
    for part_line in part_lines:
        part_line_array = part_line.split()
        part_type = part_line_array[0]
        print(part_type, part_line_array[1], part_line_array[2])
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
    Сохраняет ракету в файл
    rocket_entity - объект класса Rocket
    outfile - путь к файлу сохранения
    """
    with open(outfile, "w") as file:
        for part_entity in rocket_entity.parts:
            file.write(str(part_entity.type) + " " + str(part_entity.x) + " " + str(part_entity.y) + "\n")


'''
screen = pygame.display.set_mode((900, 900))
engine = p.Engine(0, x = 4, y = 140)
r = load_rocket("rockets/test.txt")
save_rocket(r, "rockets/test_save.txt")
#r.add_part(engine)
#r.recount()
r.draw(gridded=0)
screen.blit(r.get_surface(), dest=[0,0])
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()'''

## Тестирую на совместимость!

constants = trajectory_calculation.Constants()

rocket = load_rocket("rockets/test.txt")

rocket.parameters = np.array([constants.rad_Earth, 0, 0, 0])

rocket.activate_all()

rocket.activate_stage()

rocket.active_stage = trajectory_calculation.Stage([80000, 4000, 300, 50000, 50000])

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

rocket.active_stage = trajectory_calculation.Stage([30000, 3000, 200, 28000, 28000])

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
