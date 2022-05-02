# Calculating the trajectory of a rocket

import matplotlib.pyplot as plt
import numpy as np


class Constants:

    def __init__(self):
        self.height_max = 9000  # высота в метрах, на которой плотность воздуха падает в е раз
        self.rho_max = 1.2  # плотность воздуха на высоте уровня моря
        self.area = 2.  # площадь КА
        self.C_coefficient = 0.4  # коэффициент аэродинамического сопротивления
        self.g_0 = 9.8  # ускорение свободного падения на уровне моря
        self.rad_Earth = 6.37e6  # радиус Земли (средний)
        self.mu_Earth = 4e14
        self.mu_moon = 4.91e12  # гравитационный параметр Луны (гравитационная постоянная * масса)
        self.moon_rad = 3.85e8  # радиус орбиты Луны
        self.moon_period = 27.3 * 24 * 3600 / 2 / np.pi  # период обращения Луны вокруг Земли в с/рад
        self.fas_0 = 99 / 180 * np.pi  # начальная фаза Луны (которую нужно подогнать)


class Stage:
    """
    Rocket part class
    """

    def __init__(self, payload_mass, current_stage_mass, gas_exhaust_speed, fuel_consumption):
        self.payload_mass = payload_mass  # полезная нагрузка
        self.current_stage_mass = current_stage_mass  # масса ступени текущая
        self.gas_exhaust_speed = gas_exhaust_speed  # скорость истечения топлива
        self.fuel_consumption = fuel_consumption  # расход топлива

    def is_empty(self):
        return self.current_stage_mass <= self.payload_mass


def calc_rho(height, constants):
    """ вычисляет плотность воздуха на высоте height от Земли """
    return constants.rho_max * np.exp(-height / constants.height_max)


def calc_moon_position(current_time, constants):
    return constants.moon_rad * np.array(
        [np.cos(constants.fas_0 + current_time / constants.moon_period),
         np.sin(constants.fas_0 + current_time / constants.moon_period)])


def calc_acceleration_air(stage_parameters, stage, position_norm, velocity_norm, constants):
    if position_norm - constants.rad_Earth < 10 * constants.height_max:
        return - 0.5 * constants.C_coefficient * calc_rho(
            position_norm - constants.rad_Earth, constants) * constants.area * velocity_norm \
               * stage_parameters[2:] / stage.current_stage_mass
    else:
        return np.zeros(2)


def calc_acceleration_earth(stage_parameters, position_norm, constants):
    return - constants.mu_Earth / position_norm ** 3 * stage_parameters[:2]


def calc_acceleration_engine(stage, velocity_norm, rocket_heading, engine_is_on_flag):
    if engine_is_on_flag and not stage.is_empty():
        if velocity_norm > 1e-8:
            return stage.fuel_consumption * stage.gas_exhaust_speed / stage.current_stage_mass \
                   * rocket_heading
        else:
            return np.array([stage.fuel_consumption * stage.gas_exhaust_speed / stage.current_stage_mass, 0])
    else:
        return np.zeros(2)


def calc_acceleration_moon(stage_parameters, constants):
    rad_moon_ka = stage_parameters[:2] - calc_moon_position(time_log[counter], constants)

    return - constants.mu_moon * rad_moon_ka / (np.linalg.norm(rad_moon_ka)) ** 3


def calc_acceleration(stage_parameters, stage, rocket_heading, engine_is_on_flag, constants):
    """
    считает ускорение КА
    :param stage_parameters: массив (x, y, Vx, Vy)
    :param stage: параметры ступени
    :param rocket_heading: angle of the rocket
    :param engine_is_on_flag: включен ли двигатель
    :param constants: constants
    :return: массив (ax, ay)
    """
    position_norm = np.linalg.norm(stage_parameters[:2])
    velocity_norm = np.linalg.norm(stage_parameters[2:])

    acceleration_air = calc_acceleration_air(stage_parameters, stage, position_norm, velocity_norm, constants)

    acceleration_gravity = calc_acceleration_earth(stage_parameters, position_norm, constants)

    acceleration_engine = calc_acceleration_engine(stage, velocity_norm, rocket_heading,
                                                   engine_is_on_flag)

    acceleration_moon = calc_acceleration_moon(stage_parameters, constants)

    return acceleration_air + acceleration_gravity + acceleration_engine + acceleration_moon


def calc_differential(stage_parameters, stage, rocket_heading, engine_is_on_flag, constants):
    """ вычисляет дифференциал функции (промежутчная функция метода Рунге-Кутта) """
    total_acceleration = calc_acceleration(stage_parameters, stage, rocket_heading, engine_is_on_flag, constants)

    return np.array([stage_parameters[2], stage_parameters[3], total_acceleration[0], total_acceleration[1]])


def reduce_stage_mass(stage, step):
    if stage.current_stage_mass > stage.payload_mass:
        stage.current_stage_mass -= stage.fuel_consumption * step


def calc_step(stage_parameters, step, stage, rocket_heading, engine_is_on_flag, constants):
    """
    основная функция расчета шага
    :param stage_parameters: массив (x, y, Vx, Vy) на предыдущем шаге
    :param step: время одного шага
    :param stage: параметры ступени
    :param rocket_heading: vector heading
    :param engine_is_on_flag: включен ли двигатель
    :param constants : const
    :return: массив (x, y, Vx, Vy) на текущем шаге
    """
    k_1 = calc_differential(stage_parameters, stage, rocket_heading, engine_is_on_flag, constants)
    k_2 = calc_differential(stage_parameters + 0.5 * step * k_1, stage, rocket_heading, engine_is_on_flag, constants)
    k_3 = calc_differential(stage_parameters + 0.5 * step * k_2, stage, rocket_heading, engine_is_on_flag, constants)
    k_4 = calc_differential(stage_parameters + step * k_3, stage, rocket_heading, engine_is_on_flag, constants)

    reduce_stage_mass(stage, step)

    return stage_parameters + (k_1 + 2 * (k_2 + k_3) + k_4) * step / 6


def calc_differential_euler(predicative_stage_parameters, constants):
    total_acceleration = calc_acceleration_earth(predicative_stage_parameters,
                                                 np.linalg.norm(predicative_stage_parameters[:2]),
                                                 constants) + calc_acceleration_moon(predicative_stage_parameters,
                                                                                     constants)

    return np.array([predicative_stage_parameters[2], predicative_stage_parameters[3], total_acceleration[0],
                     total_acceleration[1]])


def calc_step_euler(predicative_stage_parameters, step, constants):
    return predicative_stage_parameters + calc_differential_euler(predicative_stage_parameters, constants) * step


def calc_predicative_orbit(stage_parameters, step, constants):
    log_size = 500
    predicative_orbit = np.ndarray(shape=(log_size, 4), dtype=float)
    predicative_orbit[0] = stage_parameters
    count = 0

    while count < log_size - 1:
        count += 1
        predicative_orbit[count] = calc_step_euler(predicative_orbit[count - 1], step, constants)

    return predicative_orbit


size = 500000
const = Constants()

position_and_velocity_log = np.ndarray(shape=(size, 4), dtype=float)
predicative_orbit_log = np.ndarray(shape=(500, 4), dtype=float)
position_and_velocity_log[0] = np.array([const.rad_Earth, 0, 0, 0])  # основной массив (x, y, Vx, Vy)
time_log = np.ndarray(shape=(size,), dtype=float)  # текущее время расчета
step_time = 5  # шаг расчета
counter = 0  # счетчик

first_stage = Stage(30000, 80000, 4000, 300)  # параметры первой ступени
second_stage = Stage(2000, first_stage.payload_mass, 3000, 200)  # параметры второй ступени
third_stage = Stage(5, second_stage.payload_mass, 265, 50)  # параметры третьей ступени

engine_is_on = True
heading = np.array([8, 2])
heading = heading / np.linalg.norm(heading)

while position_and_velocity_log[counter][2] >= 0:
    counter += 1
    position_and_velocity_log[counter] = calc_step(position_and_velocity_log[counter - 1], step_time, first_stage,
                                                   heading, engine_is_on, const)
    predicative_orbit_log = calc_predicative_orbit(position_and_velocity_log[counter - 1], 1.5 * step_time, const)

    time_log[counter] = time_log[counter - 1] + step_time

heading = np.array([0, 1])
heading = heading / np.linalg.norm(heading)

while counter < 1000:
    counter += 1
    position_and_velocity_log[counter] = calc_step(position_and_velocity_log[counter - 1], step_time, second_stage,
                                                   heading, engine_is_on, const)

    predicative_orbit_log = calc_predicative_orbit(position_and_velocity_log[counter - 1], 1.5 * step_time, const)

    time_log[counter] = time_log[counter - 1] + step_time


fig, ax = plt.subplots()
plt.axis('equal')
ax.add_patch(plt.Circle((0, 0), const.rad_Earth))
ax.plot(position_and_velocity_log[:counter, 0], position_and_velocity_log[:counter, 1], color="black", linewidth=4)
ax.plot(predicative_orbit_log[::, 0], predicative_orbit_log[::, 1])

plt.show()
