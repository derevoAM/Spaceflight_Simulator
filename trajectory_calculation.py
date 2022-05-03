# Calculating the trajectory of a rocket

import matplotlib.pyplot as plt
import numpy as np


class Constants:
    """
    Constants used throughout the script execution
    """

    def __init__(self):
        self.height_max = 9000  # высота в метрах, на которой плотность воздуха падает в е раз
        self.rho_max = 1.2  # плотность воздуха на высоте уровня моря
        self.area = 2.  # площадь КА
        self.C_coefficient = 0.4  # коэффициент аэродинамического сопротивления
        self.g_0 = 9.8  # ускорение свободного падения на уровне моря
        self.rad_Earth = 6.37e6  # радиус Земли (средний)
        self.mu_Earth = 4e14  # гравитационный параметр Земли
        self.mu_moon = 4.91e12  # гравитационный параметр Луны (гравитационная постоянная * масса)
        self.moon_rad = 3.85e8  # радиус орбиты Луны
        self.moon_period = 27.3 * 24 * 3600 / 2 / np.pi  # период обращения Луны вокруг Земли в с/рад
        self.fas_0 = 99 / 180 * np.pi  # начальная фаза Луны (которую нужно подогнать)


class Stage:
    """
    Rocket part class
    """

    def __init__(self, active_rocket_parameters):
        """
        Class initializer
        :param active_rocket_parameters:
        [initial_rocket_mass, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, fuel] array
        """
        self.current_stage_mass = active_rocket_parameters[0]  # масса ступени текущая
        self.gas_exhaust_speed = active_rocket_parameters[1]  # скорость истечения топлива
        self.fuel_consumption = active_rocket_parameters[2]  # расход топлива
        self.fuel_tank_capacity = active_rocket_parameters[3]
        self.fuel = active_rocket_parameters[4]

    def is_empty(self):
        """
        Secondary function
        :return: true if tank is empty, otherwise false
        """
        return self.fuel <= 0

    def reduce_mass(self, step):
        """
        Secondary function to reduce stage mass
        :param step: time step
        """
        if not self.is_empty():
            self.fuel -= self.fuel_consumption * step
            self.current_stage_mass -= self.fuel_consumption * step


def calc_rho(height, constants):
    """
    Calculating atmosphere rho
    :param height: height above the sea level
    :param constants: class of constants
    :return: rho
    """
    return constants.rho_max * np.exp(-height / constants.height_max)


def calc_moon_position(current_time, constants):
    """
    Calculating moon position in the particular moment of time
    :param current_time: global time
    :param constants: class of constants
    :return: array [x, y] of moon coordinates
    """
    return constants.moon_rad * np.array(
        [np.cos(constants.fas_0 + current_time / constants.moon_period),
         np.sin(constants.fas_0 + current_time / constants.moon_period)])


def calc_acceleration_air(stage_parameters, stage, position_norm, velocity_norm, constants):
    """
    Calculating air impact
    :param stage_parameters: [x, y, vx, vy] array consisting of rocket stage parameters
    :param stage: stage entity
    :param position_norm: the norm of vector earth-rocket
    :param velocity_norm: the norm of rocket speed
    :param constants: class of constants
    :return: [ax, ay] array consisting of acceleration values for each axis
    """
    if position_norm - constants.rad_Earth < 10 * constants.height_max:
        return - 0.5 * constants.C_coefficient * calc_rho(
            position_norm - constants.rad_Earth, constants) * constants.area * velocity_norm \
               * stage_parameters[2:] / stage.current_stage_mass
    else:
        return np.zeros(2)


def calc_acceleration_earth(stage_parameters, position_norm, constants):
    """
    Calculating gravitational acceleration by Earth
    :param stage_parameters: [x, y, vx, vy] array consisting of rocket stage parameters
    :param position_norm: the norm of vector earth-rocket
    :param constants: class of constants
    :return: [ax, ay] array consisting of acceleration values for each axis
    """
    return - constants.mu_Earth / position_norm ** 3 * stage_parameters[:2]


def calc_acceleration_engine(stage, velocity_norm, rocket_heading, engine_is_on_flag):
    """
    Calculating acceleration by engine working
    :param stage: stage entity
    :param velocity_norm: the norm of rocket speed
    :param rocket_heading: vector of rocket direction
    :param engine_is_on_flag: true if the engine is working
    :return: [ax, ay] array consisting of acceleration values for each axis
    """
    if engine_is_on_flag and not stage.is_empty():
        if velocity_norm > 1e-8:
            return stage.fuel_consumption * stage.gas_exhaust_speed / stage.current_stage_mass \
                   * rocket_heading
        else:
            return np.array([stage.fuel_consumption * stage.gas_exhaust_speed / stage.current_stage_mass, 0])
    else:
        return np.zeros(2)


def calc_acceleration_moon(stage_parameters, time, constants):
    """
    Calculating gravitational acceleration made by moon
    :param stage_parameters: [x, y, vx, vy] array consisting of rocket stage parameters
    :param time: global time
    :param constants: class of constants
    :return: [ax, ay] array consisting of acceleration values for each axis
    """
    rad_moon_ka = stage_parameters[:2] - calc_moon_position(time, constants)

    return - constants.mu_moon * rad_moon_ka / (np.linalg.norm(rad_moon_ka)) ** 3


def calc_acceleration(stage_parameters, stage, rocket_heading, engine_is_on_flag, time, constants):
    """
    Calculating final value of vehicle acceleration
    :param stage_parameters: [x, y, vx, vy] array consisting of rocket stage parameters
    :param stage: stage entity
    :param rocket_heading: vector of rocket direction
    :param engine_is_on_flag: true if the engine is working
    :param time: global time
    :param constants: class of constants
    :return: [ax, ay] array consisting of acceleration values for each axis
    """
    position_norm = np.linalg.norm(stage_parameters[:2])
    velocity_norm = np.linalg.norm(stage_parameters[2:])

    acceleration_air = calc_acceleration_air(stage_parameters, stage, position_norm, velocity_norm, constants)

    acceleration_gravity = calc_acceleration_earth(stage_parameters, position_norm, constants)

    acceleration_engine = calc_acceleration_engine(stage, velocity_norm, rocket_heading,
                                                   engine_is_on_flag)

    acceleration_moon = calc_acceleration_moon(stage_parameters, time, constants)

    return acceleration_air + acceleration_gravity + acceleration_engine + acceleration_moon


def calc_differential(stage_parameters, stage, rocket_heading, engine_is_on_flag, time, constants):
    """
    Calculating Runge-Kutta method differential
    :param stage_parameters: [x, y, vx, vy] array consisting of rocket stage parameters
    :param stage: stage entity
    :param rocket_heading: vector of rocket direction
    :param engine_is_on_flag: true if the engine is working
    :param time: global time
    :param constants: class of constants
    :return: [vx, vy, ax, ay] array
    """
    total_acceleration = calc_acceleration(stage_parameters, stage, rocket_heading, engine_is_on_flag, time, constants)

    return np.array([stage_parameters[2], stage_parameters[3], total_acceleration[0], total_acceleration[1]])


def calc_step(stage_parameters, step, stage, rocket_heading, engine_is_on_flag, time, constants):
    """
    Main function to calculate stage parameters for the next step
    :param stage_parameters: [x, y, vx, vy] array consisting of rocket stage parameters
    :param step: time step
    :param stage: stage entity
    :param rocket_heading: vector heading
    :param engine_is_on_flag: true if the engine is working
    :param time: global time
    :param constants : class of constants
    :return: array [new_x, new_y, new_vx, new_vy] for the next step
    """
    k_1 = calc_differential(stage_parameters, stage, rocket_heading, engine_is_on_flag, time, constants)
    k_2 = calc_differential(stage_parameters + 0.5 * step * k_1, stage, rocket_heading, engine_is_on_flag, time,
                            constants)
    k_3 = calc_differential(stage_parameters + 0.5 * step * k_2, stage, rocket_heading, engine_is_on_flag, time,
                            constants)
    k_4 = calc_differential(stage_parameters + step * k_3, stage, rocket_heading, engine_is_on_flag, time, constants)

    stage.reduce_mass(step)

    return stage_parameters + (k_1 + 2 * (k_2 + k_3) + k_4) * step / 6, time + step


################

def calc_differential_euler(predicative_stage_parameters, time, constants):
    """
    Function to calculate differential for predicative orbit parameters
    :param predicative_stage_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
    :param time: time used in predicative calculations
    :param constants: class of constants
    :return: predicative [vx, vy, ax, ay] array
    """
    total_acceleration = calc_acceleration_earth(predicative_stage_parameters,
                                                 np.linalg.norm(predicative_stage_parameters[:2]),
                                                 constants) + calc_acceleration_moon(predicative_stage_parameters, time,
                                                                                     constants)

    return np.array([predicative_stage_parameters[2], predicative_stage_parameters[3], total_acceleration[0],
                     total_acceleration[1]])


def calc_step_euler(predicative_stage_parameters, step, time, constants):
    """
    Function to process step using basic integration method
    :param predicative_stage_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
    :param step: step used for forecast
    :param time: time used in predicative calculations
    :param constants: class of constants
    :return: predicative [new_x, new_y, new_vx, new_vy] array
    """
    return predicative_stage_parameters + calc_differential_euler(predicative_stage_parameters, time,
                                                                  constants) * step, time + step


def calc_predicative_orbit(stage_parameters, step, time, constants):
    """
    Function to calculate predicative orbit
    :param stage_parameters: current stage parameters use for further orbit predication
    :param step: step used for forecast
    :param time: time used in predicative calculations
    :param constants: class of constants
    :return: array [[x, y, vx, vy], ...] consisting of predicative orbit points
    """
    log_size = 100
    time_array = np.zeros(log_size)
    time_array[0] = time
    predicative_orbit = np.ndarray(shape=(log_size, 4), dtype=float)
    predicative_orbit[0] = stage_parameters
    count = 0

    while count < log_size - 1:
        count += 1
        predicative_orbit[count], time_array[count] = calc_step_euler(predicative_orbit[count - 1], step,
                                                                      time_array[count - 1], constants)

    return predicative_orbit


size = 500000
const = Constants()

position_and_velocity_log = np.ndarray(shape=(size, 4), dtype=float)
predicative_orbit_log = np.ndarray(shape=(500, 4), dtype=float)
position_and_velocity_log[0] = np.array([const.rad_Earth, 0, 0, 0])  # основной массив (x, y, Vx, Vy)
time_log = np.ndarray(shape=(size,), dtype=float)  # текущее время расчета
step_time = 5  # шаг расчета
counter = 0  # счетчик

first_stage = Stage([80000, 4000, 300, 50000, 50000])  # параметры первой ступени
second_stage = Stage([first_stage.current_stage_mass - first_stage.fuel_tank_capacity, 3000, 200, 28000,
                      28000])  # параметры второй ступени
third_stage = Stage([second_stage.current_stage_mass - second_stage.fuel_tank_capacity, 265, 50, 1995,
                     1995])  # параметры третьей ступени

engine_is_on = True
heading = np.array([8, 2])
heading = heading / np.linalg.norm(heading)

while position_and_velocity_log[counter][2] >= 0:
    counter += 1
    position_and_velocity_log[counter], time_log[counter] = calc_step(position_and_velocity_log[counter - 1], step_time,
                                                                      first_stage,
                                                                      heading, engine_is_on, time_log[counter - 1],
                                                                      const)
    predicative_orbit_log = calc_predicative_orbit(position_and_velocity_log[counter - 1], 2 * step_time,
                                                   time_log[counter - 1], const)

heading = np.array([0, 1])
heading = heading / np.linalg.norm(heading)

while counter < 1000:
    counter += 1
    position_and_velocity_log[counter], time_log[counter] = calc_step(position_and_velocity_log[counter - 1], step_time,
                                                                      second_stage,
                                                                      heading, engine_is_on, time_log[counter - 1],
                                                                      const)

    predicative_orbit_log = calc_predicative_orbit(position_and_velocity_log[counter - 1], 5 * step_time,
                                                   time_log[counter - 1], const)

fig, ax = plt.subplots()
plt.axis('equal')
ax.add_patch(plt.Circle((0, 0), const.rad_Earth))
ax.plot(position_and_velocity_log[:counter, 0], position_and_velocity_log[:counter, 1], color="black", linewidth=4)
ax.plot(predicative_orbit_log[::, 0], predicative_orbit_log[::, 1])

plt.show()
