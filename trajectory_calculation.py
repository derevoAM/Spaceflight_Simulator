# Calculating the trajectory of a rocket

import numpy as np


class Constants:
    """
    Constants used throughout the script execution
    """

    def __init__(self, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, step):
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
        self.initial_fas = 99 / 180 * np.pi  # начальная фаза Луны (которую нужно подогнать)

        self.gas_exhaust_speed = gas_exhaust_speed  # скорость истечения топлива
        self.fuel_consumption = fuel_consumption  # расход топлива
        self.fuel_tank_capacity = fuel_tank_capacity

        self.step = step


class RocketParameters:

    def __init__(self, initial_rocket_mass, fuel):
        self.parameters = np.array([0.0, 0, 0, 0])
        self.position_norm = np.linalg.norm(self.parameters[:2])
        self.velocity_norm = np.linalg.norm(self.parameters[2:])
        self.direction = np.array([1, 0])
        self.current_time = 0.0
        self.predicative_orbit = np.ndarray(shape=(100, 4), dtype=float)

        self.current_stage_mass = initial_rocket_mass  # масса ступени текущая
        self.fuel_remained = fuel

        self.engine_is_on_flag = False

    def renew_norms(self):
        self.position_norm = np.linalg.norm(self.parameters[:2])
        self.velocity_norm = np.linalg.norm(self.parameters[2:])

    def turn_rocket(self):
        pass

    def is_empty(self):
        return self.fuel_remained <= 0


class PhysicsEngine:

    def __init__(self, step, initial_rocket_mass, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, fuel):
        self.constants = Constants(gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, step)
        self.rocket_parameters = RocketParameters(initial_rocket_mass, fuel)

    def calc_rho(self, height):
        """
        Calculating atmosphere rho
        :param height: height above the sea level
        :return: rho
        """
        return self.constants.rho_max * np.exp(-height / self.constants.height_max)

    def reduce_mass(self):
        self.rocket_parameters.current_stage_mass -= self.constants.step * self.constants.fuel_consumption
        self.rocket_parameters.fuel_remained -= self.constants.step * self.constants.fuel_consumption

    def calc_moon_position(self):
        """
        Calculating moon position in the particular moment of time
        :return: array [x, y] of moon coordinates
        """
        return self.constants.moon_rad * np.array(
            [np.cos(self.constants.initial_fas + self.rocket_parameters.current_time / self.constants.moon_period),
             np.sin(self.constants.initial_fas + self.rocket_parameters.current_time / self.constants.moon_period)])

    def calc_acceleration_air(self):
        """
        Calculating air impact
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        if self.rocket_parameters.position_norm - self.constants.rad_Earth < 10 * self.constants.height_max:
            return - 0.5 * self.constants.C_coefficient * self.calc_rho(
                self.rocket_parameters.position_norm - self.constants.rad_Earth) * self.constants.area * \
                   self.rocket_parameters.velocity_norm * \
                   self.rocket_parameters.parameters[2:] / self.rocket_parameters.current_stage_mass
        else:
            return np.zeros(2)

    def calc_acceleration_earth(self):
        """
        Calculating gravitational acceleration by Earth of rocket stage parameters
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        return - self.constants.mu_Earth / self.rocket_parameters.position_norm ** 3 * self.rocket_parameters.parameters[
                                                                                       :2]

    def calc_acceleration_engine(self):
        """
        Calculating acceleration by engine working
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        if self.rocket_parameters.engine_is_on_flag and not self.rocket_parameters.is_empty():
            if self.rocket_parameters.velocity_norm > 1e-8:
                return self.constants.fuel_consumption * self.constants.gas_exhaust_speed / self.rocket_parameters.current_stage_mass \
                       * self.rocket_parameters.direction
            else:
                return np.array([
                    self.constants.fuel_consumption * self.constants.gas_exhaust_speed / self.rocket_parameters.current_stage_mass,
                    0])
        else:
            return np.zeros(2)

    def calc_acceleration_moon(self):
        """
        Calculating gravitational acceleration made by moon
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        rad_moon_ka = self.rocket_parameters.parameters[:2] - self.calc_moon_position()

        return - self.constants.mu_moon * rad_moon_ka / (np.linalg.norm(rad_moon_ka)) ** 3

    def calc_acceleration(self):
        """
        Calculating final value of vehicle acceleration
        :return: [ax, ay] array consisting of acceleration values for each axis
        """

        acceleration_air = self.calc_acceleration_air()

        acceleration_gravity = self.calc_acceleration_earth()

        acceleration_engine = self.calc_acceleration_engine()

        acceleration_moon = self.calc_acceleration_moon()

        return acceleration_air + acceleration_gravity + acceleration_engine + acceleration_moon

    def calc_differential(self):
        """
        Calculating Runge-Kutta method differential
        :return: [vx, vy, ax, ay] array
        """
        total_acceleration = self.calc_acceleration()

        return np.array(
            [self.rocket_parameters.parameters[2], self.rocket_parameters.parameters[3], total_acceleration[0],
             total_acceleration[1]])

    def calc_step(self):
        """
        Main function to calculate stage parameters for the next step
        :return: array [new_x, new_y, new_vx, new_vy] for the next step
        """
        k_1 = self.calc_differential()
        k_2 = self.calc_differential()
        k_3 = self.calc_differential()
        k_4 = self.calc_differential()

        self.reduce_mass()

        self.rocket_parameters.parameters += (k_1 + 2 * (k_2 + k_3) + k_4) * self.constants.step / 6

        self.rocket_parameters.current_time += self.constants.step

        self.rocket_parameters.renew_norms()

    def calc_differential_euler(self, predicative_stage_parameters):
        """
        Function to calculate differential for predicative orbit parameters
        :return: predicative [vx, vy, ax, ay] array
        """
        total_acceleration = self.calc_acceleration_earth() + self.calc_acceleration_moon()

        return np.array([predicative_stage_parameters[2], predicative_stage_parameters[3],
                         total_acceleration[0],
                         total_acceleration[1]])

    def calc_step_euler(self, predicative_stage_parameters, time):
        """
        Function to process step using basic integration method
        :param predicative_stage_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: time used in predicative calculations
        :return: predicative [new_x, new_y, new_vx, new_vy] array
        """
        return predicative_stage_parameters + self.calc_differential_euler(
            predicative_stage_parameters) * self.constants.step, time + self.constants.step * 5

    def calc_predicative_orbit(self, stage_parameters, time):
        """
        Function to calculate predicative orbit
        :param stage_parameters: current stage parameters use for further orbit predication
        :param time: time used in predicative calculations
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
            predicative_orbit[count], time_array[count] = self.calc_step_euler(predicative_orbit[count - 1],
                                                                               time_array[count - 1])

        self.rocket_parameters.predicative_orbit = predicative_orbit

    def process_step(self):
        """
        Function to process step
        :return: new time
        """
        self.calc_step()
        self.calc_predicative_orbit(self.rocket_parameters.parameters[-1], self.rocket_parameters.current_time)


if __name__ == "__main__":
    engine = PhysicsEngine()

"""size = 500000
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

plt.show()"""
