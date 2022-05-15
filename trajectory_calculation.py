# Calculating the trajectory of a rocket

import matplotlib.pyplot as plt
import numpy as np


class Constants:
    """
    Constants used throughout the script execution
    """

    def __init__(self, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity):
        self.height_max = 9000  # высота в метрах, на которой плотность воздуха падает в е раз
        self.rho_max = 1.2  # плотность воздуха на высоте уровня моря
        self.area = 2.  # площадь КА
        self.C_coefficient = 0.4  # коэффициент аэродинамического сопротивления
        self.rad_Earth = 6.37e6  # радиус Земли (средний)
        self.rad_Moon = 1.74e6
        self.mu_Earth = 4e14  # гравитационный параметр Земли
        self.mu_moon = 4.91e12  # гравитационный параметр Луны (гравитационная постоянная * масса)
        self.moon_rad = 3.85e8  # радиус орбиты Луны
        self.moon_period = 27.3 * 24 * 3600 / 2 / np.pi  # период обращения Луны вокруг Земли в с/рад
        self.initial_fas = 99 / 180 * np.pi  # начальная фаза Луны (которую нужно подогнать)
        self.log_size = 300

        self.gas_exhaust_speed = gas_exhaust_speed  # скорость истечения топлива
        self.fuel_consumption = fuel_consumption  # расход топлива
        self.fuel_tank_capacity = fuel_tank_capacity

        self.step = 5


class RocketParameters:

    def __init__(self, initial_parameters, initial_rocket_mass, fuel):
        self.parameters = np.array(initial_parameters)
        self.direction = np.array([1, 0])
        self.current_time = 0.0
        self.predicative_orbit = np.ndarray(shape=(100, 4), dtype=float)

        self.current_stage_mass = initial_rocket_mass  # масса ступени текущая
        self.fuel_remained = fuel
        self.engine_power = 1.0

        self.engine_is_on_flag = True
        self.collision_flag = False

    def is_empty(self):
        return self.fuel_remained <= 0


class PhysicsEngine:

    def __init__(self, initial_rocket_mass, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, fuel,
                 initial_parameters):
        self.constants = Constants(gas_exhaust_speed, fuel_consumption, fuel_tank_capacity)
        self.rocket_parameters = RocketParameters(initial_parameters, initial_rocket_mass, fuel)

    def set_predicative_orbit_log_size(self, new_size):
        self.constants.log_size = new_size

    def set_parameters(self, new_parameters):
        self.rocket_parameters.parameters = new_parameters

    def set_rocket_direction(self, angle):
        self.rocket_parameters.direction = np.array([np.cos(angle), np.sin(angle)])

    def turn_rocket(self, angle):
        """
        Changing rocket angle
        :param angle: angle of rotation in radians, can be either positive or negative (positive angle refers to turning
        rocket
        counterclockwise)
        """
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        self.rocket_parameters.direction = np.dot(rotation_matrix, self.rocket_parameters.direction)

    def reduce_mass(self):
        if self.rocket_parameters.engine_is_on_flag and not self.rocket_parameters.is_empty():
            self.rocket_parameters.current_stage_mass -= self.rocket_parameters.engine_power * self.constants.step * \
                                                         self.constants.fuel_consumption
            self.rocket_parameters.fuel_remained -= self.rocket_parameters.engine_power * self.constants.step * self.constants.fuel_consumption

    def switch_engine(self, flag, power=1.0):
        self.rocket_parameters.engine_is_on_flag = flag
        self.rocket_parameters.engine_power = power

    def detect_collision(self):
        """
        Function to detect collision with Earth and Moon
        """
        if np.linalg.norm(self.rocket_parameters.parameters[:2]) < self.constants.rad_Earth or np.linalg.norm(
                self.rocket_parameters.parameters[:2] - self.calc_moon_position(
                    self.rocket_parameters.current_time)) < self.constants.rad_Moon:
            self.rocket_parameters.collision_flag = True

    def calc_rho(self, position_norm):
        """
        Calculating atmosphere rho
        :param position_norm: height above the sea level
        :return: rho
        """
        return self.constants.rho_max * np.exp(-position_norm / self.constants.height_max)

    def calc_moon_position(self, time):
        """
        Calculating moon position in the particular moment of time
        :param time: time of calculation
        :return: array [x, y] of moon coordinates
        """
        return self.constants.moon_rad * np.array(
            [np.cos(self.constants.initial_fas + time / self.constants.moon_period),
             np.sin(self.constants.initial_fas + time / self.constants.moon_period)])

    def calc_acceleration_air(self, parameters, position_norm, velocity_norm):
        """
        Calculating air impact
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param position_norm: the norm of vector earth-rocket
        :param velocity_norm: the norm of rocket speed
        :return: [ax, ay] array consisting of acceleration values for each axis
        """

        if position_norm - self.constants.rad_Earth < 10 * self.constants.height_max:
            return - 0.5 * self.constants.C_coefficient * self.calc_rho(
                position_norm - self.constants.rad_Earth) * self.constants.area * velocity_norm \
                   * parameters[2:] / self.rocket_parameters.current_stage_mass
        else:
            return np.zeros(2)

    def calc_acceleration_earth(self, parameters, position_norm):
        """
        Calculating gravitational acceleration by Earth
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param position_norm: the norm of vector earth-rocket
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        return - self.constants.mu_Earth / position_norm ** 3 * parameters[:2]

    def calc_acceleration_engine(self, velocity_norm):
        """
        Calculating acceleration by engine working
        :param velocity_norm: the norm of rocket speed
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        if self.rocket_parameters.engine_is_on_flag and not self.rocket_parameters.is_empty():
            if velocity_norm > 1e-8:
                return self.rocket_parameters.engine_power * self.constants.fuel_consumption * self.constants.gas_exhaust_speed / self.rocket_parameters.current_stage_mass \
                       * self.rocket_parameters.direction
            else:
                return np.array([self.rocket_parameters.parameters *
                                 self.constants.fuel_consumption * self.constants.gas_exhaust_speed / self.rocket_parameters.current_stage_mass,
                                 0])
        else:
            return np.zeros(2)

    def calc_acceleration_moon(self, parameters, time):
        """
        Calculating gravitational acceleration made by moon
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: global time
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        rad_moon_ka = parameters[:2] - self.calc_moon_position(time)

        return - self.constants.mu_moon * rad_moon_ka / (np.linalg.norm(rad_moon_ka)) ** 3

    def calc_acceleration(self, parameters, time):
        """
        Calculating final value of vehicle acceleration
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: global time
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        position_norm = np.linalg.norm(parameters[:2])
        velocity_norm = np.linalg.norm(parameters[2:])

        acceleration_air = self.calc_acceleration_air(parameters, position_norm, velocity_norm)

        acceleration_gravity = self.calc_acceleration_earth(parameters, position_norm)

        acceleration_engine = self.calc_acceleration_engine(velocity_norm)

        acceleration_moon = self.calc_acceleration_moon(parameters, time)

        return acceleration_air + acceleration_gravity + acceleration_engine + acceleration_moon

    def calc_differential(self, parameters, time):
        """
        Calculating Runge-Kutta method differential
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: global time
        :return: [vx, vy, ax, ay] array
        """
        total_acceleration = self.calc_acceleration(parameters, time)

        return np.array([parameters[2], parameters[3], total_acceleration[0], total_acceleration[1]])

    def calc_step(self):
        """
        Main function to calculate stage parameters for the next step
        :return: array [new_x, new_y, new_vx, new_vy] for the next step
        """
        k_1 = self.calc_differential(self.rocket_parameters.parameters, self.rocket_parameters.current_time)
        k_2 = self.calc_differential(self.rocket_parameters.parameters + 0.5 * self.constants.step * k_1,
                                     self.rocket_parameters.current_time + 0.5 * self.constants.step)
        k_3 = self.calc_differential(self.rocket_parameters.parameters + 0.5 * self.constants.step * k_2,
                                     self.rocket_parameters.current_time + 0.5 * self.constants.step)
        k_4 = self.calc_differential(self.rocket_parameters.parameters + self.constants.step * k_3,
                                     self.rocket_parameters.current_time + 0.5 * self.constants.step)

        self.reduce_mass()

        self.rocket_parameters.parameters += (k_1 + 2 * (k_2 + k_3) + k_4) * self.constants.step / 6
        self.rocket_parameters.current_time += self.constants.step

    def calc_differential_euler(self, predicative_parameters, time):
        """
        Function to calculate differential for predicative orbit parameters
        :param predicative_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: time used in predicative calculations
        :return: predicative [vx, vy, ax, ay] array
        """
        total_acceleration = self.calc_acceleration_earth(predicative_parameters, np.linalg.norm(
            predicative_parameters[:2])) + self.calc_acceleration_moon(predicative_parameters, time)

        return np.array([predicative_parameters[2], predicative_parameters[3], total_acceleration[0],
                         total_acceleration[1]])

    def calc_step_euler(self, predicative_parameters, time):
        """
        Function to process step using basic integration method
        :param predicative_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: time used in predicative calculations
        :return: predicative [new_x, new_y, new_vx, new_vy] array
        """
        return predicative_parameters + self.calc_differential_euler(predicative_parameters,
                                                                     time) * self.constants.step * 5, time + self.constants.step * 5

    def calc_predicative_orbit(self):
        """
        Function to calculate predicative orbit
        :return: array [[x, y, vx, vy], ...] consisting of predicative orbit points
        """
        log_size = self.constants.log_size
        time_array = np.zeros(log_size)
        time_array[0] = self.rocket_parameters.current_time
        predicative_orbit = np.ndarray(shape=(log_size, 4), dtype=float)
        predicative_orbit[0] = self.rocket_parameters.parameters
        count = 0

        while count < log_size - 1:
            count += 1
            predicative_orbit[count], time_array[count] = self.calc_step_euler(predicative_orbit[count - 1],
                                                                               time_array[count - 1])

        self.rocket_parameters.predicative_orbit = predicative_orbit

    def process_step(self):
        """
        Function to process step
        """
        self.calc_step()
        self.calc_predicative_orbit()
        self.detect_collision()


if __name__ == "__main__":
    initial_position = [7e6, 0, 0, 8000]
    engine = PhysicsEngine(80000, 4000, 300, 50000, 50000, initial_position)
    engine.switch_engine(True, 0.2)

    size = 500000

    position_and_velocity_log = np.ndarray(shape=(size, 4), dtype=float)
    position_and_velocity_log[0] = engine.rocket_parameters.parameters
    predicative_orbit_log = np.ndarray(shape=(100, 4), dtype=float)
    time_log = np.ndarray(shape=(size,), dtype=float)  # текущее время расчета
    step_time = 5  # шаг расчета
    counter = 0  # счетчик

    engine.set_rocket_direction(np.pi/2)

    while counter < 1000 and not engine.rocket_parameters.collision_flag:
        counter += 1
        engine.process_step()
        position_and_velocity_log[counter] = engine.rocket_parameters.parameters
        # print(engine.rocket_parameters.parameters)
        predicative_orbit_log = engine.rocket_parameters.predicative_orbit

    fig, ax = plt.subplots()
    plt.axis('equal')
    ax.add_patch(plt.Circle((0, 0), engine.constants.rad_Earth))
    ax.plot(position_and_velocity_log[:counter, 0], position_and_velocity_log[:counter, 1], color="black", linewidth=1)
    ax.plot(predicative_orbit_log[::, 0], predicative_orbit_log[::, 1])

    plt.show()

"""
    first_stage = Stage([80000, 4000, 300, 50000, 50000])  # параметры первой ступени
    second_stage = Stage([first_stage.current_stage_mass - first_stage.fuel_tank_capacity, 3000, 200, 28000,
                          28000])  # параметры второй ступени
    third_stage = Stage([second_stage.current_stage_mass - second_stage.fuel_tank_capacity, 265, 50, 1995,
                         1995])  # параметры третьей ступени"""
